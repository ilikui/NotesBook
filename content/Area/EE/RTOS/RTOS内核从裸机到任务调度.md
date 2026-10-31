---
title: RTOS 内核：从裸机 super-loop 到任务调度
tags:
  - RTOS
  - 嵌入式
---

# 专栏⑮·补充一：RTOS 内核——从裸机 super-loop 到任务调度

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjUxMjA1MDcx

**专栏⑮·补充一：RTOS 内核——从裸机 super-loop 到任务调度**

▎ **为什么裸机经验要升级到 RTOS**<br>
第7篇中断是裸机并发，RTOS 是系统级并发：任务调度、优先级反转、同步互斥。FreeRTOS 和 AUTOSAR OS（OSEK）是一类东西——理解 RTOS 内核，AUTOSAR OS 的 TASK/Event 就通了。

▎ **核心概念**

1. 任务（Task）：独立执行流，有自己的栈——AUTOSAR OS 里叫 TASK
2. 调度器：决定哪个任务跑——抢占式（preemptive）vs 合作式（cooperative）
3. 上下文切换：保存/恢复寄存器——代价 = 栈操作 \+ 调度时间
4. Tick：系统时基（1ms），时间片轮转（Round Robin）

▎ **任务状态机**

- Ready（就绪）→ Running（运行）→ Blocked（阻塞：等事件/延时）→ Suspended（挂起）
- 关键认知：Blocked 任务不占 CPU——RTOS 的效率来自「谁没事谁睡觉」

▎ **同步与互斥**

1. 信号量：二值（互斥/事件）vs 计数（资源池）——AUTOSAR OS 用 Event
2. 互斥量：带优先级继承——防优先级反转
3. 队列：任务间传数据——AUTOSAR OS 无标准队列，用共享内存 + 保护
4. 优先级反转：高优先级任务等低优先级任务占的资源，被中优先级插队——解法：优先级继承 / 优先级天花板（接 C语言补充三）

▎ **和看门狗的关系（预告补充四）**<br>
裸机在 main loop 喂狗；RTOS 里 idle 任务喂狗 + 任务栈高水位监控。

▎ **三个坑**

1. 优先级分配乱：所有任务都高 = 没有优先级——按 deadline 分配
2. 任务栈溢出：栈给太小——用高水位（High Water Mark）监控
3. ISR 里调用阻塞 API：死锁——ISR 只能发信号/队列（FromISR 版本）

▎ **一句话**：RTOS = 调度器 + 任务状态机 + 同步互斥三件套；任务阻塞不占 CPU、互斥量防反转、ISR 只发信号——三条理解透，AUTOSAR OS 就通了。

📎 第7篇：中断与 ISR → [https://v.flomoapp.com/mine/?memo\_id=MjUwNTg0NDc5](https://v.flomoapp.com/mine/?memo_id=MjUwNTg0NDc5)<br>
📎 C语言补充三：并发与原子性 → [https://v.flomoapp.com/mine/?memo\_id=MjUxMjA0Mjc0](https://v.flomoapp.com/mine/?memo_id=MjUxMjA0Mjc0)<br>
📎 专栏⑮导航 → [https://v.flomoapp.com/mine/?memo\_id=MjQ1NzMzNDk3](https://v.flomoapp.com/mine/?memo_id=MjQ1NzMzNDk3)

**专栏⑮进度：10/10 + 补充一**

#Area/技术/嵌入式