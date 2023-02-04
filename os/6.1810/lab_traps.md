# Lab: traps

## trap机制

trap：由用户程序触发用户态和内核态的切换

### 进程虚拟地址空间

![vas](https://906337931-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MKlssQnZeSx7lgksqSn%2F-MKopGK-JjubGvX84-qy%2Fimage.png?alt=media&token=0084006f-eedf-44ac-b93e-a12c936e0cc0)


#### 栈帧

![stackframe](https://pic4.zhimg.com/80/v2-d7a2b1baeaf71d7e0c2cf306d80c49d7_720w.webp)


### RISC-V寄存器

![riscv_reg](https://906337931-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MM-XjiGboAFe-3YvZfT%2F-MM0rYc4eVnR9nOesAAv%2Fimage.png?alt=media&token=f30ebac8-8dc0-4b5d-8aa7-b241a10b43b3)

SATP：储存页目录物理地址  
STVEC：储存内核中处理trap指令的起始地址  
SEPC：储存程序计数器（PC）的值  
SSRATCH：储存trapframe page的地址  
SCAUSE：描述中断原因（具体见[这篇文章](./Lab_copy_on_write_fork.md)）
STVAL：储存出错的虚拟地址  
SSTATUS：状态寄存器  
SIE：检测中断信号
SIP：记录每种中断是否能触发


### 特殊的页
- trapframe保存了系统的状态以及用户寄存器，用于恢复用户进程
- trampoline page在user page table中的映射与kernel page table中的映射是完全一样的，这样在页表切换的过程中不会发生错误

### 切换

- 保存32个用户寄存器和PC寄存器
- 进入内核态并进行页表和栈堆的切换
- 跳入具体的处理程序

### 过程

ecall -> uservec ->usertrap -> 具体处理 -> usertrapret -> userret -> sret

- ecall
  - 更新mode标志位为supervisor
  - 将程序计数器的值保存在SEPC中
  - 设置程序计数器成STVEC寄存器内的值
  - 关中断、记录中断原因（SCAUSE）

- uservec
  - 保存通用寄存器、用户栈、用户页表到trapframe
  - 设置内核栈、内核页表

- usertrap
  - 保存epc到trapframe
  - 开中断
  - 具体处理

- usertrapret
  - 关中断
  - 保存内核栈、内核页表
  - 设置SSTATUS（使得执行sret后中断打开）

- userret
  - 恢复用户页表、用户栈、通用寄存器
  - 保存trapframe地址

- sret
  - 更新mode标志位为user
  - SEPC寄存器的数值会被拷贝到PC寄存器
  - 开中断（SSTATUS设置）

## backtrace

要求：实现backtrace

实现：获得fp的值，再用PGROUNDUP函数和PGROUNDDOWN函数作为上界和下界，打印返回地址(fp - 8)并将fp设置为prev frame的值(fp - 16) 

## Alarm

要求：实现系统调用sigalarm和sigreturn

实现：自己没有独立完成，看了其他实现发现了自己的问题，具体实现[见这篇文章](https://blog.csdn.net/LostUnravel/article/details/121341055)

问题：usertrap处于核心态，页表是内核的页表，执行不了用户态的函数，需要返回用户态再执行

