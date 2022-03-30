# lab2
lab2分为四部分  
1. 选举
2. 添加log
3. 持久化
4. 日志压缩

## 代码框架
labgob：在gob(go binary，将传递数据转为二进制进行传输)的基础上添加了安全性检查，比如，会对未大写的字段进行提示  
labrpc：实现了基于通道的RPC，去模拟一个可能丢失请求，丢失回复，延迟消息以及断开特定主机的网络，使用到了labgob  
raft/config.go：实现config，用来控制网络的通断、客户端节点、服务器节点的创建、删除、模拟崩溃等操作  
raft/persister.go：持久化  
raft/util.go：帮助调试的工具  

## 测试框架
raft/test_test.go:分为4个部分，分别测试不同的功能

## lab2A
实现心跳检测和leader选举
![state](https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwww.pianshen.com%2Fimages%2F747%2Fc8fc9ea2c63b350d176243e89fbee013.png&refer=http%3A%2F%2Fwww.pianshen.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1650809088&t=617f734051cfc013aca45a093d858ca0)

### 分析

| case | start_state | event | end_state |
|  --  |      -      |   -   |     -     |
|1|follower|在election timeout内收到"有效"rpc|follower|
|2|follower|election timeout内没有收到"有效"rpc|candidate|
|3|candidate|election timeout内收到"有效"rpc|follower|
|4|candidate|election timeout内没有收到"有效"rpc|candidate|
|5|candidate|election timeout内收到半数以上票数响应|leader|
|6|leader|election timeout内收到"有效"rpc|follower|

- follower的"有效"rpc：leader发送的任期大于等于自己的任期、candidate发送的任期大于等于自己的任期
- candidate的"有效"rpc：收到leader发送的任期大于等于自己的任期、收到其他candidate发送的任期大于自己的任期
- leader的"有效"rpc：收到的任期大于自己的任期

### 测试
- TestInitialElection2A，测试raft第一次选举。
- TestReElection2A：测试网络故障后进行的选举，包括如下部分
    - leader会被设置为网络故障，检测新的选举，并且要求在旧leader加入之后也不会扰乱选举
    - 如果集群人数少于一半，要求无leader被选举出来
    - 集群人数达到条件，则可以选举
    - 新节点的重新加入不应阻止leader的存在
- TestManyElections2A：开启7个节点，选出leader，再断连3个节点，然后再加入3个节点，检测是不是还是只有一个leader。

### 实现
一开始，我觉得可能这个状态维护可能很复杂，于是想着使用状态机，用管道做同步，结果，由于经验不足，写出一堆死锁，于是放弃状态机，照着给的思路进行了实现，不到一个小时就写出来。其实按照分析实现即可，不要多想。

### 问题
在并发或分布式下，使用如下代码，可能会导致随机的种子一样，由此产生活锁。
```
rand.Seed(time.Now().UnixNano())
rand.Intn(100)
```
解决方法：每一次随机种子之前随机一下,或者后台开一个随机种子routine。  
