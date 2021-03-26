---
title: ImageView的使用笔记
date: 2016-11-28 11:20
tags:
- Android
-  技术
---

### 一、使用ImageView 的src 和background

> src ：原图大小，不被拉伸;  
> background：为Imageview的背景，根据ImageView给长宽进行拉伸；


### 二、设置Imageview的透明度

> android:src在设置ImageView的setAlpha(int alpha)时，起作用;  
> android:background在设置ImageView的setAlpha(int alpha)时，不起作用;

```
mImageView.setBackgroundDrawable(mDrawable.mutate());
mImageView.getBackground().setAlpha(100);
```

### 三、设置ImageView的前景（foreground）
有时候设计需要在ImageView 上面覆盖一层（如灰色）
> View 提供了一个setForeground(Drawable foreground)

### 四、使用ImageView的“android:adjustViewBounds”

**如果想设置图片固定大小，又想保持图片宽高比，需要如下设置：**

1. 设置setAdjustViewBounds为true；
2. 设置maxWidth、MaxHeight；
3. 设置设置layout_width和layout_height为wrap_content

### 五、正确使用ImageView的“android:scaleType”
ImageView的“android:scaleType”属性是对src才有效的

ScaleDrawable类是afc框架中提供了一个专门处理Drawable scale的类，在ImageView的ScaleType的基础上额外提供了11中裁剪方式：
```
（1）CROP_CENTER
（2）CROP_START
（3）CROP_END
（4）FIT_CENTER
（5）FIT_START
（6）FIT_END
（7）MATCH_WIDTH_TOP
（8）MATCH_WIDTH_BOTTOM
（9）MATCH_WIDTH_CENTER
（10）CENTER
（11）CROP_BY_PIVOT
```
![image](https://images.thoughtbot.com/blog-vellum-image-uploads/wDbiaqGSQyyErtXGSh6w_scaletype.png)
> 要保证ScaleDrawable.CROP_START属性设置成功，在xml中一定要设置“android:scaleType=”fitXY”



















