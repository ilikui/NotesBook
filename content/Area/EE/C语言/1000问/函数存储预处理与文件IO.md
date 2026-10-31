---
title: C语言1000问：函数、存储类、预处理器与文件I/O
tags:
  - C语言
  - 1000问
  - 嵌入式
---

# C语言1000问：函数、存储类、预处理器与文件I/O

本篇迁移 C 语言 1000 问第二批 10 张完整问答卡，覆盖有符号/无符号、递归、函数指针、static、字符串、宏、条件编译、union、可变参数和文件模式。

## 11. 为什么有符号整数溢出和无符号整数溢出的标准语义不同？

**答案：** 对无符号整数，算术结果按模 2^N 回绕，行为有定义；有符号整数超出可表示范围时，行为未定义（signed overflow UB）。编译器可基于有符号溢出不发生的假设进行优化。

混合比较也危险：若 usual arithmetic conversions 将负的 signed 值转换为 unsigned，负数可能变成很大的正数。避免方法是统一类型、检查转换范围、开启 -Wsign-compare/-Wconversion，并对边界做显式测试。

## 12. 递归和迭代应该怎么选？尾递归在 C 中一定省栈吗？

**答案：** 树遍历、分治和嵌套结构适合递归表达；线性遍历和深度不确定的嵌入式任务通常更适合迭代。递归会消耗调用栈，朴素递归还可能重复计算。C 标准不保证尾调用优化，不能依赖尾递归一定复用栈帧；需要可移植地控制栈深时应改用循环或显式栈。

## 13. 函数指针是什么？有哪些典型用途？

**答案：** 函数指针保存函数入口的可调用引用，类型中包含返回类型和参数类型。例如：

~~~~c
typedef int (*compare_fn)(const void *, const void *);
compare_fn cmp = my_compare;
~~~~

典型用途包括回调、qsort 比较函数、状态机跳转表、中断向量表和驱动操作表。函数指针类型必须与实际函数签名兼容；通过不兼容类型调用函数会产生未定义行为。

~~~~mermaid
flowchart TD
  A[事件 / 命令 / 状态] --> B[索引或分派表]
  B --> C[函数指针]
  C --> D[具体处理函数]
  D --> E[处理结果]
~~~~

## 14. static 修饰局部变量、全局变量和函数分别有什么效果？

**答案：**

- 块作用域局部 static：具有静态存储期，生命周期贯穿程序运行，但名称仍只在该块内可见。
- 文件作用域 static 对象：具有内部链接，只能在当前翻译单元中通过该名字访问。
- 文件作用域 static 函数：同样具有内部链接，适合实现文件私有的辅助函数。

因此 static 在不同上下文中分别涉及存储期和链接性。模块内部不需要对外暴露的状态和函数通常应限制为 static。

## 15. C 为什么没有内置字符串类型？以 NUL 结尾有什么代价？

**答案：** C 字符串通常用 char 数组保存，并以空字符 NUL（值为 0）标记结束。设计轻量、易与底层内存交互，但长度需要扫描，缓冲区边界由调用方管理，NUL 字节也不能作为字符串内部普通字符使用。

嵌入式中更稳妥的接口常采用“指针 + 显式长度 + 容量”，例如传入 buffer、buffer_size 和 data_length，避免仅靠结束符推断边界。

## 16. 带参数宏与函数有什么区别？宏有哪些常见坑？

**答案：** 宏在预处理阶段进行文本替换，没有普通函数那样的参数类型检查，参数也可能被多次求值。常见风险：

- 参数和整体表达式未加括号，优先级错误。
- 参数含 i++ 等副作用，展开后可能求值多次。
- 多语句宏在 if/else 中展开后破坏语法。

~~~~c
#define SQUARE(x) ((x) * (x))
#define SWAP(a, b) do { \
    int tmp = (a);      \
    (a) = (b);          \
    (b) = tmp;          \
} while (0)
~~~~

若不需要字符串化、token 拼接或条件编译，优先考虑 static inline 函数。

## 17. 条件编译和头文件守卫有什么作用？pragma once 是否标准？

