---
title: 算法学习笔记 - Alogrithm Fourth Edition
date: 2016-11-21T12:18:13+08:00
draft: true
tags:
- 技术
- 算法
---

## 排序算法

#### 选择排序(Selection)
如果有N个数组，从第一个元素开始往后选择，与后面的每一个元素做对比，挑出最小的元素，如果后面元素中有一个最小的值，则把这个值放到第一位。然后从第二位数开始，继续往后面的元素做对比，挑出最小元素，如果后面元素中有一个最小的值，则把这个值放到第二位。以此重复操作到第N位，排序就完成了。
```
public class Selection {
	Selection() {

	}

	public static void main(String[] args) {
		int[] a = new int[] { 1, 2, 5, 7, 9, 12, 93, 5, 4, 6, 88 };
		show(a);
		Selection.sort(a);
		show(a);
	}

	public static void sort(int[] a) {
		for (int i = 0; i < a.length; i++) {
			int mini = i;
			for (int j = i + 1; j < a.length; j++) {
				if (less(a[j], a[mini])) {
					mini = j;
				}
			}
			exch(a, i, mini);
		}
	}

	private static boolean less(int v, int w) {
		return v < w;
	}

	private static void exch(int[] a, int i, int j) {
		Object swap = a[i];
		a[i] = a[j];
		a[j] = (int) swap;
	}

	private static void show(int[] a) {
		for (int i = 0; i < a.length; i++) {
			System.out.print(a[i] + " ");
		}
		System.out.println();
	}
}

```

#### 插入排序
假设有N个元素的数组，从第二元素开始，与左边的第一元素比较，如果第二个比第一个元素小则插入第一个前面。接着从第三个开始与左边元素与第二个比较，如果第三个小于第二个，则插入到第二个前面，接着比较第一个。以此类推。
```
package com.srs.test;

public class Insert {
	Insert() {
	}

	public static void main(String[] args) {
		int[] a = new int[] { 1, 2, 5, 7, 9, 12, 93, 5, 4, 6, 88 };
		show(a);
		Selection.sort(a);
		show(a);
	}

	private void sort(int[] a) {
		for (int i = 1; i < a.length; i++) {
			for(int j = i;j>0&&less(a,j,j-1);j--){
				exch(a,j,j-1);
			}
		}
	}
	
	private boolean less(int[] a,int i,int j){
		return a[i]<a[j];
	}
	
	private static void exch(int[] a, int i, int j) {
		Object swap = a[i];
		a[i] = a[j];
		a[j] = (int) swap;
	}
	
	private static void show(int[] a) {
		for (int i = 0; i < a.length; i++) {
			System.out.print(a[i] + " ");
		}
		System.out.println();
	}
}
```

#### 希尔排序
插入排序在极端情况下有可能最右端的数值要经过其他全部数值的比较才到达第一位。所以当数组长度很大时，排序的效率就非常低了，后来便有了希尔排序，希尔排序是插入排序的优化，它的基础原理思想就是，将数组分成几个小队列，让数组元素跨数组排列。当分组排列完成后，缩小组别的长度，重复上面的排序，直至最后做普通的插入排序即完成了希尔排序；
- 例如，假设有这样一组数[ 13 14 94 33 82 25 59 94 65 23 45 27 73 25 39 10 ]，如果我们以步长为5开始进行排序，我们可以通过将这列表放在有5列的表中来更好地描述算法，这样他们就应该看起来是这样：
> 13 14 94 33 82   
> 25 59 94 65 23  
> 45 27 73 25 39  
> 10

然后我们对每列进行排序：

> 10 14 73 25 23  
> 13 27 94 33 39  
> 25 59 94 65 82  
> 45

将上述四行数字，依序接在一起时我们得到：[ 10 14 73 25 23 13 27 94 33 39 25 59 94 65 82 45 ].这时10已经移至正确位置了，然后再以3为步长进行排序：
> 10 14 73  
> 25 23 13  
> 27 94 33  
> 39 25 59  
> 94 65 82  
> 45

排序之后变为：
>10 14 13  
>25 23 33  
>27 25 59  
>39 65 73  
>45 94 82  
>94

最后以1步长进行排序（此时就是简单的插入排序了）。

代码如下：
```
public class Shell extends BaseClass {
	public static void main(String[] args) {
		startTest(new Shell());
	}

	@Override
	public void sort(int[] a) {
		int n = a.length;
		int h = 1;
		while (h < n / 3)
			h = 3 * h + 1;
		while (h >= 1) {
			for (int i = h; i < n; i++) {
				for (int j = i - h; j >= 0 && less(a, j + h, j); j -= h) {
					exch(a, j + h, j);
				}
			}
			h /= 3;
		}
	}
}

```

#### 归并排序
分治是归并排序的基本思想，将一数组通过不断的分化，直至最小，元素数量为2的小数组，小数组排序后再和其他小数组合并合并的时候也做排序，合并完成后再与另外一组同样有小数组再继续合并，指导最终排序完成
```
public class Merge extends BaseClass {
	public static void main(String[] args) {
		startTest(new Merge());
	}

	@Override
	public void sort(int[] a) {
		sort(a,0,a.length-1);
	}

	public void sort(int[] a, int lo, int hi) {
		if (hi <= lo)
			return;
		int mid = lo+(hi - lo) / 2;
		sort(a, lo, mid);
		sort(a, mid + 1, hi);
		merge(a, lo, mid, hi);
	}

	public void merge(int[] a, int lo, int mid, int hi) {
		int i = lo, j = mid + 1;
		int[] arr = new int[a.length];
		for (int k = lo; k <= hi; k++) {
			arr[k] = a[k];
		}
		for (int k = lo; k <= hi; k++) {
			if (i > mid) {
				a[k] = arr[j++];
			} else if (j > hi) {
				a[k] = arr[i++];
			} else if (less(arr[j], arr[i])) {
				a[k] = arr[j++];
			} else {
				a[k] = arr[i++];
			}
		}

	}

}
```

#### 快速排序
快速排序使用分治法（Divide and conquer）策略来把一个序列（list）分为两个子序列（sub-lists）。选取一个基准值，程序同时从左端和右端向中间靠拢，首先左端和右端同基准值做比较，左端小于基准值时光标继续移动，直至左端大于基准值，右端的大于基准值时光标继续移动，直至右端小于基准值，这时候交换左端右端位置。接着继续移动左右端光标重复以上操作。当两端相遇时完成左右端大小归类。然后继续分裂左右端归类后的数组，数组不能再继续分裂排序就完成了

```
public class Quick extends BaseClass {
	public static void main(String[] args) {
		startTest(new Quick());
	}
	
	@Override
	public void sort(int[] a) {
		sort(a,0,a.length-1);
	}

	public void sort(int[] a, int lo, int hi) {
		if (lo >= hi) {
			return;
		}
		int j = partition(a, lo, hi);
		sort(a, lo, j-1);
		sort(a, j + 1, hi);
	}

	private int partition(int[] a, int lo, int hi) {
		int i = lo, j = hi + 1;
		int v = a[lo];
		while (true) {

			while (less(a[++i], v)) {
				if (i == hi) {
					break;
				}
			}

			while (less(v, a[--j])) {
				if (j == lo) {
					break;
				}
			}

			if (i >= j) {
				break;
			}

			exch(a, i, j);
		}
		exch(a, lo, j);
		return j;
	}
}

```

## 优先队列

### 堆的定义
> 当一棵二叉树的每一个结点都大于等于它的两个子节点是，它被称为有序堆

