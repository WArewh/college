# PLA
PLA用于解决线性可分的二分类问题，如果线性

![PLA](https://images2015.cnblogs.com/blog/578330/201612/578330-20161210102842038-1222204880.png)

# pocket
pocket算法针对线性不可分的二分类问题

![pocket](https://images2015.cnblogs.com/blog/578330/201612/578330-20161210104105913-835177747.png)

# 逻辑回归
假设Y服从伯努利分布

## 模型
$
sigmoid:\ h_{\theta}(x) = \frac{1}{1+exp(-\theta^{T}x)}
$

## 代价函数
$$
cost(x,y) = -\big( ylog(h_{\theta}(x))+(1-y)log(1-h_{\theta}(x)) \big) \\

J(\theta) = \frac{1}{n}\sum_{i=1}^{n}cost(x^{(i)},y^{(i)})

$$

如果y=1为正类，y=-1为负类，则可以写成以下形式

$$
cost(x,y) = -log(1+exp(-y\theta^Tx))
$$



## 多分类
多分类问题转化为多个二分类问题

### OVA
具体为把单一类别归为一类，其余归为另一类，那么K个类就构造出了K个二分类，但如果分类很多，每个二分类问题会变为不平衡分类  

### OVO
任意挑选两个类进行学习，忽略其他类，那么K个类就构造出了$\mathrm{C}_k^2$个二分类，对于任意一点，对所有模型进行代入，取预测最多的那个类，虽然每个模型训练量比较小，但是训练的模型比较多

# SVM
具体见[SVM](svm.md)