**答案：** 条件编译通过 #if/#ifdef/#ifndef 等指令控制哪些代码进入编译，可用于平台适配、功能裁剪和调试开关。头文件守卫防止同一头文件在一个翻译单元中重复展开。经典写法为：

~~~~c
#ifndef MODULE_CONFIG_H
#define MODULE_CONFIG_H
/* declarations */
#endif
~~~~

#pragma once 是广泛支持的编译器扩展，但不是 ISO C 标准语法；include guard 更可移植。大型项目应遵循团队统一规范。

## 18. struct 和 union 的内存布局有什么本质区别？

**答案：** struct 的成员各自占据存储空间，整体大小还可能包含对齐填充；union 的成员共享同一块存储，大小至少足以容纳最大成员，并满足最大对齐要求。union 常用于节省空间的 tagged union、协议数据多视角解释和硬件寄存器映射。

**标准边界：** 读取非最后写入的 union 成员在 C 中涉及对象表示的重新解释，结果可能是实现定义的，也可能遇到无效表示；不要把它当作跨平台无风险的类型转换。需要严格可移植的位模式转换时，可考虑 memcpy 并结合目标类型表示约束。

~~~~mermaid
flowchart LR
  A[struct] --> B[成员分别存储]
  B --> C[总大小含填充]
  D[union] --> E[成员共享存储]
  E --> F[大小按最大成员与对齐确定]
~~~~

## 19. C 可变参数函数中的 va_list、va_start、va_arg、va_end 分别做什么？

**答案：** 它们定义在 stdarg.h：

- va_list：参数遍历状态。
- va_start：初始化遍历状态，定位到最后一个具名参数之后。
- va_arg：按指定类型读取下一个参数并推进状态。
- va_end：结束遍历。

可变参数函数无法自动获知参数个数和真实类型，必须依赖格式串、显式计数或终止标记。va_arg 类型必须与默认实参提升后的类型匹配；char/short 通常提升为 int，float 提升为 double。转发到 vprintf/vsnprintf 等接口时应使用 va_list 版本。

## 20. fopen 的文本模式和二进制模式有什么区别？

**答案：** 文本模式允许实现进行文本流转换，例如某些系统的换行符转换；二进制模式要求按字节序列读写，不进行文本转换。跨平台读写图片、固件镜像、协议数据和结构体序列化文件时，应使用 rb/wb 等二进制模式。文本文件则按项目约定使用文本模式或显式统一换行格式。

## 工程安全检查

- 避免有符号溢出和危险的隐式类型转换。
- 递归深度要有上界；实时路径优先评估最坏栈占用。
- 函数指针表中的每个函数签名必须一致。
- 模块私有符号使用 static，头文件只暴露接口。
- 字符串接口始终传长度/容量，优先使用有界函数。
- 宏复杂逻辑优先改成 inline 函数。
- 可变参数仅用于有明确格式/计数约定的接口。
- 二进制文件始终使用二进制模式，并检查 I/O 返回值。

## Flomo 原始来源

- C语言 1000 问导航：https://v.flomoapp.com/mine/?memo_id=MjQ1NzM0NTk5
- 有符号与无符号溢出：https://v.flomoapp.com/mine/?memo_id=MjU2NDUxMjUw
- 递归与迭代：https://v.flomoapp.com/mine/?memo_id=MjU2NDUwODMx
- 函数指针：https://v.flomoapp.com/mine/?memo_id=MjU2NDUwODk5
- static 的三种语义：https://v.flomoapp.com/mine/?memo_id=MjUyNTg3NjQ0
- C 字符串设计：https://v.flomoapp.com/mine/?memo_id=MjUyNTg4MDYx
- 宏与函数：https://v.flomoapp.com/mine/?memo_id=MjU2MzEyNjEw
- 条件编译与头文件守卫：https://v.flomoapp.com/mine/?memo_id=MjU2MzEyNjk5
- struct 与 union：https://v.flomoapp.com/mine/?memo_id=MjU2MzA5MzA3
- 可变参数：https://v.flomoapp.com/mine/?memo_id=MjU2NDUwNjI2
- 文件文本/二进制模式：https://v.flomoapp.com/mine/?memo_id=MjU2NDUwNDAx
