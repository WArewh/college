# 逻辑回归
服从伯努利分布
## 模型
$
sigmoid:\ h_{\theta}(x) = \frac{1}{1+exp(-\theta^{T}x)}
$

## 代价函数
$$
cost(x,y) = -\big( ylog(h_{\theta}(x))+(1-y)log(1-h_{\theta}(x)) \big) \\

J(\theta) = \frac{1}{n}\sum_{i=1}^{n}cost(x^{(i)},y^{(i)})

$$
这个损失函数也称为[交叉熵](../foundation/statistics.md)

如果y=1为正类，y=-1为负类，则可以写成以下形式

$$
cost(x,y) = -log(1+exp(-y\theta^Tx))
$$

## 理解

### 概率角度
$y=p^x(1-p)^{1-x}$，使用MLE得到交叉熵

### 指数族角度
[指数族角度](../foundation/statistics.md)可以看这篇文章



