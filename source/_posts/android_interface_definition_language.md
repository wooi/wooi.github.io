---
title: AIDL 官方使用介绍
date: 2016-11-21 14:09
tags:
- 技术
- 算法
---

# Android Interface Definition Language (AIDL)
AIDL是允许你完成自定义接口，用于不同进程中服务器和客户端之间的通讯。主要是因为Android不允许你直接跨进程间传递消息，所以需要通过AIDL把传递的对象分解包装为操作系统可以接受的对象。

>当你的Service提供跨进程通讯，而且在服务中做多线程处理时你可以使用AIDL。如果当前的Service不准备提供给其他进程服务端做访问你只需要在服务中实现自定义的binder即可。或者你想实现IPC（进程间通讯），Service内又不需要做多线程管理，这种情况下你只要使用Messager。当然要合理选择哪一种方式的前提是你清楚了解如何绑定一Service；

设计AIDL接口时，要知道你在什么情景下才需要调用你这个接口

- 如果只是本地进程中调用这个接口，完全没必要使用AIDL,这时候只要在服务中实现binder即可
- 提供接口给远程进程，这时候可能接受远程中不同的线程访问你的接口，换句话说，你要在你的接口中保证线程的安全
- The oneway keyword modifies the behavior of remote calls. When used, a remote call does not block; it simply sends the transaction data and immediately returns. The implementation of the interface eventually receives this as a regular call from the Binder thread pool as a normal remote call. If oneway is used with a local call, there is no impact and the call is still synchronous.

## 定义AIDL接口
使用java语法在源码目录中创建你的 *.aidl* 文件

当你在应用中创建了 *.aidl* 文件，Android SDK tools 会基于这个文件自动为我们在 *gen/* 目录中生成IBinder对象。这样客户端就可以通过IBinder实现IPC通讯

通过AIDL绑定服务的如下步骤：

1. 创建 *.aidl* 文件
2. 实现接口

    文件自动创建接口文件，内部Stub类必须继承Binder，实现Stubd方法内的行为

3. 对客户端暴露接口

    实现的Service重写 onBind()方法 返回你实现的stub类

> aidl文件的做了任何的改变，切记修改使用你服务的客户端

### 1.创建 *.aidl* 文件

**IRemoteService.aidl**
```
// IRemoteService.aidl
package com.example.administrator.aidl.AIDL;

import com.example.administrator.aidl.AIDL.IRemoteServiceCallback;

// Declare any non-default types here with import statements

interface IRemoteService {
    /**
     * Demonstrates some basic types that you can use as parameters
     * and return values in AIDL.
     */
    void registerCallback(IRemoteServiceCallback cb);
    void unregisterCallback(IRemoteServiceCallback cb);
}

```

**ISecondary.aidl**
```
// ISecondary.aidl
package com.example.administrator.aidl.AIDL;

// Declare any non-default types here with import statements

interface ISecondary {
    /**
     * Demonstrates some basic types that you can use as parameters
     * and return values in AIDL.
     */

    int getPid();
}

```
**IRemoteServiceCallback.aidl**
```
// IRemoteServiceCallback.aidl
package com.example.administrator.aidl.AIDL;

// Declare any non-default types here with import statements

interface IRemoteServiceCallback {
    /**
     * Demonstrates some basic types that you can use as parameters
     * and return values in AIDL.
     */
    void valueChanged(int value);
}

```

### 实现 *.aidl* 文件中的接口,如实现 *IRemoteService.aidl* 和 *ISecondary.aidl* 接口

创建 *.aidl* 文件时，Android skd Tool 会自动对应的java文件，其中会生成一个继承Binder抽象内部类 *Stub* 。所以在服务中继承Stub，实现自己的内部方法，例如下面RemoteService中 mBinder和mSecondaryBinder中的实现

### 暴露你的接口，例如在例如下面RemoteService中OnBind的方法中，把实现的对象返回给客户端程序

**RemoteService**
```
public class RemoteService extends Service {

    @Override
    public void onCreate() {
        super.onCreate();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        if (IRemoteService.class.getName().equals(intent.getAction())) {
            return mBinder;
        }
        if (ISecondary.class.getName().equals(intent.getAction())) {
            return mSecondaryBinder;
        }
        return null;
    }

    private final IRemoteService.Stub mBinder = new IRemoteService.Stub() {

        @Override
        public void registerCallback(IRemoteServiceCallback cb) throws RemoteException {
                cb.valueChanged(mSecondaryBinder.getPid());
        }

        @Override
        public void unregisterCallback(IRemoteServiceCallback cb) throws RemoteException {

        }
    };

