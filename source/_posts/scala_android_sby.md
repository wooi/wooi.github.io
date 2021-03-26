---
title: Scala 语言开发Andorid ，开发环境的搭建(一)
date: 2017-01-10 21:43
tags:
- 技术
- Scala
- Android
---

# Scala 语言开发Andorid ，开发环境的搭建(一)

厌倦 Java 繁琐的语法，为了更优雅的开发 Android 程序，Scala 代替 Java 是一个不错的尝试。 开发前可以学习 Scala 的基本语法，某些部分和 Java 非常类似，但又聚合了其他先进语言的特性。与 Java 不同的是，在你熟悉函数式编程的情况下能写出更加优雅的代码。

## SBT 构建工具
现在绝大多数的 Android 开发者是官方提供的 Android Studio ，这个 IDE 使用的是基于 Gradle 的自动化建构工具，通过 Gradle 可以配置 Project 各种参数，生产 APK 等操作。
SBT 是和 Gradle,Ant,Maven 一样的自动化建构工具，SBT 方便管理我们用 Scala 编写的 Android 工程。

和使用 Java 开发 Andoird 一样，首先要安装 Scala， [下载](http://scala-lang.org/download/) 官方文件，在此之前先确定电脑已经安装配置好 Java 环境。如果 macOS 已经安装有 Homebrew 只需要一行代码即可安装配置成功
```
brew install scala
```
接着安装 SBT 同一也一行代码搞定(赶紧换一台 mac 吧~~
```
brew install sbt
```
其他系统的配置大可直接看 [Scala]((http://scala-lang.org/) 和 [SBT](http://www.scala-sbt.org/index.html) 官网，里边有详细的安装配置教程


## 项目结构
和使用 构建工具一样，Gradle 有一种固定的文件分类方式，不同的文件夹安放不同类型的文件。同样的，SBT 也是有固定的文件结构。其实 SBT 的结构和 Gradle 的结构类似。

```
scala-android/
|- project/
|  |- plugins.sbt 
|- src/
|  |- main/
|     |- assets/
|     |- java/
|     |- res/
|        |- layout/
|           |- main.xml
|        |- values/
|           |- strings.xml
|     |- scala/
|        |- com/
|           |- fortysevendeg/
|              |- scala/
|                 |- android/
|                    |- SampleActivity.scala/
|     |- AndroidManifest.xml
|  |- test/
|     |- java/
|     |- res/
|     |- scala/
|- build.sbt
```

## 结构文件

根目录下，src 文件夹内存放的有源码的文件，布局文件，以及另外一些资源文件。java 文件存放的是 java的源代码文件，scala文件夹里存放的当然是 scala 源代码文件，和 java 编写的结构一样，倒序域名包命名的管理方式。text存放的是测试文件。

build.sbt 和 app 中Gradle build  文件类似，可以配置一些项目信息，例如管理包名，应用名，编译的目标版本，最低限制版本，开启混淆的。使用的语法与 gradle 的语法略有不同。下面是一些常用的配置信息。
**build.sbt**
```
// 申明使用 Android 插件，让构造工具知道这是一个Android 工程
android.Plugin.androidBuild
​    
// 生命 Android 目标 API 
platformTarget in Android := "android-21"

// 应用名
name := """scala-android"""

// 应用版本号
version := "1.0.0"

// Scala 版本
scalaVersion := "2.11.4"

// 项目中依赖的库
resolvers += Resolver.jcenterRepo
libraryDependencies ++=
  "com.android.support" % "cardview-v7" % supportLibsVersion ::
  "com.android.support" % "customtabs" % supportLibsVersion ::
  "com.android.support" % "design" % supportLibsVersion ::
  "com.android.support" % "gridlayout-v7" % supportLibsVersion ::
  "com.android.support" % "preference-v14" % supportLibsVersion ::
  "com.futuremind.recyclerfastscroll" % "fastscroll" % "0.2.5" ::
  "com.evernote" % "android-job" % "1.1.4" ::
  "com.github.jorgecastilloprz" % "fabprogresscircle" % "1.01" ::
  "com.google.android.gms" % "play-services-ads" % playServicesVersion ::
  "com.google.android.gms" % "play-services-analytics" % playServicesVersion ::
  "com.google.android.gms" % "play-services-gcm" % playServicesVersion ::


// 开启 Scala 混淆
proguardScala in Android := true

// 开启 Android 混淆
useProguard in Android := true

// 设置混淆规则
proguardOptions in Android ++= Seq(
  "-ignorewarnings",
  "-keep class scala.Dynamic")
```


project/plugins.sbt文件是项目中构建工具使用到的插件
**project/plugins.sbt**
```
addSbtPlugin("org.scala-android" % "sbt-android" % "1.7.2")
addSbtPlugin("com.timushev.sbt" % "sbt-updates" % "0.1.10")
addSbtPlugin("net.virtual-void" % "sbt-dependency-graph" % "0.8.2")
```











```

```