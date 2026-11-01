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

## 配置与版本边界补充

BswM ActionList 不是可在配置里调用任意 C 函数的通用脚本引擎。它执行 AUTOSAR 规范和供应商实现所支持的 Action 类型，例如模式切换、通信/路由相关动作、调用已定义的 BSW 请求接口等；具体 Action 类型和参数由所用 Release、BSW 模块集成及 DaVinci/EB 工具版本决定。

因此，不能把示例中的 PduR、CanIf、NvM API 当成所有项目都能直接放入 ActionList 的通用清单。应在工具的 BswM Action 类型列表、生成代码和模块 SWS 中确认支持范围，并检查动作执行顺序、条件反复触发、立即/延迟执行和失败处理。