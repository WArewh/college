# attacklab

## 栈

![stack](https://pic2.zhimg.com/80/v2-bd5a0aa1625c4445ba33e506b91dba29_720w.webp)

call指令
- push %eip 将调用函数下一条指令地址压入栈中
- mov func_addr,%eip 将调用函数地址给eip

ret指令
- pop %eip 将调用函数下一条指令地址给eip

tips：
- 现在很多编译器开启优化后，汇编代码里很多地方就没有push ebp;mov ebp, esp;这样的操作了，它们全部被优化掉了。
- 用ebp是为了让偏移固定，更好写 + 更好读

## Part I: Code Injection Attacks
如果程序没有做缓冲区溢出安全，可以通过代码注入攻击程序。简单来说，就是通过溢出更改返回地址，让程序执行字符串中的代码。

### phase1

目的：把test中的getbuf返回地址修改为touch1

方法：
- 查看getbuf发现rsp减去0x28，并调用Gets函数后返回，Gets中也没有申请额外空间，所以编译器给getbuf分配了40字节
- getbuf没有保存ebp，所以40字节之后就是返回地址，只要把返回地址改为touch1的地址即可（注意小端序）

### phase2

目的：把test中的getbuf返回地址修改为touch2并传递一个整数，即让程序跳转到我们的注入代码，注入代码应该把cookie传递给edi然后跳转到touch2

方法：缓冲区存储注入代码，给edi赋值并eip跳转到字符串初始位置

### phase3

目的：把test中的getbuf返回地址修改为touch2并传递一个指针，

方法：基本同phase2，要注意由于hexmatch会申请栈空间，所以把字符串放在缓冲区会被覆盖，因此字符串要远离被申请空间


## Part II: Return-Oriented Programming
为了防止了代码注入攻击，我们采取了两种措施：栈随机化和栈不可执行，但这并不能阻挡我们使用ROP攻击程序。ROP简单来说，就是通过添加一些看似"无害"的函数，对其"断章取义"。这会导致寄存器和栈发生变化进而破坏程序。

### phase4
目的：使用ROP把phase2重做一遍

方法：
- 设置返回地址，使得程序执行一些指令使得rdi为cookie的值
  - 最简单的方法就是在栈中保存cookie和touch2的地址，执行popq rdi; ret（5f 90）
  - 但是没有发现类似的代码，但是有popq rax; nop; ret（58 90 c3）和mov rax, rdi; ret（48 89 c7 c3）也可以达到同样效果

### phase5
目的：使用ROP把phase3重做一遍

方法：
- 同phase4，在栈中保存cookie字符串和touch3的地址，找到一个方案可以将cookie字符串地址给rdi。由于栈随机化，只能通过偏移获得字符串地址
  - mov rsp, rax; ret
  - add 0x37, al; ret
  - mov rax, rdi; ret
  - 将字符串放到rax + 0x37的位置