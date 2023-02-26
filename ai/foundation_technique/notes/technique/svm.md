# 支持向量机
SVM算法输出一个最优化的分隔超平面，适合中小型数据样本、非线性、高维的分类问题

![支持向量机](https://images2018.cnblogs.com/blog/1355387/201808/1355387-20180803125024936-432373019.png)


## 间隔
d = $\frac{\vert w^Tx+b \vert}{\Vert w \Vert}$，其中$ \Vert w \Vert = \sqrt[]{w^2_1+...w^2_{n-1}} $

## 支持向量
支持向量就是可以用来确定平面的点，是所有点中到平面的最小间隔的那几个点

## 硬间隔SVM
硬间隔是指数据可以被分类准确即数据线性可分，误差为0  
硬间隔SVM有d+1个变量，N个限制，如果数据不够就很难求解，因此适合特征少，数据多的情况

### 求解
SVM求解就是$y(w^Tx+b)>0\ $，$max\ y*d_{min}$，可以转换为以下式子具体见[台大的机器学习技法](https://www.bilibili.com/video/BV1ix411i7yp?p=3)
$$
 y(w^Tx+b)\ge1\ \\
\min_{w} \ \frac{1}{2}\Vert w \Vert^2 
$$

### 对偶问题
SVM的对偶，有N个变量，N+1个限制，因此适合数据少的情况，但没有完全避开d（X进行特征转换的维度Z的空间维度）,如果d较大，计算内积将是比较麻烦的事情，由此引出[核函数](kernel.md)  
$$
\min_{\alpha} \frac{1}{2} \alpha^T Q \alpha - e^T \alpha\\
{s.t}\ \  y^T \alpha = 0\\
\alpha_i\ \geq 0
$$
求解具体见[台大的机器学习技法](https://www.bilibili.com/video/BV1ix411i7yp?p=6) 

### 联系
SVM可被视为一种正则化模型

![SVM与正则化](https://upload-images.jianshu.io/upload_images/8016875-5c9036d3bb3119fd.png?imageMogr2/auto-orient/strip|imageView2/2/w/938/format/webp)

SVM可以理解为L2正则化的逻辑回归

![错误衡量](https://upload-images.jianshu.io/upload_images/8016875-0ab36ffdd0121a93.png?imageMogr2/auto-orient/strip|imageView2/2/w/955/format/webp)


## 软间隔SVM（SVC）
软间隔SVM不执着于将数据严格分开，而是寻找较低的复杂度的模型来降低过拟合的危险，因此可以将pocket算法和硬间隔SVM结合，同时使用$\xi$表示错误程度，$\xi$越大表示离边界越远，使用C表示注重哪方面，C越大，越注重分类正确，C越小，越注重找一个比较宽的边界
$$
\min_ {w, b,\xi} \frac{1}{2}w^Tw+C\sum^{N}_{n=1}\xi_n \\
s.t：y_n(w^Tz_n+b)\ge1-\xi_n，\xi_n\ge0
$$
可以转换为无约束形式软间隔SVM（LinearSVC）
$$
\min_ {w, b} \frac{1}{2} w^T w + C \sum_{i=1}\max(0, 1 - y_i (w^T \phi(x_i) + b)),
$$

### 对偶问题
以下式子为SVC对偶问题
$$
\min_{\alpha} \frac{1}{2} \alpha^T Q \alpha - e^T \alpha\\
s.t\ \  y^T \alpha = 0\\
0 \leq \alpha_i \leq C
$$

具体见[台大的机器学习技法](https://www.bilibili.com/video/BV1ix411i7yp?p=15)

### 选择合适参数
- 交叉验证，选取验证误差最小的模型
- 支撑向量个数，过滤掉支撑向量占比过大的模型($E_{loocv} <= \frac{支撑向量个数}{资料数量}$)

## 概率SVM
概率SVM融合SVM和逻辑回归各自的优势，可以得到SVM在Z空间的逻辑回归的近似解
$$
\underset{A,B}{min}\frac{1}{N}\sum^{N}_{n=1}log
\Biggl(1+exp
    \biggl(-y_n
        \Bigl(
            A\cdot\bigl(w^T_{svm}\phi(x_n)+b_{svm}\bigr)+B
        \Bigr)
    \biggr)
\Biggr)
$$
上述模型分为两阶段学习：
1. 做SVM，结果作为转换，将数据转换到1维空间
2. 做1维空间内的简单的逻辑回归问题

## 支撑向量回归SVR
[LLSVM](kernel.md)用作分类，得出的边界相似，但会有更多支撑向量（$\beta$稠密），预测较慢，需要稀疏解来加快预测速度

### ε不敏感误差
设置$\varepsilon>0$，$error = max(0,\vert s-y\vert-\epsilon)$，$\vert s-y\vert$为到平面距离，这个错误也叫做$\epsilon$不敏感误差 ，相比平方错误，距离较小错误基本一样，距离较大比平方错误收到的影响更小，具体见[台大的机器学习技法](https://www.bilibili.com/video/BV1ix411i7yp?p=23)
$$
\min_ {w, b, \zeta, \zeta^*} \frac{1}{2} w^T w + C \sum_{i=1}^{n} (\zeta_i + \zeta_i^*)\\{s.t} \  y_i - w^T \phi (x_i) - b \leq \varepsilon + \zeta_i,\\
w^T \phi (x_i) + b - y_i \leq \varepsilon + \zeta_i^*,\\
\zeta_i, \zeta_i^* \geq 0
$$
有d+1+2N个变量，4N个限制，此外同样可以转换到无约束形式（LinearSVR）
$$
\min_ {w, b} \frac{1}{2} w^T w + C \sum^{N}_{i=1}\max(0, |y_i - (w^T \phi(x_i) + b)| - \varepsilon)
$$

### 对偶问题
$$
\min_{\alpha, \alpha^*} \frac{1}{2} (\alpha - \alpha^*)^T Q (\alpha - \alpha^*) + \varepsilon e^T (\alpha + \alpha^*) - y^T (\alpha - \alpha^*)\\
s.t\ \  e^T (\alpha - \alpha^*) = 0\\ 0 \leq \alpha_i, \alpha_i^* \leq C
$$

这种模型为SVR，求解具体见[台大的机器学习技法](https://www.bilibili.com/video/BV1ix411i7yp?p=24)，在tube之外均为支撑向量，相比之前就变稀疏了，有2N个变量，4N+1个限制

