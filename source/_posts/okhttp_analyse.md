---
title: Okhttp 源码解析
date: 2016-11-21 14:09
tags:
---

# Okhttp解析

### 总体思想
分析源码，首先要熟悉用例，由上到下一层一层剥开源码，初步了解项目的框架，然后再细看代码的实现细节。现在试着分析 OKhttp 的源码，下面代码是来至 [OKhttp官网](https://square.github.io/okhttp/#examples)。

GET A URL

```
OkHttpClient client = new OkHttpClient(); //(1)

String run(String url) throws IOException {
  Request request = new Request.Builder()
      .url(url)
      .build();                           //(2)

  Response response = client.newCall(request).execute();  //(3)
  return response.body().string();                        //(4)
}
```
1. 创建一个 OkHttpClient 对象。
2. 创建一个 Request 对象，可以设置 URL 等网络配置。
3. 调用 OkHttpClient 的 newCall() 方法，并把自定义配置的Request对象作为参数传进去。到处为止程序成功的将需要的请求放在了队列中，执行 execute() 方法开始向服务器发起请求，服务器返回的信息转化为 Response 对象。
4. 返回 response 对象的 body 主体信息。

一张来至[piasy](http://blog.piasy.com/)的流程图:
![image](http://blog.piasy.com/img/201607/okhttp_full_process.png)

### 细节分析

#### 创建 OkHttpClient 对象

```
OkHttpClient client = new OkHttpClient();
```

OkHttpClient.class 里面的两个构造函数：
```
public OkHttpClient() {
    this(new Builder());
  }
  
private OkHttpClient(Builder builder) {
    this.dispatcher = builder.dispatcher;
    this.proxy = builder.proxy;
    this.protocols = builder.protocols;
    .
    .
    .
    this.retryOnConnectionFailure = builder.retryOnConnectionFailure;
    this.connectTimeout = builder.connectTimeout;
    this.readTimeout = builder.readTimeout;
    this.writeTimeout = builder.writeTimeout;
  }

```
上面可以看出，new OkHttpClient() 是调用 OkHttpClient.class 另外一个 private 的构造函数 OkHttpClient(Builder builder) ，其中 Builder 是 OkHttpClient 的一个内部类，Builder 是使用了[构造者模式](https://www.tutorialspoint.com/design_pattern/builder_pattern.htm)，里面包含了一些配置相关的字段如下：

```
    final Dispatcher dispatcher;  //分发器
    final Proxy proxy; //代理
    final List<Protocol> protocols; //协议
    final List<ConnectionSpec> connectionSpecs; //传输层版本和连接协议
    final List<Interceptor> interceptors; //拦截器
    final List<Interceptor> networkInterceptors; //网络拦截器
    .
    .
    .
    final int readTimeout; //read 超时
    final int writeTimeout; //write 超时
```

#### 创建 Request 对象
创建完 OkHttpClient 对象后，就需要我们创建一个Request，Request 作用就是承载用户的请求，最简单的也是必须的做法是设置  Request 的 URL。同样和创建 OkHttpClient 对象一样，Request 也是使用 构造者模式，其中包含了 URL, header, body等字段，简单看看源码中的 Request 的构造函数：

```
 private Request(Builder builder) {
    this.url = builder.url;
    this.method = builder.method;
    this.headers = builder.headers.build();
    this.body = builder.body;
    this.tag = builder.tag != null ? builder.tag : this;
  }
```

#### 真正开始工作啦

##### 同步请求
最上面的官方示例代码是一个同步的网络请求，接着我们一步一步拆解代码。
```
//官方示例代码
Response response = client.newCall(request).execute(); 
```

```
//OkHttpClient.class
public Call newCall(Request request) {
    return new RealCall(this, request);
  }

```

```
//Recall.class
  protected RealCall(OkHttpClient client, Request originalRequest) {
    this.client = client;
    this.originalRequest = originalRequest;
    this.retryAndFollowUpInterceptor = new RetryAndFollowUpInterceptor(client);
  }
  
    @Override protected void execute() {
      boolean signalledCallback = false;
      try {
        Response response = getResponseWithInterceptorChain();
        if (retryAndFollowUpInterceptor.isCanceled()) {
          signalledCallback = true;
          responseCallback.onFailure(RealCall.this, new IOException("Canceled"));
        } else {
          signalledCallback = true;
          responseCallback.onResponse(RealCall.this, response);
        }
      } catch (IOException e) {
        if (signalledCallback) {
          // Do not signal the callback twice!
          Platform.get().log(INFO, "Callback failure for " + toLoggableString(), e);
        } else {
          responseCallback.onFailure(RealCall.this, e);
        }
      } finally {
        client.dispatcher().finished(this);
      }
    }
```
在 OkhttpClient 代码里面看到，newCall() 函数返回一个 Call 对象，其实 Call 是一个接口，而我们的没一次请求都是转载在一个 Call 对象中。其中看到返回的是一个 RealCall 对象，由这里看到 RealCall 是 Call 的一个实现类。

Ok，接着看看 RealCall 对象的 execute() 方法，可以看到这样一行最重要的代码 Response response = getResponseWithInterceptorChain() ，通过这一个方法可得到从服务器返回的一个 Response 对象。从这个函数的名字可以推测，这是一个接一个的链式调用，接下来也可以从源码发现，这个地方使用了[责任链模式](https://www.tutorialspoint.com/design_pattern/chain_of_responsibility_pattern.htm)

```
//RealCall.call
private Response getResponseWithInterceptorChain() throws IOException {
    // Build a full stack of interceptors.
    List<Interceptor> interceptors = new ArrayList<>();
    interceptors.addAll(client.interceptors());
    interceptors.add(retryAndFollowUpInterceptor);
    interceptors.add(new BridgeInterceptor(client.cookieJar()));
    interceptors.add(new CacheInterceptor(client.internalCache()));
    interceptors.add(new ConnectInterceptor(client));
    if (!retryAndFollowUpInterceptor.isForWebSocket()) {
      interceptors.addAll(client.networkInterceptors());
    }
    interceptors.add(new CallServerInterceptor(
        retryAndFollowUpInterceptor.isForWebSocket()));

    Interceptor.Chain chain = new RealInterceptorChain(
        interceptors, null, null, null, 0, originalRequest);
    return chain.proceed(originalRequest);
  }
```

上的代码总的功能就是往一个 list 里面一个一个的添加 interceptor ，interceptor 是一个抽象的接口，而代码里添加的各种各样的拦截器都是对 interceptor 接口不同的实现。例如，首先添加用户自己配置的interceptor，然后添加 retryAndFollowUpInterceptor 主要负责重定向和失败重连，接着添加 BridgeInterceptor 主要负责转化用户配置的url，header等配置生成一个服务器能接受的文本格式。列表中 CacheInterceptor 我们大概能猜出它的作用，这是一个缓存拦截器，根据 url 读取缓存中的数据，如果有结果就在这里砍断链式调用，成功返回结果。 ConnectInterceptor 则是开始向服务器发起连接。CallServerInterceptor 是正式与服务器发生关系，也是从这个拦截器中返回最终的 Response 结果。

当然，要发生上述的所有动作必须有一个起点，chain.proceed(originalRequest) 就是整个链路的入口，就在这里开始一个环节扣着一个环节执行下去。放回最终的结果，这不，一次完整的同步网络请求就完成了。

##### 异步请求
上面是一个同步请求的解析，现在来谈谈异步请求，它跟同步请求有异曲同工之妙，大部分的流程实现还是沿用同一份代码，最大的不同是异步请求加入了 dispatcher ，见面知其意，就是由这个类来负责分发用户的请求。按照上面的思路，首先看看一个异步的示例

```
//异步示例
OkHttpClient client=new OkHttpClient();

Request request = new Request.Builder()
                        .url(url)
                        .build();

client.newCall(request)
        .enqueue(new Callback() {
            @Override
            public void onResponse(Call call, Response response) throws IOException {

            }

            @Override
            public void onFailure(Call call, IOException e) {

            }
        });
```

Request 和 OkHttpClient 创建和同步请求一致，重点在与 RealCall() 接口里面的 enqueue(CallBack callback) 方法。传入的当然是一个 CallBack 接口对象用户需要服务器返回的消息通过这个对象传递回来。复写的 onResponse() 成功获取服务器端返回的结果，onFailure() 返回错误失败的信息，下面接着看 enqueued() 调用栈。

```
//RealCall.class
  @Override 
  public void enqueue(Callback responseCallback) {
    synchronized (this) {
      if (executed) throw new IllegalStateException("Already Executed");
      executed = true;
    }
    client.dispatcher().enqueue(new AsyncCall(responseCallback));
  }
    //RealCall 内部类继承NamedRunnable（代码向下滑）
  final class AsyncCall extends NamedRunnable {
    private final Callback responseCallback;

    private AsyncCall(Callback responseCallback) {
      super("OkHttp %s", redactedUrl().toString());
      this.responseCallback = responseCallback;
    }
    
    @Override protected void execute() {
      boolean signalledCallback = false;
      try {
        Response response = getResponseWithInterceptorChain();
        if (retryAndFollowUpInterceptor.isCanceled()) {
          signalledCallback = true;
          responseCallback.onFailure(RealCall.this, new IOException("Canceled"));
        } else {
          signalledCallback = true;
          responseCallback.onResponse(RealCall.this, response);
        }
      } catch (IOException e) {
        if (signalledCallback) {
          // Do not signal the callback twice!
          Platform.get().log(INFO, "Callback failure for " + toLoggableString(), e);
        } else {
          responseCallback.onFailure(RealCall.this, e);
        }
      } finally {
        client.dispatcher().finished(this);
      }
    }
  }
  
```
```
//Dispatcher.class
  private final Deque<AsyncCall> readyAsyncCalls = new ArrayDeque<>();
  private final Deque<AsyncCall> runningAsyncCalls = new ArrayDeque<>();
  private final Deque<RealCall> runningSyncCalls = new ArrayDeque<>();
  
 synchronized void enqueue(AsyncCall call) {
    if (runningAsyncCalls.size() < maxRequests && runningCallsForHost(call) < maxRequestsPerHost) {
      runningAsyncCalls.add(call);
      executorService().execute(call);
    } else {
      readyAsyncCalls.add(call);
    }
  }
```

```
//NamedRunnable.class
public abstract class NamedRunnable implements Runnable {
  protected final String name;

  public NamedRunnable(String format, Object... args) {
    this.name = Util.format(format, args);
  }

  @Override public final void run() {
    String oldName = Thread.currentThread().getName();
    Thread.currentThread().setName(name);
    try {
      execute();
    } finally {
      Thread.currentThread().setName(oldName);
    }
  }

  protected abstract void execute();
}

```
RealCall 类 enqueue(Callback responseCallback) 中可以看到 dispatcher() 方法 ，dispatcher 也有一个 enqueue(AsyncCall call) 方法， 在这个 enqueue 方法里有一个列表并且执行 AsynCall ，如何执行 AsynCall 呢? AsynCall 是 RealCall 的内部类，集成 NamedRunnable，NamedRunnable 继承 Runanble。最终的与服务器发生交互的动作就在 AsynCall 的 execute() 方法内，这里就看到了熟悉的一行代码 ：

```
Response response = getResponseWithInterceptorChain();

```
执行的流程就和同步的请求一模一样，不同点是再取得的服务器最终结果 Callback 接口放回给用户。

### 总结
更好读懂 OKHttp 的源码关键是要了解常用的设计模式，用构造模式创建出 OkHttpClient 和 Request 对象，使用责任链模式完成一个链式的调用。个人认为这就是 OkHttp 最基本的框架。代码的还有许多设计精良的部分，还未还好细读，目前还不把每一部分做到庖丁解牛的境界，有时间再一另帮 Blog 做另外的分析。