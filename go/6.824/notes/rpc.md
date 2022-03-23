# RPC
远程过程调用（Remote Procedure Call）一般用来实现部署在不同机器上的系统之间的方法调用，就像调用本地服务一样调用远程服务。

![RPC](https://mmbiz.qpic.cn/mmbiz_png/sXFqMxQoVLH0NGpJwroLMHm63WnquZ2sFyOzhTdDXqTsKS2DVnotRy9XFhkfumTr3icPWaIyfBVfvgCID6aRwpQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)


## 所用技术

### 序列化和反序列化
序列化就是将对象转换为标准类型消息，比如，json、xml等，也可以跳过编码直接转为二进制，反序列化就是序列化的反过程。
但我也发现网上对序列化的定义是对象转换为二进制流，序列化包含编码。

### 编码解码
编码就是将标准类型消息转换为二进制流，比如json转为ascii码或utf-8序列，解码就是编码的反过程。

### 反射
简单来说，反射就是运行时知道自己的类型和方法，比如在工厂方法中创建实例或者printf时，如果没有反射就需要创建多个if语句判断对象的类型。

## 简单实现
在具体实现中，一般存在一个注册中心，这样做是让服务器和客户端解耦，具体为：
1. 服务端启动后，向注册中心发送注册消息，注册中心得知该服务已经启动，处于可用状态。一般来说，服务端还需要定期向注册中心发送心跳，证明自己还活着。
2. 客户端向注册中心询问，当前哪天服务是可用的，注册中心将可用的服务列表返回客户端。
3. 客户端根据注册中心得到的服务列表，选择其中一个发起调用。

![simple impl](https://geektutu.com/post/geerpc-day7/registry.jpg)

