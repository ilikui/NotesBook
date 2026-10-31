# 多核共享一个变量——只用 volatile 加全局变量行不行？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzcwODY4

多核共享一个变量——只用 volatile 加全局变量行不行？

结论：地址上能通，正确性上不行。volatile 只挡住「编译器优化」，挡不住硬件层的两件事：

1. 缓存一致性：两个核各有自己的 cache。核 A 改了本地 cache 的副本，核 B 还在读自己 cache 里的旧副本，volatile 不会帮你做 cache 失效 / 刷新。

2. 原子性：volatile 不提供原子操作。变量若是 32 位且跨 cache line 或没按字对齐，读写会被拆成多个总线事务，两个核同时读写就是竞态。


三个能走通的路：

A. 靠硬件 cache coherence：有些多核 SoC 的 cluster 内部有 snoop 机制（如 ARM SCU + MOESI），cluster 内共享自洽。但只覆盖 cluster 内、跨 cluster 不行；还要把变量放进共享内存区。

B. 共享内存区 + 原子操作或锁：变量放专门的核间共享段，配 spinlock 或原子指令（如 LDREX/STREX）保证互斥和原子。

C. AUTOSAR 正路是走 IOC：跨核通信交给 IOC（RTE 转发），内部统一处理拷贝 / 互斥 / 一致性与内存隔离。

最关键约束：AUTOSAR 的自由度干扰（Freedom from Interference）要求跨 OS-Application / 跨核不通过普通全局变量共享数据——那会破坏内存分区，ASIL 部署下不允许。「volatile 全局变量」顶多算调试时的权宜，量产设计应走 IOC。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzcwNzgw><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR