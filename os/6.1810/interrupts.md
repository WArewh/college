# Interrupts

## 硬件
处理器上是通过Platform Level Interrupt Control（PLIC）来处理设备中断。基本流程：
1. PLIC会通知当前有一个待处理的中断
2. 其中一个CPU核会接收中断
3. CPU核处理完中断之后，CPU会通知PLIC
4. PLIC将不再保存中断的信息

## 软件
管理设备的代码称为驱动，所有的驱动都在内核中，且大多数分为两个部分：
- 用户进程或者内核的其他部分调用的接口（write、read等）
- 对应的Interrupt handler

通常情况下，驱动中会有一些队列(buffer)，用户和设备通过这些队列进行数据的传递。而且驱动一般是通过memory mapped I/O完成的。