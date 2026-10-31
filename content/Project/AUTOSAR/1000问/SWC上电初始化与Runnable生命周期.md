---
title: SW-C 生命周期与状态管理 Q1：一个 Application SW-C 从 ECU 上电到正常运行的生命周期？开始/停止执行 Runnable 是由谁控制的？
tags:
  - AUTOSAR
  - 1000问
---

# SW-C 生命周期与状态管理 Q1：一个 Application SW-C 从 ECU 上电到正常运行的生命周期？开始/停止执行 Runnable 是由谁控制的？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1MjU0NTgx

SW-C 生命周期与状态管理 Q1：一个 Application SW-C 从 ECU 上电到正常运行的生命周期？开始/停止执行 Runnable 是由谁控制的？

答：生命周期节点由外部模块（EcuM / BswM / RTE 调度）管理，SW-C 自身是被动实体，不控制自己的生命周期。

从上电到正常运行：

1. 上电 / 复位：MCU 启动 → MCAL 初始化 → EcuM 的 Startup Sequence 逐个 Init 各 BSW 模块。

2. BSW 就绪：RTE 初始化、COM / PduR / CanIf / Can 等通信栈就绪。

3. Runnable 开始被调度：RTE 根据 EcuM / BswM 触发的模式，把 SW-C 的 runnable 放进可调度状态（通过 OS 任务 / Schedule Table 激活）。SW-C 不「主动开始」，是被 RTE 调用。

4. 正常运行：runnable 按触发事件（TimingEvent / DataReceivedEvent / OperationInvokedEvent）被周期或事件驱动执行。


开始 / 停止由谁决定：

- 何时开始执行：由 RTE 调度（触发事件）+ 当前模式状态（EcuM 进入 RUN、BswM 切换通信模式）决定。
- 何时停止：ECU 进入 Shutdown / 休眠时，相关 runnable 停止被调度；EcuM 状态机进入 PostRun / Shutdown 时，应用 runnable 被关闭。

但 SW-C 有「感知」模式的手段：通过 RTE 的 Mode 接口（Rte\_Mode / Rte\_ModeSwitch）获知 EcuM / BswM 切换的模式，从而在 runnable 内部做适应。这属于对模式变化的感知，不等于自主控制生命周期。

一句话：SW-C 是被动实体，执行调度和启动/停止由 RTE / EcuM / BswM 管；它只能通过 Mode 接口感知外部模式、在 runnable 内部适配，不能控制自己何时开始/停止。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU1MjU0NDky><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR