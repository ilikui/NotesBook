---
title: AUTOSAR 1000问 · SWC类型Q4 Runnable 怎么配、怎么挂到 Task 上？
tags:
  - AUTOSAR
  - 1000问
---

# AUTOSAR 1000问 · SWC类型Q4：Runnable 怎么配、怎么挂到 Task 上？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjYxMzU2MjA5

**AUTOSAR 1000问 · SWC类型Q4：Runnable 怎么配、怎么挂到 Task 上？**

▎ 五大学习法：费曼——把 Runnable 映射讲成「这段代码挂在哪个时隙上跑」

**费曼（一句话本质）**：Runnable 是 SWC 里一段可被调度的函数；把它映射到 Task，就是决定这段代码挂在哪个确定的执行时隙上。Task 管「什么时候跑」，Runnable 管「跑什么」。

**SQ3R（去哪找）**

- Runnable 本体 + 触发事件：DaVinci Developer，跟 SWC 一起定义
- 挂到哪个 Task：DaVinci Configurator 的 RTE 视图，做 Runnable-to-Task 映射
- 触发事件与 Task 的对应关系，就在这个映射里定

**麦肯锡金字塔（三组对应，MECE）**

1. 触发事件决定挂哪种 Task：TimingEvent（周期）→ 周期 Task；DataReceivedEvent（收到数据）→ 主周期 Task 或专用 Task；OperationInvokedEvent（被调用）→ 由调用方所在 Task 执行；InitEvent → 初始化阶段
2. 周期要对齐：TimingEvent 的周期得是 Task 周期的整数倍，Task 跑不出比它更快的节奏
3. 一个 Runnable 只能挂一个 Task；一个 Task 可装多个 Runnable，同 Task 内多个 Runnable 的执行顺序由配置决定

**西蒙（流程五步）**：Developer 里定义 Runnable + 触发事件 → 导出 ARXML → Configurator 导入并做 SWC→ECU 映射 → RTE 里逐个挂到目标 Task（配周期/偏移）→ Validate → Generate，最后翻生成的 Rte.c 和 SchM 确认调用接对了

**几个常见的坑**

- TimingEvent 周期和 Task 周期对不上（Task 10ms，Runnable 写 7ms），校验直接报错
- DataReceivedEvent 的 Runnable 挂错 Task，数据处理时机和延迟就变了
- 一个 Runnable 想挂多个 Task 会报错，只能拆成多个 Runnable
- 只改了 Developer 没在 Configurator 重新映射，两边不同步，生成出来还是旧映射
- 同一个 Task 里多个 Runnable 别依赖声明顺序，执行顺序看配置

📎 上一题 SWC类型Q3（如何配置 SWC）→ [https://v.flomoapp.com/mine/?memo\_id=MjYxMzU1MTQ3](https://v.flomoapp.com/mine/?memo_id=MjYxMzU1MTQ3)

📎 AUTOSAR 1000问总表 → [https://v.flomoapp.com/mine/?memo\_id=MjMxMTQ2NDk4](https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4)

#Area/技术/AUTOSAR