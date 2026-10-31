---
title: BswM 模式管理深入 Q2：Action List 能触发哪些操作？只改模式值，还是真能调用其他 BSW 模块接口？
tags:
  - AUTOSAR
  - 1000问
---

# BswM 模式管理深入 Q2：Action List 能触发哪些操作？只改模式值，还是真能调用其他 BSW 模块接口？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0OTY4NjMw

BswM 模式管理深入 Q2：Action List 能触发哪些操作？只改模式值，还是真能调用其他 BSW 模块接口？

答：两者都能。Action List 是 BswM 执行仲裁结果的手段，既能改模式值，也能真正调用其他 BSW 模块的接口。

BswM 的 Action（BswMAction）主要类型：

1. 设置 / 修改模式值：设置自身或目标模块的模式——如把通信模式值传给 PduR、ComM、CanNm（BswMActionSetMode）。

2. 调用其他 BSW 模块接口：关键所在——Action 可配置为调用指定 BSW API，比如：
   - 切换 PduR 路由表：PduR\_SetRoutingTable。
   - 设置 CanIf 的 PDU 模式：CanIf\_SetPduMode / 控制 Can 控制器模式。
   - 触发 NvM 写、EcuM / ComM / CanNm 的相关调用。
3. 顺序执行一组动作（BswMActionBlock / 动作序列）：把多个动作串成一个列表按序执行。


运行机制：某个模式请求变化 → 规则求值命中 → 触发 ActionList → Action 可以是「改模式」也可以是「调 BSW 接口」。

补充：这些 Action 是配置时静态决定的，BswM 本身不含业务逻辑，只做「模式仲裁 + 动作分发」。动作能调哪些接口，取决于对应 BSW 模块是否注册了可被 BswM 调用的入口，以及配置里是否正确引用了目标接口。

一句话：BswM 的 Action List 不局限于改模式值，它能真正调用其他 BSW 模块接口（如 PduR\_SetRoutingTable），是「模式仲裁 → 动作分发」的引擎；但调用范围和入口都是配置时定的静态动作。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0OTY4NDY4><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR