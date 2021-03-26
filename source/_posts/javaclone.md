---
title: Java 的拷贝
date: 2016-11-21 14:05
tags:
- 技术
- Java
---

# 对象的拷贝

## 深度拷贝一个对象

java.lang.Object 根类已经定义了 clone() 方法。子类只需要事项 java.lang.Cloneable 接口，就可以返回一个拷贝的对象。实现接口的同时要实现 clone() 方法里面的实现。这是拷贝方式就是浅拷贝(shallow copy of object)，这代表着原有对象的值复制一份存储在一个新的对象里面。

浅拷贝并不是完全复制原对象的所有内容，除了基本类型(int,float...)，引用类型只是复制一份引用对象的引用，那么原有的对象和拷贝的对象就指共同指向同一个引用对象。这样使用浅拷贝就会导致一些不可预测的错误。看看项目 Exampl1的例子。

```
public class Example1 {

    public static void main(String[] args) {
        // Make a Vector
        Vector original = new Vector();

        // Make a StringBuffer and add it to the Vector
        StringBuffer text = new StringBuffer("The quick brown fox");
        original.addElement(text);

        // Clone the vector and print out the contents
        Vector clone = (Vector) original.clone();
        System.out.println("A. After cloning");
        printVectorContents(original, "original");
        printVectorContents(clone, "clone");
        System.out.println(
            "--------------------------------------------------------");
        System.out.println();

        // Add another object (an Integer) to the clone and 
        // print out the contents
        clone.addElement(new Integer(5));
        System.out.println("B. After adding an Integer to the clone");
        printVectorContents(original, "original");
        printVectorContents(clone, "clone");
        System.out.println(
            "--------------------------------------------------------");
        System.out.println();

        // Change the StringBuffer contents
        text.append(" jumps over the lazy dog.");
        System.out.println("C. After modifying one of original's elements");
        printVectorContents(original, "original");
        printVectorContents(clone, "clone");
        System.out.println(
            "--------------------------------------------------------");
        System.out.println();
    }

    public static void printVectorContents(Vector v, String name) {
        System.out.println("  Contents of \"" + name + "\":");

        // For each element in the vector, print out the index, the
        // class of the element, and the element itself
        for (int i = 0; i < v.size(); i++) {
            Object element = v.elementAt(i);
            System.out.println("   " + i + " (" + 
                element.getClass().getName() + "): " + 
                element);
        }
        System.out.println();
    }

}
```

Exampl1 运行输出的结果：
```
A. After cloning
  Contents of "original":
   0 (java.lang.StringBuffer): The quick brown fox

  Contents of "clone":
   0 (java.lang.StringBuffer): The quick brown fox

--------------------------------------------------------

B. After adding an Integer to the clone
  Contents of "original":
   0 (java.lang.StringBuffer): The quick brown fox

  Contents of "clone":
   0 (java.lang.StringBuffer): The quick brown fox
   1 (java.lang.Integer): 5

--------------------------------------------------------

C. After modifying one of original's elements
  Contents of "original":
   0 (java.lang.StringBuffer): The quick brown fox jumps over the lazy dog.

  Contents of "clone":
   0 (java.lang.StringBuffer): The quick brown fox jumps over the lazy dog.
   1 (java.lang.Integer): 5

--------------------------------------------------------
```

运行结果打印出3个区域块，在第一个区域块中成功的创建了一个对象和复制拷贝了一个一模一样的对象。从第二个区域块可以看出两个对象是相互对立的，当往复制拷贝的对象添加一个 Integer 数值，打印的结果显示原有的对象不受影响，复制拷贝的对象打印添加的数值。第三个区域块修改了 StringBuffer 的值，打印显示出两个对象里面的内容同时被修改了，这恰恰验证了上面的说法，应用类型的值时用 clone 时无法被完全复制过去的。

所以使用 clone 这种方法复制内容可能会造成不可预测的错误。

