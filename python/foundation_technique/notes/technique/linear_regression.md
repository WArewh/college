# 线性回归

假设Y服从高斯分布

## 模型
$$
h_{\theta}(x) = \theta^Tx
$$

## 损失函数
$$
cost(x,y)=(\theta^Tx-y)^2 \\
J(\theta) = \frac{1}{2n}\sum_{i=1}^ncost(x^{(i)},y^{(i)})
$$

[损失函数推导](https://blog.csdn.net/saltriver/article/details/57544704)，本质是对$\theta$的极大似然估计

## 正规方程
$\theta$ = $(x^Tx)^{-1}x^Ty$，复杂度$O(d^3)$，适用于数据多、特征d较少的情况
如果$(x^Tx)^{-1}$ 不可逆，则可能有冗余的特征类型或者数据少于特征，可以使用L2正则化（岭回归）或者L1正则化（lasso回归）解决

### 数学推导
#### 无正则
将损失函数写成向量形式
$$
J(\theta) = \frac{1}{2m}\sum_{i=1}^m(\theta^Tx_i-y_i)^2 = \frac{1}{2m}\sum_{i=1}^m\left(\theta^Tx^Tx\theta-2\theta^Tx^Ty+y^Ty\right)
$$

对$\theta$求导

$$
\frac{\partial J}{\partial \theta} = \frac{1}{m}\left(x^Tx\theta-x^Ty\right)
$$

因为损失函数是一个凸函数，因此只有唯一最小点，该点梯度为0，因此$x^Tx\theta=x^Ty$，即$\theta$ = $(x^Tx)^{-1}x^Ty$

#### L2正则
同样的求解得$\theta$ = $(x^Tx+\lambda I)^{-1}x^Ty$

### 几何理解
$\theta$ = $(x^Tx)^{-1}x^Ty$，$(x^Tx)^{-1}x^T$是x的左逆矩阵，是A列空间投影的投影矩阵，因此从几何上表示为：

![几何](https://images0.cnblogs.com/blog/489652/201503/050000028527557.png)
