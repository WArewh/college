# 并发
Go语言中的并发程序可以用两种手段来实现，顺序通信进程和基于共享内存的并发。  

## goroutine
在Go语言中，每一个并发的执行单元叫作一个goroutine。新的goroutine使用用go语句来创建
```
f()    // call f(); wait for it to return
go f() // create a new goroutine that calls f(); don't wait
```
### 特点
- 以一个很小的栈开始其生命周期，一般为2KB，栈的大小会根据需要动态地伸缩
- 不需要进入内核的上下文，代价很小（协程）
- 没有ID号，这样做是防止thread-local storage被滥用

## channels
在go语言中，channels是goroutine之间的通信手段，类似于双向管道。两个相同类型的channel可以使用==运算符比较，引用相同对象则为true
```
ch = make(chan int) // ch has type 'chan int'
ch <- x             // a send statement
x = <-ch            // a receive expression in an assignment statement
<-ch                // a receive statement; result is discarded
close(ch)           // close ch
```
goroutine泄露：如果goroutine卡住，gc不会对它回收

### 不带缓存channel
基于无缓存Channels的发送和接收操作都会堵塞，除非另一端准备好，这导致两个goroutine会进行同步操作，因此被称为同步channels。  
有些消息事件并不携带额外的信息，它仅仅是用作两个goroutine之间的同步，这个时候可以使用空结构体做同步。  
可以使用range处理管道，管道被关闭，range自动停止。管道关闭，如果没有数据可以读，将永远读出0值，写则panic。
```
chan1 = make(chan int)      // unbuffered channel
chan3 = make(chan int, 3)   // buffered channel with capacity 3

for x := range chan1 {
    chan2 <- x
}
close(chan1)
```

### 单方向管道
表示一个只发送int的channel类型为```chan<- int```，表示一个只接受int的channel类型为```<-chan int```，```chan int```可隐式转换为单方向管道，反过来不行

### 带缓存管道
cap函数可查看管道容量，len函数可查看管道有效数据个数

### select
可以使用select实现多路复用，所有channel表达式都会被求值。
- 如果没有加default分支，程序可能会被阻塞，直到某个通道可以运行
- 如果多个case满足读写条件，select会随机选择一个语句执行
- nil通道会永远堵塞，select不会理会它，这个特点的使用场景是假设有多个case，有一个case不再会有数据，那么可以让它被置为nil。
- select可以用于超时或定时任务
```
select {
case <-ch1:
    // ...
case x := <-ch2:
    // ...use x...
case ch3 <- y:
    // ...
default:
    // ...
}
// 定时超时
for {
	select {
	case <- time.After(time.Second):
	    // do something per second
	case <- ch:
		return	
	}
}
```

### channel广播
channel被关闭之后，channel仍然可读，可以读取出已发送的数据，没有数据则不断读取零值，因此channel广播可以用来关闭其他goroutine

### 问题
[happens before](https://www.liuvv.com/p/6196d525.html)

## 共享内存
go里没有重入锁，有互斥锁```sync.Mutex```，读写锁```sync.RWMutex```  
go里可以使用```sync.Once```惰性初始化
go中提供竞争检查器，检查并发可能潜在的错误