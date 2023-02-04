# bomblab

思路：通过引爆条件进行反推

## 寄存器

![reg](https://img-blog.csdnimg.cn/a9b55f0d546d49b6879b543db35d3aa5.png)

## lab

### phase1
- 爆炸条件
  - strings_not_equal有两个参数放在edi和esi中，返回非0则爆炸。

- 拆除过程
  - 根据strings_not_equal推测，edi和esi是两个字符串的地址，当edi和esi指向的字符串内容一致时返回0。
  - edi存储的是read_line的得到的字符串指针，esi存储的是$0x402400，查看(char*)0x402400的内容即为答案

### phase2

- 爆炸条件
  - 调用read_six_numbers后，(rsp)不为1
  - eax和(rbx)的值不等

- 拆除过程
  - 根据read_six_numbers推测，应该有六个数，六个数全部正确就拆除
    - 观察到该函数调用了sscanf，因此应该存在一个字符串常量表示输入格式
    - 查看(char*)0x4025c3的内容即为输入格式
  - 测试发现(rsp)为第一个输入的值，因此第一个数为1
  - 每次循环eax倍增由此可以得出后面的序列为2 4 8 16 32

### phase3

- 爆炸条件
  - sscanf返回值小于等于1
  - 0x8(rsp)大于7
  - 0xc(rsp)和eax值不等

- 拆除过程
  - 观察到该函数调用了sscanf，查看(char*)0x4025cf的内容即为输入格式，发现需要输入两个整数
  - 分析开头的汇编发现0x8(rsp)等于rdx的值，即sscanf第三个参数，也就是输入的第一个整数
  - 同理可得，0xc(rsp)是输入的第二个整数，输入比7小的数测试，发现0x402470是跳转表的起始地址
  - 表中对应地址的指令都是eax被赋予不同的数值，然后跳转进行判断，所以第二个数应该填入eax对应的数值

### phase4

- 爆炸条件
  - sscanf返回值不等于2
  - 0x8(rsp)大于14
  - 调用fun4返回值为0且0xc(rsp)为0

- 拆除过程
  - 观察发现输入和phase3类似，0x8(rsp)为输入的第一个整数，0xc(rsp)为输入的第二个整数
  - 分析fun4，写出了伪码但是没看出来是实现什么功能，只知道第一个数不能大于14，第二个数为0，结果试了出来
  - 具体分析见[这篇文章](https://blog.csdn.net/qq_38537503/article/details/117199006)

### phase5

- 爆炸条件
  - string_length返回值不为6
  - strings_not_equal返回值不为0

- 拆除过程
  - 注意到调用string_length和string_not_equal函数，因此应该传递一个字符串与给的字符串内容相同
  - 发现有两个常量，尝试用char*打印，发现str1长度为6，str2暂时不知含义
  - 分析发现这段程序取str1低四位给str2做索引得到的str3和str1做比较，那么只需要根据映射反推出字符即可

### phase6

没做出来，可以参考上面那篇文章