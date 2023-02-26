# 提取模型
让机器自动提取特征提取和特征转换

## 神经网络
神经网络的隐藏层可以理解为是对资料特征的提取

## 反向传播
链式法则

### 优化
神经网络的$d_{vc}$约等于神经元的数量乘以权重的数量，可以通过以下方法进行优化：  
1. 随机化权重且权重不易过大，因为S型函数在权值较大梯度近似为0
2. 使用weight-elimination regularizer（$\sum{}{}\frac{(w^{(l)}_{ij}\ \ )^2\ }{1\ +\ (w^{(l)}_{ij}\ \ )^2\ }$），以同等程度的缩小，可以得到稀疏解
3. 迭代次数越多，给模型寻找最优值更多的可能性，这会使得模型更加复杂，迭代次数减少，可以让模型复杂度减少
4. 加入一些杂讯，让神经网络学到更为具有代表性的特征

### 深度学习
|深度学习面临的挑战|迎接该挑战的相关技术|
|----------------|-------------------|
|难以训练|小批量 GPU|
|复杂的结构|CNN、RNN等|
|模型复杂度高|大数据 正则化 dropout denoising|
|优化困难|预训练|

## 自动编码器
这种$d−\tilde{d}−d$的输出数据本身的神经网络叫做自编码器，这种网络的意义在于获得样本数据中的隐藏结构，通常来说，要限制两边的权重一致，以此来正则化，可以用来做预训练

![自动编码器](https://img-blog.csdn.net/20180318211750732)

对于监督学习，这种网络目的在于得到合理的特征转换，获得原数据的不同表示形式  
对于无监督学习，这种网络可以目的在于学习数据的类型表示，比如异常检测中，如果误差很大就说明有异常  
如果$\tilde{d}\ <\ d$，那么就可达到数据压缩的效果

## RBFN

RBFN将任意一点到中心点的距离作为特征转换，表达一种相似性，如果距离越近就表示越相近，因此可以完成分类或聚类任务

$$
h ( \mathbf { x } )  = \text { Output } \left( \sum _ { m = 1 } ^ { M } \beta _ { m } \operatorname { RBF } \left( \mathbf { x } , \mu _ { m } \right) + b \right)
$$

![RBFN](https://img-blog.csdnimg.cn/20200501113836456.png)

RBF做分类  
1. RBF一般选择的是高斯函数。
2. Output（输出）选择sign做为二分类输出。
3. M则是支持向量的个数。
4. $μ_m$ 则是支持向量$x_m$。
5. $β_m$ 则是通过SVM Dual问题求解$α_m$与$y_m$的乘积。

### Full RBFN
把每个点都是中心点，这样的话一个新来的点都会受到以前资料点的投票表决，离新来的的点越近的所持有的票数越大，这样的网络就做Full RBFN  

Full RBFN可以达到在训练集上不犯错，但这也意味可能过拟合，因此需要正则化，比如L2或者选取一些代表的点计算，选取一些代表的点可以得到K最近邻和K均值算法

![Full_RBFN](https://img-blog.csdn.net/20180324222931840)

#### K最近邻
由于高斯函数衰减的很快，这就导致了距离新来的点最近的那个点会有比较大的权重，如果只选最接近K个较大值作为依据，这样的算法就是k最近邻算法，具体算法见[聚类](cluster.md)  

#### K均值
由于μ是一个集群的中心点，因此能够代表一定范围内的点也就是一个群内的点，所以可以找K个集群中心点进行预测，具体算法见[聚类](cluster.md)  


## 矩阵分解
跳过