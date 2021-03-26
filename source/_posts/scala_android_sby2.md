---
title: Scala 语言开发Andorid ，开发环境的搭建(二) 
date: 2017-01-17 13:12
tags:
- 技术
- Scala
- Android
---

# Scala 语言开发Andorid ，开发环境的搭建(二)

## 什么是 sbt ？
上一篇文章介绍过，sbt 就是和 maven ，ant 类似的自动构建工具。
那 sbt 有什么优势呢？

1. 相对其他构建工具更快的编译速度，只编译修改过的文件以及引用的第三方库依赖
2. triggered execution 特性方便做测试驱动的开发
3. 依据类和依赖使用 Scala 的解析器
4. sbt 是基于 Scala ，所以可以灵活的使用 Scala 构建工程
5. 支持 java 和 Scala 的混合编程

## 基本目录
工程的根目录下的文件和文件夹，下面看看文件夹里面到底是什么东西。

### 源码
根下的 src 目录就是存放源码文件的地方呢 
```
src/
  main/
    resources/
       <files to include in main jar here>
    scala/
       <main Scala sources>
    java/
       <main Java sources>
  test/
    resources
       <files to include in test jar here>
    scala/
       <test Scala sources>
    java/
       <test Java sources>

```

### sbt 配置文件
在一个小项目中一两个 sbt 文件已经足够了，当时随着项目的扩展有可能要同时管理多个 sbt 文件

一般情况下我们习惯使用 build.sbt 作为文件的名称，当然你也可以使用任何的名字。

根目录下的 sbt 文件
```
build.sbt
project/
  plugin.sbt
  Build.scala
  <Other Scala files>
```

看到这里你可能会还好奇，sbt 和 Scala  的配置文件有什么区别

一般推荐，sbt 文件作为项目的主要设定文件，而 scala 用于设置第三方依赖或者版本信息等

## 编写build.sbt
下面一步一步写出项目到build.sbt 文件

### 表达式

在我们的定义文件了，我们只需要关注设置的表达式 

下面的实例显示了项目版本号命名等基本信息，还有 项目中使用的 Scala 版本的配置信息
```
name := "scala-on-android"

organization := "com.fortysevendeg"

organizationName := "47 Degrees"

organizationHomepage := Some(new URL("http://47deg.com"))

version := 0.1.0

scalaVersion := 2.11.6
```
不难发现上面的例子 使用 := 作为连接符

另外还可以使用其他的连接符
+= 添加多一个元素
++= 添加多个元素
例如
> scalacOptions ++= Seq("-feature", "-deprecation")

### 添加第三方库依赖

和 gradle 一样，其实库的添加分两种
一是添加本地 jar 包
二是添加远程仓库库

#### 添加 jar 包
使用 jar 包最简单到方式是直接把 jar 放到下面目录，这样项目就会自动导入 jar 包
> /src/main/libs

除此之外还能使用自定义到路径
> unmanagedBase := baseDirectory.value / "custom_lib"


#### 远程依赖
远程依赖使用是 ivy 到远程管理仓库，同样你可以使用 += 或者 ++= 到导入一个或多个依赖
先看看导入一个到基本表达式
> libraryDependencies += groupID % artifactID % revision [% configuration]

导入多个
```
libraryDependencies ++= Seq(
  aar("com.android.support" %  "cardview-v7" % "22.0.0"),
  aar("com.android.support" % "appcompat-v7" % "22.0.0"),
  aar("com.android.support" % "recyclerview-v7" % "22.0.0"),
  aar("com.google.android.gms" % "play-services-base" % "6.5.87"),
  "com.typesafe.play" %% "play-json" % "2.3.6",
  "org.specs2" %% "specs2-core" % "2.4.15" % "test",
  "org.specs2" % "specs2-mock_2.11" %  "3.0-M2" % "test")
```

上面可见，可以使用 % 作为分割符，那 %% 又代表上面意思呢。其实为何配合不同版本的 scala ，需要不同依赖， %% 就是解决这个问题的，例如上面的 "org.specs2" %% "specs2-core"  sbt 构建工具就根据不同情况选择合适的 org.specs2 或者 specs2-core 库。

### 添加 sbt 插件
 在目录 project 下有一个 plugin.sbt 文件，只需要 配置相关的信息就能方便安装对应的插件。为了更加方便使用 sbt 管理我们的 Android 工程，可以使用一些插件让开发过程中更加方便，这里说一个常用的插件
  [sbt-android](https://github.com/scala-android/sbt-android),详细使用和配置的可以看开发文档。这里只演示如何最快的安装。只需要在 plugin.sbt 添加一行便可以完成安装

 > addSbtPlugin("org.scala-android" % "sbt-android" % "1.7.1")

 接着在 根目录下的 build.sbt 中使用我们的插件

 > android.Plugin.androidBuild  
 >  platformTarget in Android := "android-21"


 这样遍可以使用这个插件提供的一些功能，例如 compile（编译），android:run（运行），android:package-release（打包）等操作。

此外插件还提供了打包的配置方案如下面设置签名文件的路径等信息
```
packageRelease <<= (packageRelease in Android).dependsOn(setDebugTask(false))

apkSigningConfig in Android := Option(
  PromptPasswordsSigningConfig(
    keystore = new File(Path.userHome.absolutePath + "/.android/signed.keystore"),
    alias = "my-password"))
```

  


