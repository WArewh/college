# Lab: Copy-on-Write Fork for xv6

## page fault
通过page fault可以实现的一系列虚拟内存功能包括：
- lazy allocation
- Zero Fill On Demand（.BSS）
- copy-on-write fork
- demand paging
- memory mapped files

为此需要三个重要信息：
1. 引起page fault的内存地址（STVAL）
2. 引起page fault的原因类型（SCAUSE）
3. 引起page fault的指令位置（trapframe->epc）
 
![SCAUSE](https://906337931-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MMD_TK8Ar4GqWE6xfWV%2F-MMNmVfRDZSAOKze10lZ%2Fimage.png?alt=media&token=4bbfdfa6-1491-4ab8-8248-03bd0e36a8e9)

### copy-on-write fork

概述：fork函数会复制父进程给子进程，但是子进程很多时候会执行别的任务，因此可以采用写时复制的方法优化。

数据结构：
- 页表项的第9个bit标识为一个COW页（PTE_COW）
- 一个全局数组实现页面计数

实现：
1. 修改uvmcopy把父进程的页表复制一份，把PTE_W置0、PTE_COW置1
2. 修改kinit、kalloc、kfree、uvmcopy实现页面计数
   - kinit实现页面计数锁的初始化
   - kalloc实现页面计数初始化
   - kfree实现页面计数递减以及释放
   - uvmcopy实现页面计数递增
3. 修改usertrap处理COW
   - 判断是否是非法地址（大于sz或MAXVA）、是否为有效页、是否为COW页
   - 根据页面计数分为两种情况
     - 页面计数为1，PTE_COW置1，PTE_W置0
     - 页面计数大于1，分配一个新页面并对旧页面复制，新页面PTE复制旧页面PTE，再将PTE_COW置1，PTE_W置0
4. 修改copyout，同步骤3

tips:
  1. kinit开始会调用freerange因此需要先部分页面计数先增加
  2. mappages中会判断二次map的情况，因此需要先uvmunmap
  3. 完成前两步运行cowtest，应该只会出现SCAUSE=15的错误
  4. 完成前三步运行cowtest，可以通过simple，three，不通过file
  5. fork涉及的都是用户区的内存，而copyout是内核内存拷贝到用户内存，所以需要修改