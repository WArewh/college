# 核
核函数是为了避免d的影响而设计的

![核函数](https://ewr1.vultrobjects.com/imgur2/000/005/282/186_237_f48.png)

支持向量机通过某非线性变换$\phi(x)$ ，将输入空间映射到高维特征空间，如果支持向量机的求解只用到内积运算，而在低维输入空间又存在某个函数$K(x, x')=<\phi(x),\phi(x')>$，那么支持向量机就不用计算复杂的非线性变换，而由这个函数$K(x, x')$直接得到非线性变换的内积，使大大简化了计算。这样的$K(x, x')$叫核函数，比如：  
$$
\phi_2(x)=(1,x_1,x_2,...,x_d.x_1^2,x_1x_2,...,x_1x_d,x_2^2,x_2x_1,...,x_d^2)
$$
可以求得一个核函数，只需要$O(d)$的时间
$$
\phi_2(x)^T\phi_2(x')=1+x^Tx+(x^Tx')(x^Tx')
$$

## 多项式核
模型的参数不一样就会有不一样的内积，不一样的内积就会有不一样的距离，因此不同的参数可能有不一样的支撑向量
$$
K_Q(x, x') = (\zeta+\gamma x^Tx')^Q\ \ \zeta\ge0，\gamma>0
$$  

## 高斯核
实质上是以支持向量为中心的多个高斯函数的线性组合  
$$
K(x, x') = exp(-\gamma \Vert x-x'\Vert^2)\  \gamma>0
$$


## 比较
多项式：非线性、参数多比较灵活、边界比较复杂，Q很大也不容易过拟合，但K的范围比较大，难以调参，因此适合Q很小的情况    
高斯：非线性、边界更加复杂，但$\gamma$太大（方差太小）可能出现过拟合，求解速度较慢 

# 表达定理
根据表示定理，任意的L2正则化的线性模型是可以kernelized，从直观来说，W能表示成一些Z的线性组合，就会有内积就可以有核函数，具体证明见[台大的机器学习技法](https://www.bilibili.com/video/BV1ix411i7yp?p=21)

# 核函数逻辑回归
$$
\underset{w}{min}\ \frac{\lambda}{N}w^Tw+\frac{1}{N}\sum^{N}_{n=1}log(1+exp(-yw^Tx)) \\
w = \sum^{N}_{n=1}\beta_n z_n
$$

替代后

$$
\underset{w}{min}\ \frac{\lambda}{N}\sum^{N}_{n=1}\sum^{N}_{m=1}\beta_n\beta_mK(x_n,x_m)
+
\frac{1}{N}\sum^{N}_{n=1}log\Bigl(1+exp\bigl(-y_n\sum^{N}_{m=1}\beta_mK(x_n,x_m\bigl)\Bigr)
$$
- 如果把KLR当做是关于$\beta$的线性模型，那么X就转换到了一个维度为N的Z空间，包含了kernel regularizer
- 如果把KLR当做是关于w的线性模型，那么X就转换到了一个维度为$d$的Z空间，包含了L2 regularizer


# 最小二乘支持向量机
最小二乘支持向量机（LSSVM）是将Kernel应用到ridge regression中的一种方法
$$
\underset{w}{min}\ \frac{\lambda}{N}w^Tw+\frac{1}{N}\sum^{N}_{n=1}(y_n-w^Tz_n)^2 \\
w = \sum^{N}_{n=1}\beta_n z_n
$$
替换后
$$
\underset{w}{min}\ \frac{\lambda}{N}\sum^{N}_{n=1}\sum^{N}_{m=1}\beta_n\beta_mK(x_n,x_m)
+
\frac{1}{N}\sum^{N}_{n=1}\Bigl(y_n-\sum^{N}_{m=1}\beta_mK(x_n,x_m\bigl)\Bigr)^2
$$
写成向量形式
$$
\frac{\lambda}{N}\beta^TK\beta+\frac{1}{N}(\beta^TK^TK\beta-2\beta^TK^Ty+y^Ty)
$$
求导，导数为0得
$$
\beta=(\lambda I+K)^{-1}y
$$
复杂度为$O(N^3)$，因此数据少、特征多时可以使用此方法


