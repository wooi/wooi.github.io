---
title: 注解解释
date: 2016-11-21 12:19:54
tags:
---

Java注解又称Java标注，是Java语言5.0版本开始支持加入源代码的特殊语法元数据[1]。
Java语言中的类、方法、变量、参数和包等都可以被标注。Java标注和Javadoc不同，标注有自反性。在编译器生成类文件时，标注可以被嵌入到字节码中，由Java虚拟机执行时获取到标注[2]。

```
 // @Twizzle标注toggle()方法。
  @Twizzle
  public void toggle() {
  }

  // 声明Twizzle标注
  public @interface Twizzle {
  }
```

标注可以包含一个关键字和值的对所构成的列表：
```
 //等同于 @Edible(value = true)
  @Edible(true)
  Item item = new Carrot();

  public @interface Edible {
    boolean value() default false;
  }

  @Author(first = "Oompah", last = "Loompah")
  Book book = new Book();

  public @interface Author {
    String first();
    String last();
  }
```