为了解决浅拷贝带来的问题，另外的解决方案是使用*深度拷贝(deep copy of object)* 。深度拷贝使得原有对象和新对象完全独立，对象里面的所有属性都完成被复制过去。Java Api 提供的 clone 方法无法一步到位的深度拷贝，只能为对象里面的所有的熟悉均实现 Cloneable 接口，为所有的属性变量 clone 一遍。就如同上的例子，需要重写 clone 方法拷贝一个新的字符串，再把新的字符串对象复制给 Vector克隆出来的对象。
不过这种做法有几点缺点：


1. 要拷贝一个对象，必须修改这个类里面所有元素的 clone 方法。假如你使用第三库的代码，而且没有源码这就无法使用这个方法，还有如果使用 final 修饰变量这也是没使用这个拷贝方法
2. 要有权限访问父类属性变量，如果某个变量是私有属性就没有权限修改它
3. 必须要确定属性变量的类型，尤其不能运行中才能确定的类型
4. 操作繁琐容易出错

另外一种通用的办法就是使用 Java Object Serialization (JOS) ，使用序列化，使用把 ObjectOutputStream       对象写入出入到一个数组中，再使用 ObjectInputStream 复制到另一个对象，从而得到两个完全独立的对象。

```
import java.io.IOException;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.io.ObjectInputStream;

/**
 * Utility for making deep copies (vs. clone()'s shallow copies) of 
 * objects. Objects are first serialized and then deserialized. Error
 * checking is fairly minimal in this implementation. If an object is
 * encountered that cannot be serialized (or that references an object
 * that cannot be serialized) an error is printed to System.err and
 * null is returned. Depending on your specific application, it might
 * make more sense to have copy(...) re-throw the exception.
 *
 * A later version of this class includes some minor optimizations.
 */
public class UnoptimizedDeepCopy {

    /**
     * Returns a copy of the object, or null if the object cannot
     * be serialized.
     */
    public static Object copy(Object orig) {
        Object obj = null;
        try {
            // Write the object out to a byte array
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            ObjectOutputStream out = new ObjectOutputStream(bos);
            out.writeObject(orig);
            out.flush();
            out.close();

            // Make an input stream from the byte array and read
            // a copy of the object back in.
            ObjectInputStream in = new ObjectInputStream(
                new ByteArrayInputStream(bos.toByteArray()));
            obj = in.readObject();
        }
        catch(IOException e) {
            e.printStackTrace();
        }-快速深度拷贝一个对象
        catch(ClassNotFoundException cnfe) {
            cnfe.printStackTrace();
        }
        return obj;
    }

}


```

这种方法也是有缺点的：


1. 必须序列化，都要实现 java.io.Serializable 接口
2. 序列化影响程序运输速度。
3. 可以适应不同的对象大小，创建适合大小的数组，可以在多线程任务中安全使用。符合上面种种特点，可想而知速度是有多慢。

出于以上的种种缺点，可以对 ByteArrayOutputStream 和 ByteArrayInputStream 做出3点优化：

1. ByteArrayOutputStream 默认初始化 32 byte的数组，遇到大的对象就增大为目前两倍大的数组，这意味着要摒弃到初始化的小数组，优化这个问题的方法也简单，初始化一个大的数组。
2. ByteArrayOutputStream 修改的内容都是 synchronized 修饰的，这是个安全的做法，但是在确定的单一线程里许可以抛弃 synchronized 这样做也是安全的。
3. toByteArray() 方法会创建和复制一个字节流数组。检索数据数组然后继续写入流中，原有的数据就不会被改变。尽管如此，这循环复制一个数组会造成多余的垃圾回收工作。

#深度拷贝速度优化

