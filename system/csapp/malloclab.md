# malloclab
编写一个简单的动态内存申请器，本实现采用分离链表实现动态内存申请器

## 分离链表

### 内存块结构

![block](https://pic3.zhimg.com/80/v2-192d8f524e2a61226337699d46ed736e_720w.webp)

### 合并优化

序言块和结束块：消除合并时复杂的边界条件判断
footer：header的复制，使得当前块立即找到前一块

![tricks](https://pic2.zhimg.com/80/v2-620a104a2d7a0f6183b3cfc9418e0f41_720w.webp)

### 分离适配

设置多个链表存储不同payload的内存块

![segregated](https://pic1.zhimg.com/80/v2-9c4bf602289ce7f948d2d7b1f2e39a88_720w.webp)


## lab

- 第一个链表存储0-8，第二个链表9-16，...，第十个链表2049 - 4096，第十一个链表4097 - INF
- 链表使用LIFO的顺序和首次适配