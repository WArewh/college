# 数据降维
用尽量少的损失，将特征减少，但不缺失信息，可以加快训练速度

## 主成分分析
输出是一个低维平面，这个平面使数据的投影误差最小即
$$
min\  \frac{1}{m}\sum_{i=1}^{m}\Vert x^{(i)} - x^{(i)}_{approx\ } \Vert^2 \ \ x^{(i)}_{approx\ }为x^{(i)}在低维平面的投影
$$

## 选择K
K最小满足以下条件
$$
\frac{
    \frac{1}{m}\sum_{i=1}^{m}\Vert x^{(i)} - x^{(i)}_{approx} \Vert^2
    }
    {
        \frac{1}{m}\sum_{i=1}^{m}\Vert x^{(i)}\vert^2
    } <= p 
$$  
如果使用SVD则可以，使用S矩阵变为以下条件
$$
\frac{
    {\sum_{i=1}^{k}}S_{ii}}
    {\sum_{i=1}^{m}S_{ii}}
    <= p 
$$
p一般取0.01或0.05，表明1-p的方差被保留了（可以理解为精度）


## 推导
1. 投影误差最小可以转化为最大方差，见[这篇文章](https://www.zhihu.com/question/41120789/answer/474222214) ，转化为 $max\  \frac{1}{m}\sum_{i=1}^{m}( x^{(i)} - u )^2$，对x进行中心化（$a_i=x^{(i)}-u$）处理，转化为$max\ \frac{1}{m}\sum_{i=1}^{m}a_i^2 $  
2. 这个公式只是适合二维到一维，N维到K维见[这篇文章](http://blog.codinglabs.org/articles/pca-tutorial.html)，我们从中得到优化目标：是选择K个单位正交基，使得原始数据变换到这组基上后，各字段两两间协方差为0，而字段的方差则尽可能大  
3. $C=\frac{1}{m}XX^T$ ，则C是一个对称矩阵，其对角线分别个各个字段的方差，而第i行j列和j行i列元素相同，表示i和j两个字段的协方差，那么对C进行对角化，对角元素按从大到小依次排列，前K个对角元素对应的单位特征向量我们所需要的矩阵$P$

### 从线性自动编码器上理解
自动编码器，具体见[神经网络](neural_network.md)
平方错误的自动编码器
$$
E _ { \mathrm { in } } ( \mathbf { h } ) = \frac { 1 } { N } \sum _ { n = 1 } ^ { N } \left\| \mathbf { x } _ { n } - \mathrm { WW } ^ { T } \mathbf { x } _ { n } \right\| ^ { 2 } \text { W为 } d \times \tilde { d } \text { 矩阵 }
$$

进行$\mathrm { WW } ^ { T } = \mathrm { V } \Gamma \mathrm { V } ^ { T }$，$\mathrm {I}=V \mathrm {I} { V } ^ { T }$正交变换得到

$$
\min _ { \mathbf { V } } \min _ {  \Gamma } \frac { 1 } { N } \sum _ { n = 1 } ^ { N } \| \underbrace { \operatorname { VIV } ^ { T } \mathbf { x } _ { n } } _ { \mathbf { x } _ { n } } - \underbrace { \operatorname { V } \Gamma \mathbf { V } ^ { T } \mathbf { x } _ { n } } _ { \mathbf { W } \mathbf { W } ^ { \top } \mathbf { x } _ { n } } \| ^ { 2 }
$$

先优化$\Gamma$，将V当作常量得到

$$
\min _ { \mathbf { V } } \min _ { \Gamma } \frac { 1 } { N } \sum _ { n = 1 } ^ { N } \|\mathbf {V} \left(  \mathrm {I} - \Gamma  \right)  {\mathbf { V } ^ { T } \mathbf { x } _ { n } } \| ^ { 2 }
$$
要想最小化，那么$\Gamma$就要尽可能与I相同，但$rank(W)\le\tilde{d}$，那么可以得到最小化时$\ \  \mathrm { I }-\Gamma = \left[ \begin{array} { c c } 0 & 0 \\ 0 & \mathbf { I } _ { d - \tilde { d } } \end{array} \right]$，那么可以得到
$$
\min_ { \mathbf { V } } \sum _ { n = 1 } ^ { N } \left\| \left[ \begin{array} { c c } 0 & 0 \\ 0 & \mathbf { I } _ { d - \tilde { d } } \end{array} \right] \mathbf { V } ^ { T } \mathbf { x } _ { n } \right\| ^ { 2 }
$$
可以转化为
$$\max_{ \mathbf { V } } \sum _ { n = 1 } ^ { N } \left\| \left[ \begin{array} { c c } \mathbf { I } _ { \tilde { d } } & 0 \\ 0 & 0 \end{array} \right] \mathbf { V } ^ { T } \mathbf { x } _ { n } \right\| ^ { 2 }
$$
得到
$$
\max _ { \mathbf { v } } \sum _ { n = 1 } ^ { N } \mathbf { v } ^ { T } \mathbf { x } _ { n } \mathbf { x } _ { n } ^ { T } \mathbf { v } \text { subject to } \mathbf { v } ^ { T } \mathbf { v } = 1
$$
使用拉格朗日乘数法得到
$$
\sum _ { n = 1 } ^ { N } \mathbf { x } _ { n } \mathbf { x } _ { n } ^ { T } \mathbf { v } = \lambda \mathbf { v }
$$
最大化时，V应该是$X ^ { T } X$的最大特征向量  

线性自动编码器做的事投影到这些与数据 $x_{n}$ 最匹配的几个正交向量，投影后，保证它们的和最大。这和PCA是基本一致