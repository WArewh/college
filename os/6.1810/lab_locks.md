# Lab: locks
重新设计代码以降低锁竞争，提高多核机器上系统的并行性。
锁竞争优化一般有几个思路：
- 只在必须共享的时候共享（Memory allocator）
- 必须共享时，尽量减少在关键区中停留的时间（Buffer cache）

### spinlock
- spinlock轮询的过程发生中断可能会造成死锁
- 编译器和硬件的指令重排序

### sleep&wakeup
sleep和wakeup使用于等待某事发生，用于阻塞和唤醒线程的情形

#### lost wakeup
问题：sleep和wakeup不位于同一个同步块中，会出现进程的状态还没有改变就调用了weakup，导致weakup无效  
解决：
- 类似于条件变量，在sleep添加一个参数，传入保护等待数据的锁，使得sleep和wakeup位于同一个同步块中
- semaphore

### exit
1. 关闭了所有已打开的文件
2. 唤醒wait的父进程
3. 将子进程的父进程设置为init进程
4. 将进程的状态设置为ZOMBIE，调度其他进程

### wait

1. 扫描进程表，找到父进程是自己且状态是ZOMBIE的进程
2. 调用freeproc，清理系统资源并状态设置为UNUSED

### kill

1. 设置killed为1
2. 如果进程正在SLEEPING状态，将其设置为RUNNABLE
3. 目标进程运行到内核代码中能安全停止运行的位置时，调用exit

#### init进程
init进程的工作就是在一个循环中不停调用wait。每个进程都需要对应一个wait，这样才能调用freeproc函数，并清理进程的资源。

## Memory allocator

要求：为每个CPU设置独立的freelist，减少多个CPU并发分配物理页冲突的概率

实现：设置一把大锁和多个小锁，小锁的维护freelist，大锁的防止出现导致死锁的情况（比如：A偷B、B偷A）

## Buffer cache

要求：建立哈希表，并为每个桶单独加锁，减少多个进程访问block发生冲突的概率，替换策略为LRU

实现：
- 加锁，基本Memory allocator
- bget：
  - 找自身哈希表，缓存过，修改buf并返回
  - 找自身哈希表，根据LRU找到空闲位置，修改buf并返回
  - 找其他哈希表，根据LRU找到空闲位置，将buf添加到自身哈希表中，修改buf并返回