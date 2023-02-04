# Lab: file system

## xv6

### 概况

![file system](https://906337931-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MRhzbAZwhuzp63wWdRE%2F-MRielGcbrHOzPCrxHcO%2Fimage.png?alt=media&token=f685aafe-7c22-4965-9936-d811b090023d)

### crash
采用logging解决文件系统crash有以下好处：
1. 保证文件系统的系统调用是原子性的
2. 支持快速恢复

一般分为三步：
1. 写log
2. 执行log中的操作
3. 清除log

#### 准则

write ahead rule：系统需要先将所有的写操作记录在log中，之后才能将这些写操作应用到文件系统的实际位置，这使得一系列的更新在面对crash时具备了原子性

freeing rule：从log中删除一个transaction之前，我们必须将所有log中的所有block都写到文件系统中

#### xv6
- begin_op，表明马上就对文件系统进行更新
- end_op，表明文件系统现在已经完成了所有write操作
- 在begin_op和end_op之间，所有的write block操作只会走到block cache中。当系统调用走到了end_op函数，文件系统会将修改过的block cache拷贝到log中。这使得所有写操作在面对crash时具备原子性

## Large files

目的：实现二级间接索引

方法：
- 修改索引相关的宏、inode、dinode的结构
- 修改bmap，仿照一级索引分配空间的代码实现二级索引分配。由于要写文件所以要**写log**
- 修改itrunc，仿照一级索引释放空间的代码实现二级索引释放

## Symbolic links

目的：实现符号链接

方法：
- 实现sys_symlink系统调用，调用create取创建符号链接，再调用writei把target path写到inode中
  - 由于这是对文件系统操作，因此需要begin_op和end_op
  - create会返回inode，同时也持有inode的锁
  - iunlockput来释放inode的锁以及inode计数
- 修改sys_open，查看O_NOFOLLOW标志，如果没有设置该标志位就要递归查询到非符号链接，有环则报错
  - O_NOFOLLOW，如果参数pathname是符号连接, 则会令打开文件失败
- 递归查询到非符号链接
  - 使用数组存储符号链接路径的inum
  - 使用readi和namei找到链接的inode
  - 判断是否为非符号链接
  - 判断是否有环