    private final ISecondary.Stub mSecondaryBinder = new ISecondary.Stub() {
        @Override
        public int getPid() throws RemoteException {
            return Process.myPid();
        }
    };

}
```

### 绑定方法如同bind方法一样，bindService(intent, mConnection, Context.BIND_AUTO_CREATE);

```
public class Binding extends Activity {
    private static final int BUMP_MSG = 1;
    TextView mCallbackText;
    IRemoteService mService;
    Button mKillButton;
    Boolean mIsBound;
    ISecondary mSecondaryService;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.aidl_layout);

        Button bindbutton = (Button) findViewById(R.id.bind);

        bindbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Binding.this, RemoteService.class);
                intent.setAction(IRemoteService.class.getName());
                bindService(intent, mConnection, Context.BIND_AUTO_CREATE);

                intent.setAction(ISecondary.class.getName());
                bindService(intent, mSecondaryConnection, Context.BIND_AUTO_CREATE);
                mCallbackText.setText("Binding.");
                mIsBound = true;
            }
        });

        Button unbindbutton = (Button) findViewById(R.id.unbind);
        unbindbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (mIsBound) {
                    if (mService != null) {
                        try {
                            mService.unregisterCallback(mCallback);
                        } catch (RemoteException e) {
                            e.printStackTrace();
                        }
                        unbindService(mConnection);
                        mKillButton.setEnabled(false);
                        mIsBound = false;
                        mCallbackText.setText("Unbinding");
                    }
                }
            }
        });
        mKillButton = (Button) findViewById(R.id.kill);
        mKillButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (mSecondaryService != null) {
                    try {
                        int pid = mSecondaryService.getPid();
                        Process.killProcess(pid);
                        mCallbackText.setText("Killed service process.");
                    } catch (RemoteException e) {
                        e.printStackTrace();
                        Toast.makeText(Binding.this,
                                R.string.remote_call_failed,
                                Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });
        mKillButton.setEnabled(false);

        mCallbackText = (TextView) findViewById(R.id.callback);
        mCallbackText.setText("Not attached.");
    }


    private ServiceConnection mConnection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName componentName, IBinder iBinder) {
            Log.e("TAG","connected");
            mService = IRemoteService.Stub.asInterface(iBinder);
            mKillButton.setEnabled(true);
            mCallbackText.setText("Attached");
            try {
                mService.registerCallback(mCallback);
            } catch (RemoteException e) {
                e.printStackTrace();
            }
            Toast.makeText(Binding.this, R.string.remote_service_connected,
                    Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onServiceDisconnected(ComponentName componentName) {
            mService = null;
            mKillButton.setEnabled(false);
            mCallbackText.setText("Disconnected.");

        }
    };

    private ServiceConnection mSecondaryConnection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName componentName, IBinder iBinder) {
            mSecondaryService = ISecondary.Stub.asInterface(iBinder);
            mKillButton.setEnabled(true);
        }

        @Override
        public void onServiceDisconnected(ComponentName componentName) {
            mSecondaryService = null;
            mKillButton.setEnabled(false);
        }
    };


    private IRemoteServiceCallback mCallback = new IRemoteServiceCallback.Stub() {
        @Override
        public void valueChanged(int value) throws RemoteException {
            mHandler.sendMessage(mHandler.obtainMessage(BUMP_MSG, value, 0));
        }
    };

    private Handler mHandler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            switch (msg.what) {
                case BUMP_MSG:
                    mCallbackText.setText("Received from service: " + msg.arg1);
                    break;
                default:
                    super.handleMessage(msg);
            }
        }

    };

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if(mService!=null){
            unbindService(mConnection);
        }
    }
}
```

### IPC传递对象
1. 传递的对象实现Parcelable接口
2. 在对象的类中实现 writeToParcel方法
3. 添加一个静态变量CREATOR并且实现Parcelable.Creator 的接口
4. 在目录中添加一个.aidl文件声明上面所创建的parcelable 类,列如如下

Rect.aidl
```
package android.graphics;
parcelable Rect;
```
这里创建我们的Rect类，并实现现Parcelable接口，类中再实现writeToParcel方法，静态变量CREATOR

Rect.java
```
public class Rect implements Parcelable {
    public int left;
    public int top;
    public int right;
    public int bottom;

    public static final Parcelable.Creator<Rect> CREATOR = new Creator<Rect>() {
        @Override
        public Rect createFromParcel(Parcel parcel) {
            return new Rect(parcel);
        }

        @Override
        public Rect[] newArray(int i) {
            return new Rect[i];
        }
    };

    public Rect() {
    }

    private Rect(Parcel in) {
        readFromParcel(in);
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel parcel, int i) {
        parcel.writeInt(left);
        parcel.writeInt(top);
        parcel.writeInt(right);
        parcel.writeInt(bottom);
    }

    public void readFromParcel(Parcel in) {
        left = in.readInt();
        top = in.readInt();
        right = in.readInt();
        bottom = in.readInt();
    }

}
```

在 IRemoteService.aidl添加下面的接口
```
Rect getRect();
```
在RemoteService.java中的mBinder对象中实现以下方法，这里我们对服务返回的对象进行赋值
```
 @Override
        public Rect getRect() throws RemoteException {
            Rect rect = new Rect();
            rect.bottom = 10;
            rect.top = 10;
            rect.left = 5;
            rect.right = 6;
            return rect;
        }
```

这样我们便可以在客户端中先服务获取我的对象，具体在Bindnd.java中的mConnection得到Rect对象，如下
```
   private ServiceConnection mConnection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName componentName, IBinder iBinder) {
            Log.e("TAG", "connected");
            mService = IRemoteService.Stub.asInterface(iBinder);
            mKillButton.setEnabled(true);
            mCallbackText.setText("Attached");
            try {
                //获取到服务端中的Rect对象
                android.graphics.Rect rectFromService = mService.getRect();
                Log.e("TAG","bottom = "+rectFromService.bottom+",top = "+rectFromService.top+",left = "+rectFromService.left+",right ="+rectFromService.right);
                mService.registerCallback(mCallback);
            } catch (RemoteException e) {
                e.printStackTrace();
            }
            Toast.makeText(Binding.this, R.string.remote_service_connected,
                    Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onServiceDisconnected(ComponentName componentName) {
            mService = null;
            mKillButton.setEnabled(false);
            mCallbackText.setText("Disconnected.");

        }
    };
```
