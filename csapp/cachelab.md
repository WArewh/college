# cachelab

## cache
![cache](https://img-blog.csdnimg.cn/276a8c4858d94eb99b8b98c90d8516ce.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA54us5bCP6Zuq,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

### cache miss
cache miss的三种原因：

- cold miss：刚刚使用Cache时Cache为空，此时必然发生cache miss。
- capacity miss：程序最经常使用的数据超过了cache的大小
- conflict miss：cache容量足够大，但是不同的数据映射到了同一组，从而造成cache line反复被替换的现象。

为了应对通常有以下几种方法：
重新排列循环次序，提高空间局部性
使用分块技术，提高时间局部性

## Part A: Writing a Cache Simulator

目的：模拟cache，替换策略为LRU

对这一部分不感兴趣且对后面的实验没有影响就从网上抄了一份代码

## Part B: Optimizing Matrix Transpose

目的：优化一个矩阵转置函数，使得cache miss尽可能少  
cache规模为：32组，直接映射，每行32字节数据，因此每个组存储8个数据
根据本机测试，数组A和数组B的地址为0x10c0c0和0x14c0c0，所以当索引相同时，A和B会映射到同一个组中。

### 32*32

- 由于一个块可以存8个数据，加载8行需要32个块，因此很自然想到按照8*8分块，miss结果为344
- 理论上，一个32x32的矩阵最少miss为128次，两个矩阵就是256次，所以还有优化的空间
- 很容易可以观察到A[0][0]和B[0][0]是冲突的，所以可以先取出A的8个元素，再赋值给B，miss结果为288
- 剩下的miss是来源于B被A覆盖了一次，如果要达到理论值可以见[这篇文章](https://zhuanlan.zhihu.com/p/79058089)

### 64*64

- 一个块可以存8个数据，而加载4行就需要32个块，尝试按照4*8分块，miss为1844，使用上面的优化手段，miss为1652
- 首先，想到的是把64x64分成4个32x32的矩阵，使用前面32x32转置函数，但是A和B的内存布局是固定的，所以此方案不可行
- 随后，分析得到B首先访问的是0-7行的0-3列，本来cache装了8个元素但只用了4个元素，后续访问也是类似的情况，所以可以从这一点入手优化。可以先按照8x8分块再按照4x4分块，让B的访问变为"块间"的顺序访问（前4行前4列、后四行前四列、前四行后四列、后四行后四列），最后miss为1180

### 61*67

- 按照8x4分块边角不做特殊处理，miss为2037
- 尝试16x4分块边角不做特殊处理，miss为1870
