---
title: List简介
date: 2016-11-21 14:05
tags:
- 技术
- Java
---

# List简介
### List 四种实现类
1. ArrayList
2. LinkeList
3. Vector
4. Stack

### 四种List的数据结构

1. ArrayList
   动态数组，初始化分配一定长度的数组

2. LinkeList
   双向链表

3. Vector
   与 ArrayList 一样使用动态数组作为存储结构

4. Stack
   Stack 继承 Vector ，不同的点是 Stack 是栈而不是队列，实现先进后出

### 四种List的不同使用场景的效率

四种 List 实现其实根据数据结构可以分为两类，ArrayList，Vector，Stack 都是动态数组划分为一类，后面一ArrayList作为代表作比较分析。另一类就用是双向链表(包含当前的值和前节点和后节点e)实现 LinkedList。

根据链表和数组的比较，链表在插入，删除操作效率更高，但是随机读取效率相比数组就比较低。
相反的，插入或删除一个数据就需要更长的时间，因为被修改位置后续的坐标全都要后移一位，所以耗时较长。

源码中可以看出，LinkedList 寻找的 index 大于List 长度的一半时，则会从后面开始读取数据
而数组的 List 直接根据下标返回所需的元素


### ArrayList 与 Vector 关于现场安全的比较

ArrayList 非现成安全，Vector 线程安全，所以在对单线程中使用 ArrayList 的效率要高于 
Vector


### ArrayList 的遍历速度比较
随机范围的效率最高
随机访问 > for循环 > 遍历器


