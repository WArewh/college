# Lab1
实现简易的Mapreduce。
## 代码框架
main/mrsequential.go：本地内存中实现mapreduce的代码  
main/mrmaster.go：测试要运行的master进程，它调用mr.MakeMaster函数创建master，每一秒使用master.Done检查是否完成任务  
main/mrworker.go：测试要运行的worker进程，它调用mr.Worker函数  
mr/worker.go：需要完成Worker函数来执行map和reduce以及rpc通信  
mr/master.go：需要完成Makemaster()函数完成创建，完成Done查看任务是否完成  
mr/rpc.go：包含一个rpc通信例子并提供call函数完成rpc通信

## 测试框架
测试分多个阶段，每个阶段通过改变map和reduce函数进行检查各个功能，测试的map和reduce函数存放在mrapp中。
wc：检查单词计数  
indexer：检查单词计数并对应文件  
map parallelism：检查map是否并行  
reduce parallelism：检查reduce是否并行  
job count：检查task数量是否符合预期
early exit：检查是否存在早退
carsh：检查worker挂掉是否不受影响

### tips
我发现有点怪的地方是每一次测试都会清除本阶段的所有输出，即使本阶段错误也会清空，我觉得如果错误应该保存正确输出和自己的程序输出，不然测试错误的提示将毫无作用。  

## 实现步骤
1. 实现map、reduce操作(本地模拟测试master：local_test.go 通过)
2. 实现忽略差错通信(mr-test.sh 除了crash-test都应通过)
3. 实现处理差错通信(mr-test.sh 通过所有)

### 处理差错
- 处理worker意外挂掉的情况

### 处理差错策略
- 采用心脏检测，worker每三秒发送心跳，master十秒没收到worker的心跳就视为worker挂掉
- 每个task同一时间内只有一个进程执行，如果worker挂掉，等到master检测crash，再分配一个进程执行
- 每个worker都会产生临时文件，其文件名为(规定名字-进程号)，如果执行顺利，将会由master完成改名(去掉进程号)，其他情况则会删除临时文件

#### tips
第三点设计可以用来做backup，也可以防止worker由于网络原因或其他原因没有真的挂掉

### 问题
1. 实际上取的是v这个局部变量地址而不是arr第i个元素的地址，导致出错
```
i,v:= range arr{
    go function(&v)
}
```
2. defer并不会执行，而使用panic会执行defer，但是要在panic之前
```
defer fun()
log.Fatalf(...)
```
推荐使用下面的模式
```
func Function(){
    defer fun(){
        if err := recover(); err != nil {
            处理错误
        }
    }
    ...
    log.Panic(...)
}
```
