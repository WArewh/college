# Lab: page tables

## XV6

### 页表
![page_table](https://906337931-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MKKjB2an4WcuUmOlE__%2F-MKPwJezGQDkWaLDRuDs%2Fimage.png?alt=media&token=654cbddc-fab3-4180-8bd7-d275c63ae67f)

### 内存映射

![mem_map](https://906337931-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MK_UbCc81Y4Idzn55t8%2F-MKaY9xY8MaH5XTiwuBm%2Fimage.png?alt=media&token=3adbe628-da78-472f-8e7b-3d0b1d3177b5)

- Guard page的PTE中Valid标志位未设置，会导致立即触发page fault

## Speed up system calls

概述：通过在用户空间和内核之间的只读区域共享数据加速特定的系统调用，执行这些系统调用可以不再进入内核。  
要求：将地址 **USYSCALL** 映射为只读页。在该页的起始处，存储一个 struct usyscall，设为当前进程的pid。    

思路：
1. 在proc结构体中添加usyscall结构体，修改allocproc、freeproc、proc_pagetable、proc_freepagetable函数
2. allocproc、freepro的作用是分配和释放物理页，proc_pagetable、proc_freepagetable的作用是建立和解除页表映射。


## Print a page table

要求：根据进程的 p->pagetable 按照特定格式打印出该进程的页表。

思路：仿照freewalk即可。

## Detect which pages have been accessed

要求：给定一个用户页表地址开始，搜索所有被访问过的页并返回一个bitmask来显示这些页是否被访问过。

思路：遍历传入的页，使用walk函数找到页表项，根据页表项判断PTE_A是否为1，为1则对应bit置一并清零，最后copyout写回。