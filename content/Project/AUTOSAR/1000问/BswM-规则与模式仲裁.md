---
title: BswM 模式管理深入 Q1：BswM 的「规则」在配置工具里怎么描述——if-then-else 还是状态机？
tags:
  - AUTOSAR
  - 1000问
---

# BswM 模式管理深入 Q1：BswM 的「规则」在配置工具里怎么描述——if-then-else 还是状态机？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0OTY4NDY4

BswM 模式管理深入 Q1：BswM 的「规则」在配置工具里怎么描述——if-then-else 还是状态机？

答：更接近 **if-then-else 规则引擎**，而不是状态机。

BswM 核心配置结构（都是条件-动作）：

1. 模式请求源（BswMModeRequestSource / ModeRequestPort）：谁在请求模式——如 CanNm 请求通信模式、EcuM 请求运行模式。

2. 规则（BswMRule）+ 条件（BswMCondition）：规则由若干条件组成，条件分两种：
   - Mode 条件：判断某个模式请求源的「当前值」是否等于某值（如 CanNm 变成 FULL\_COMMUNICATION）。
   - Logical 条件：用 AND / OR / NOT 组合多个条件，形成逻辑表达式。
3. 动作列表（BswMActionList）：规则命中时执行的动作序列（BswMAction）。


所以执行逻辑是：某个模式请求变化 → 把当前所有模式请求值套进 rule 的条件做求值（逻辑组合）→ 命中则执行对应 ActionList。这与「if（条件）then（动作）」一致。

为什么不是状态机：BswM 自己不维护「当前状态」来做转移。它是对任意时刻的模式请求组合做「组合逻辑求值」——条件真就执行动作、假就不执行，不依赖历史状态积累。偶尔看着像状态机，是因为模式请求值的连续变化给人一种「状态迁移」观感，但底层是条件-动作规则，不是状态跳转表。

一句话：BswM 的规则是「条件 → 动作」的 if-then 规则引擎，用条件表达式（含逻辑组合）判断、用 ActionList 触发，不是传统状态机。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0OTY4MzU0><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR