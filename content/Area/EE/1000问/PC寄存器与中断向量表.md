---
title: ①<u><mark>PC(Program Counter)</mark></u>:CPU内一定会有的寄存器，不同CPU可能会用不同的名字，如IP(Instruction Pointer);是用来记 录下一个指令的地址。当CPU执行完一个指令后，PC值会自动累加，此外，某些指令（如JUMP）就是通过改变PC的值来改变CPU的执行顺序。
tags:
  - 嵌入式
  - 处理器基础
---

# ①<u><mark>PC(Program Counter)</mark></u>:CPU内一定会有的寄存器，不同CPU可能会用不同的名字，如IP(Instruction Pointer);是用来记 录下一个指令的地址。当CPU执行完一个指令后，PC值会自动累加，此外，某些指令（如JUMP）就是通过改变PC的值来改变CPU的执行顺序。

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MTM1MDIwMjg2

①<u><mark>PC(Program Counter)</mark></u>:CPU内一定会有的寄存器，不同CPU可能会用不同的名字，如IP(Instruction Pointer);是用来记 录下一个指令的地址。当CPU执行完一个指令后，PC值会自动累加，此外，某些指令（如JUMP）就是通过改变PC的值来改变CPU的执行顺序。

②<u><mark>中断矢量表（Interrupt Vector Table）</mark></u>：计算机系统通过中断（Interupt）来处理突发事件，例如，键盘被按下或计时器到时

等。通常CPU（或CPU+中断处理器）可以处理许多中断来源，所以程序员必须指定当某个中断发生时，要让CPU去执行哪一个函数，而记录这些设定的表格就叫做中断矢量表。

#Area/技术/嵌入式