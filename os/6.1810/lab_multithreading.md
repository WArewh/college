# Lab: Multithreading
XV6内核共享内存并支持内核线程，一个进程有一个用户线程，一个内核线程，但是永远也不会两者同时运行，因此线程切换需要以下步骤：

1. 第一个用户线程进入到内核中，保存用户线程的状态并运行第一个用户线程的内核线程
2. 从第一个用户线程的内核线程切换到第二个用户线程的内核线程
3. 第二个用户线程的内核线程暂停自己，并恢复第二个用户线程的状态
4. 返回到第二个用户线程继续执行

线程的状态分为三部分：
- 程序计数器
- 保存变量的寄存器
  - 用户寄存器储存在trapframe中
  - 内核线程的寄存器储存在context中
- 线程自己的栈

![switch](https://img2018.cnblogs.com/blog/1521884/201811/1521884-20181110221631207-436594504.png)

## Uthread: switching between threads

要求：实现用户线程切换机制

实现：
- uthread_switch.S同swtch.S
- 在thread_schedule调用uthread_switch
- thread_create中设置ra和sp

## Using threads

要求：熟悉Linux线程，实现哈希表的并发写入和读出

实现：设置NBUCKET个锁，每个锁管理一个桶

## Barrier

要求：实现Barrier，即使得若干个线程同时到达某一点时，才可继续执行
