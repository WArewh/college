# 介绍
Go是一门编译型语言（静态语言），Go语言提供的工具都通过一个单独的命令go进行调用，比如：go run、go build等。  
Go语言最有意思并且最新奇的特性就是对并发编程的支持。

## 不同点

### 分配方式
编译器会自动选择在栈上还是在堆上分配局部变量的存储空间，如果一个变量逃逸了，就会声明在堆中，没有则在栈里。


### 包 
go通过包（模块）组织源代码，实现命名空间的管理，每个go程序开头需要写上自己属于那一个包，一般地，同一目录下的同级的所有go文件应该属于同一个包，并且包名和目录名应该一致。  

- 一个go程序只有一个main函数，它是入口函数，必须属于main包
- 包不可依赖传递，支持匿名导入```import _ package```（这样做的原因是导入包会计算包级变量的初始化表达式和执行导入包的init初始化函数）
- go1.11以后引入了[官方包管理工具](https://blog.csdn.net/weixin_39003229/article/details/97638573)

### 常规变量声明
```
var 变量名字 类型 = 表达式
```
类型省略，自动推导
表达式省略，默认为“0”值

### 简短变量声明
主要用于声明和初始化局部变量，注意不要多次声明，具体形式如下
```
名字 := 表达式
```
var形式的声明语句往往是用于需要显式指定变量类型的地方，或者因为变量稍后会被重新赋值而初始值无关紧要的地方。

### 函数声明

```
func name(parameter-list) (result-list) {
    body
}
```
实参都是通过值的方式传递，但如果实参包括引用类型，如指针，slice(切片)、map、function、channel等类型，里面的数据结构可能被间接修改。  
如果遇到没有函数体的函数声明，这表示该函数不是以Go实现的。这样的声明定义了函数签名。  

#### 匿名函数
```
func squares() func() int {
    var x int
    return func() int {
        x++
        return x * x
    }
}
```

### 赋值
不支持++i，i++表示i=i+1

### 循环语句
```
for i := 0; i < 5 ;i++{

}
```
都可省略

### string
可以使用``表示原生字符串，不会进行转义
rune类型是用来区分字符值和整数值，类型等价于int32，常用来处理unicode或utf-8字符


### iota常量生成器
用于生成一组以相似规则初始化的常量，但是不用每行都写一遍初始化表达式。itoa初始为0，比如设置flag时可以这样做。


### new、make
new函数只接受一个参数，这个参数是一个类型，并且返回一个指向该类型内存地址的指针，用到的时候比较少。
make也是用于内存分配的，但是和new不同，它只用于chan、map以及slice的内存创建，它返回的类型就是这三个类型本身，因为这三种类型是引用类型。

### slice、map
slice、map比较需要通过循环，但可以直接和nil进行比较。

### 结构体
Go语言可以让一个命名的结构体包含另一个匿名的结构体类型，这样就可以简单的点运算符x.f来访问匿名成员链中嵌套的x.d.e.f成员。

### 面对对象
Go语言中没有类这一概念
- 使用结构体进行封装
- 使用作用在接收者上的函数实现方法，包括get、set方法
- 通过字母大小写来控制可见性（大写对外可见，小写对外不可见）
- 通过嵌入结构体实现扩展类
- 通过接口实现多态，函数中返回值或参数类型为接口，返回实现接口的结构体(指针)，以此实现多态

### 泛型
go暂不支持泛型，但有空接口(interface{})。它是不包含任何的方法的接口，可以认为所有的类型都实现了空接口，因此空接口可以存储任意类型的数值，以此实现泛型

### switch
可以使用fallthrough强制执行后面的一个case语句

#### 方法
```
func (recv receiver_type) methodName(parameter_list) (return_value_list) {
    body
}
```
其中，receiver_type是一个结构体类型，通过recv.methodName调用

#### 接口
```
type interface_name interface {
    func
}
```

### 类型断言
```
x.(Type)
```
通过类型断言可以进行条件分支

### defer
具体见[这篇文章](https://www.jianshu.com/p/79c029c0bd58)


### 测试
go test命令是一个按照一定的约定和组织来测试代码的程序。以_test.go为后缀名的源文件在执行go build时不会被构建成包的一部分，它们是go test测试的一部分。  
```
//测试函数的名字必须以Test开头，可选的后缀名必须以大写字母开头
func TestName(t *testing.T) {
    // ...
}
```
具体使用方法见[这篇文章](http://c.biancheng.net/view/124.html)  
在go中，比较常见的是表格驱动测试，这个方法使用匿名结构体，把数据和逻辑处理完全分离的测试方法

#### 基准测试
通过```go test -bench=```运行，bench后接正则表达式
```
//测试函数的名字必须以Benchmark开头，可选的后缀名必须以大写字母开头
func BenchmarkName(t *testing.B) {
    // ...
}
```
比较常见的方法是比较不同次数下运行时间，以此来确定如何优化，比如，io缓存
```
func benchmark(b *testing.B, size int) { /* ... */ }
func Benchmark10(b *testing.B)         { benchmark(b, 10) }
func Benchmark100(b *testing.B)        { benchmark(b, 100) }
func Benchmark1000(b *testing.B)       { benchmark(b, 1000) }
```
#### 剖析
可以使用```go tool pprof```命令可以对程序进行剖析或者pprof的[图像显示工具](http://www.graphviz.org)

