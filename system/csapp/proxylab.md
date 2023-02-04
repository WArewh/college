# proxylab
代理主要实现以下这几件事：
- 接受用户连接
- 解析请求
- 查找缓存，查找是否存在用户需要的数据
  - 存在
    - 直接返回缓存中的数据
  - 不存在
    - 请求转发到web服务器
    - 读取服务器的响应
    - 转发到相应的客户端并缓存

![proxy](https://pic4.zhimg.com/80/v2-2db61d5d2b3db2613cb7405ea91cc2d7_720w.webp)

## 网络编程

### socket
![socket](https://pic1.zhimg.com/80/v2-1a60390222bfa3f55fc2c70de31dff48_720w.webp)

echo服务器：客户端发送数据，服务端接收数据不做处理并发送数据给客户端，客户端接收数据并输出到stdout
![socket_interface](https://pic1.zhimg.com/80/v2-d09f6f47c89ebebb6bea76b2c01ac32c_720w.webp)

- socket函数：客户端和服务器使用 socket函数来创建一个套接字描述符，可用getaddrinfo来为socket提供参数
- bind函数：告诉内核将addr中的服务器套接字地址和套接字描述符sock_fd联系起来
- listen函数：将socket_fd从一个主动套接字（默认）转化为一个监听套接字，用来接受来自客户端的连接请求
- accept函数：等待来自客户端的连接请求到达侦听描述符listen_fd，返回一个fd，可用Unix I/O函数与客户端通信
- connect函数：与套接字地址为addr的服务器建立一个因特网连接，可用getaddrinfo来为connect提供参数

## 并发编程

### 基于进程

- 优点：
  - 由于进程具有自己独立的虚拟内存空间，所以无需担心被其他进程覆盖
- 缺点：
  - 共享状态信息较困难，必须使用IPC机制

### 基于事件
I/O多路复用是并发事件驱动程序的基础，先检查多个描述符是否准备好数据，然后再对其进行读取

- 优点：
  - 共享数据容易
  - 很容易调试，类似于顺序执行
  - 不需要上下文切换
- 缺点：
  - 编码复杂
  - 不能充分利用多核处理器。

### 基于线程
- 优点：
  - 易于在线程之间共享数据结构
  - 比进程更高效
  - 同一个进程内的线程共用一个文件描述符表
- 缺点：
  - 难以控制调度
  - 不容易调试，发生错误难以复现

#### 线程
线程共享：进程的整个虚拟地址空间，包括代码、数据、堆、共享库和打开的文件  
线程私有：线程ID、所有寄存器、栈

### HTTP

#### HTTP请求报文格式  

![format](https://www.runoob.com/wp-content/uploads/2013/11/2012072810301161.png)

## Part I: Implementing a sequential web proxy
目的：实现一个处理 HTTP/1.0 GET请求的基本顺序web代理

方法：仿照tiny server实现网络通信并更改处理函数。处理函数完成以下任务：
- 解析url
- 生成http请求报文
- 给终端服务器发送报文
- 接收响应报文
- 给客户端发送响应报文

## Part II: Dealing with multiple concurrent requests
目的：采用预线程化的技术处理客户端请求

方法：这个场景可以抽象出生产者和消费者模型，如下图所示：
![pre-threading](https://pic3.zhimg.com/80/v2-c53d48a2489d0fa299c88998755645b6_720w.webp)


## Part III: Caching web objects

目的：把访问过的对象缓存下来，使用LRU替换

方法：这个场景可以抽象出读者优先的读者和写者模型，因此实现一个读者写者锁完成

问题：测试脚本过于简单，只是查看有没有完成缓存功能，因此本实现也没有采取LRU策略而是FIFO
