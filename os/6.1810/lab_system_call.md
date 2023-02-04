# Lab: System calls

## System call tracing

要求：实现trace系统调用

实现：按照提示即可完成。首先使得sys_trace可以运行，而后在proc结构体中加入trace_mask，然后在syscall函数中实现追踪，最后在fork函数复制trace_mask。

## Sysinfo

要求：实现Sysinfo系统调用

实现：通过free_list得到空闲空间的大小，通过遍历proc数组得到正在运行的进程数量，最后通过copyout复制sysinfo。