FastByteArrayOutputStream.class
```
import java.io.OutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ByteArrayInputStream;

/**
 * ByteArrayOutputStream implementation that doesn't synchronize methods
 * and doesn't copy the data on toByteArray().
 */
public class FastByteArrayOutputStream extends OutputStream {
    /**
     * Buffer and size
     */
    protected byte[] buf = null;
    protected int size = 0;

    /**
     * Constructs a stream with buffer capacity size 5K 
     */
    public FastByteArrayOutputStream() {
        this(5 * 1024);
    }

    /**
     * Constructs a stream with the given initial size
     */
    public FastByteArrayOutputStream(int initSize) {
        this.size = 0;
        this.buf = new byte[initSize];
    }

    /**
     * Ensures that we have a large enough buffer for the given size.
     */
    private void verifyBufferSize(int sz) {
        if (sz > buf.length) {
            byte[] old = buf;
            buf = new byte[Math.max(sz, 2 * buf.length )];
            System.arraycopy(old, 0, buf, 0, old.length);
            old = null;
        }
    }

    public int getSize() {
        return size;
    }

    /**
     * Returns the byte array containing the written data. Note that this
     * array will almost always be larger than the amount of data actually
     * written.
     */
    public byte[] getByteArray() {
        return buf;
    }

    public final void write(byte b[]) {
        verifyBufferSize(size + b.length);
        System.arraycopy(b, 0, buf, size, b.length);
        size += b.length;
    }

    public final void write(byte b[], int off, int len) {
        verifyBufferSize(size + len);
        System.arraycopy(b, off, buf, size, len);
        size += len;
    }

    public final void write(int b) {
        verifyBufferSize(size + 1);
        buf[size++] = (byte) b;
    }

    public void reset() {
        size = 0;
    }

    /**
     * Returns a ByteArrayInputStream for reading back the written data
     */
    public InputStream getInputStream() {
        return new FastByteArrayInputStream(buf, size);
    }

}
```

ByteArrayInputStream.class
```
import java.io.InputStream;
import java.io.IOException;

/**
 * ByteArrayInputStream implementation that does not synchronize methods.
 */
public class FastByteArrayInputStream extends InputStream {
    /**
     * Our byte buffer
     */
    protected byte[] buf = null;

    /**
     * Number of bytes that we can read from the buffer
     */
    protected int count = 0;

    /**
     * Number of bytes that have been read from the buffer
     */
    protected int pos = 0;

    public FastByteArrayInputStream(byte[] buf, int count) {
        this.buf = buf;
        this.count = count;
    }

    public final int available() {
        return count - pos;
    }

    public final int read() {
        return (pos < count) ? (buf[pos++] & 0xff) : -1;
    }

    public final int read(byte[] b, int off, int len) {
        if (pos >= count)
            return -1;

        if ((pos + len) > count)
            len = (count - pos);

        System.arraycopy(buf, pos, b, off, len);
        pos += len;
        return len;
    }

    public final long skip(long n) {
        if ((pos + n) > count)
            n = count - pos;
        if (n < 0)
            return 0;
        pos += n;
        return n;
    }

}
```
ByteArrayInputStream 和 ByteArrayOutputStream 的使用
```
import java.io.IOException;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.io.ObjectInputStream;

/**
 * Utility for making deep copies (vs. clone()'s shallow copies) of 
 * objects. Objects are first serialized and then deserialized. Error
 * checking is fairly minimal in this implementation. If an object is
 * encountered that cannot be serialized (or that references an object
 * that cannot be serialized) an error is printed to System.err and
 * null is returned. Depending on your specific application, it might
 * make more sense to have copy(...) re-throw the exception.
 */
public class DeepCopy {

    /**
     * Returns a copy of the object, or null if the object cannot
     * be serialized.
     */
    public static Object copy(Object orig) {
        Object obj = null;
        try {
            // Write the object out to a byte array
            FastByteArrayOutputStream fbos = 
                    new FastByteArrayOutputStream();
            ObjectOutputStream out = new ObjectOutputStream(fbos);
            out.writeObject(orig);
            out.flush();
            out.close();

            // Retrieve an input stream from the byte array and read
            // a copy of the object back in. 
            ObjectInputStream in = 
                new ObjectInputStream(fbos.getInputStream());
            obj = in.readObject();
        }
        catch(IOException e) {
            e.printStackTrace();
        }
        catch(ClassNotFoundException cnfe) {
            cnfe.printStackTrace();
        }
        return obj;
    }

}
```

