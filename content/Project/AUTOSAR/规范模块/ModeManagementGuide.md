---
title: ModeManagementGuide
tags:
  - Project
  - AUTOSAR
  - CP
---

`ModeManagementGuide` 是 CP 解释性指南（EXP），系统讲解 AUTOSAR **模式管理（Mode Management）**：模式是什么、模式切换如何实现、模式管理器（Mode Manager）与模式使用者（Mode User）各自的角色，以及应用模式管理（Application Mode）与基础软件模式管理（BSW Mode）之间的关系。

> [!info] 一句话定位
> CP 里「谁在什么条件下切到什么状态」的统一答案，BswM 是其中的中枢。

## 规范信息

| 项目 | 内容 |
| --- | --- |
| 平台 | CP |
| 类别 | EXP — 解释性指南（Explanation） |
| UID | 440 |
| 版本 | R25-11 |
| 本地 PDF | `AUTOSAR_CP_EXP_ModeManagementGuide.pdf` |
| 纯文本全文 | `CP_EXP_ModeManagementGuide.complete.txt` |

## 知识体系

```mermaid
flowchart TD
    A["模式管理"] --> B["基本概念"]
    A --> C["应用模式管理"]
    A --> D["BSW 模式管理"]

    B --> B1["Mode 与 ModeDeclaration"]
    B --> B2["模式请求与仲裁"]
    B --> B3["Mode Manager / Mode User 角色"]

    C --> C1["SwcModeManager"]
    C --> C2["模式切换通知"]

    D --> D1["BswM 规则与动作列表"]
    D --> D2["EcuM 状态仲裁"]
    D --> D3["ComM / 通信模式"]
```

## 核心要点

- **基本概念**：模式（Mode）是系统状态的一种抽象；模式切换通过模式管理器下发、模式使用者响应；文档用一套示例 ECU 的代码配置串讲全流程。
- **应用与 BSW 的联动**：应用模式管理（Application Mode）与基础软件模式管理紧密相关，应用侧的模式请求会驱动 BSW 侧动作。
- **BswM 是中枢**：BSW Mode Manager 是 R4.0 起的核心模式管理模块，可高度配置——用**规则（Rule）**评估条件、用**动作列表（Action List）**执行结果，配置方法是本指南的重点。
- **未覆盖的后续工作**：网关 ECU、FlexRay / Ethernet / LIN 的通信管理、DCM 路由路径组、多核 BswM 配置等在文档中列为待补充项。

## 依赖关系

- 依赖 [[BSWModeManager]]（BswM，规则与动作）、[[ECUStateManager]]（EcuM，状态仲裁）、[[COMManager]]（ComM，通信模式）。
- 应用侧模式经 [[RTE]] 传递。

## 相关

- [[BSWDistributionGuide]]
- [[BSWModeManager]]
- [[ECUStateManager]]
- [[COMManager]]
- [[CP]]
- [[规范模块]]


---

# 工程问答补全：模式管理如何落到 ECU 项目

以下按 Classic Platform 的典型架构解释。具体 API、容器、模式组、通知机制与可用功能以项目所采用的 AUTOSAR Release、模块 SWS 和供应商实现为准。

## Q1. Mode、ModeDeclaration、ModeDeclarationGroup 和 ModeRequestType 分别是什么？

**答案：** Mode 是系统或组件可处于的一种离散状态，例如 STARTUP、RUN、POST_RUN、SLEEP。ModeDeclaration 是模型中声明的具体模式；多个相关模式通常组织在 ModeDeclarationGroup 中；模式请求则表达某个参与者希望系统或模式组进入某个状态。不要把“模式声明”“模式请求”和“模式切换完成通知”混为一谈。

工程上要同时检查：
- 模式组允许的模式集合及初始模式；
- 请求者是否具有请求权限，是否存在冲突请求；
- 模式管理器如何仲裁多个请求；
- 使用者何时收到切换通知，以及何时完成本地动作。

## Q2. Mode Manager 和 Mode User 的职责如何划分？

**答案：** Mode Manager 负责接收请求、执行策略/仲裁并发布当前模式；Mode User 订阅或接收模式变化，并据此启停功能、改变通信行为或调整资源状态。一个 ECU 中可以存在多个不同范围的模式管理者，不应默认所有模式都由单个 BswM 统一控制。

## Q3. Application Mode 与 BSW Mode 有什么区别？

**答案：** Application Mode 面向应用功能行为，例如舒适模式、驾驶模式或功能启用状态；BSW Mode 面向基础软件服务状态，例如通信允许、网络唤醒、诊断会话或 ECU 启停阶段。两者可通过 RTE 模式接口、BSW 模式通知及项目定义的协调逻辑关联，但语义和责任边界不同。

**典型链路：**

```mermaid
sequenceDiagram
  participant SWC as 应用SWC
  participant RTE as RTE
  participant MM as 应用Mode Manager
  participant BswM as BswM
  participant BSW as ComM/EcuM/其他BSW
  SWC->>RTE: 请求应用模式
  RTE->>MM: 传递模式请求
  MM->>MM: 仲裁并更新模式
  MM-->>RTE: 模式切换通知
  RTE-->>SWC: 通知Mode User
  BswM->>BswM: 评估BSW模式/事件规则
  BswM->>BSW: 执行动作列表
```

此图表示一种常见协作关系，不意味着所有项目都必须采用 SWC 直接触发 BswM 的单一路径。

## Q4. BswM Rule、Logical Expression 和 Action List 如何协作？

**答案：** BswM 将模式请求、状态变化或其他配置输入映射为规则评估；规则中的逻辑表达式判断条件是否满足；规则结果触发配置的动作列表。动作列表可执行模式切换相关的 BSW 服务调用，具体动作类型和执行限制依赖所用规范版本及实现。

设计时应明确：
1. 输入信号来自哪个模块、何时更新；
2. 规则是周期评估还是事件触发；
3. 多条规则同时成立时的优先级和仲裁；
4. Action List 的执行顺序、可重入性与错误处理；
5. 是否存在动作反向触发原规则的循环；
6. 初始化阶段输入尚未有效时采用什么默认策略。

## Q5. EcuM、BswM、ComM 在启动、运行和休眠时如何配合？

**答案：** EcuM 管理 ECU 生命周期和唤醒/关机流程；BswM 根据模式和请求执行配置的 BSW 协调动作；ComM 管理通信通道的通信模式请求与限制。常见流程是唤醒源触发启动，EcuM 推进初始化状态，BswM 协调通信及其他服务，ComM 根据用户请求和总线策略管理通信；关机时则先完成用户释放、通信降级、存储写入和关机条件检查，再进入低功耗状态。

不要把 EcuM 状态、ComM 通信模式和应用功能模式当作同一个状态机。它们之间需要显式的请求、通知和时序约束。

## Q6. 如何分析多网络 ECU 的模式管理？

**答案：** 将模式管理按作用域拆分：ECU 全局状态、网络/通道状态、应用功能状态和诊断状态。CAN、LIN、FlexRay、Ethernet 等网络各自具有不同的通信管理和唤醒语义。排查时逐个追踪“请求来源 → 仲裁模块 → 目标模式 → 动作列表 → 网络状态反馈”，不要仅凭某条总线处于 Full Communication 就推断 ECU 所有网络均已进入相同状态。

## Q7. DCM Routing Path Group 与模式管理有什么关系？

**答案：** 诊断路由路径组用于控制诊断请求可通过哪些路由路径或目标。模式管理可根据 ECU 状态、诊断会话或网络可用性协调路由启停，但路由路径组本身不是 ECU 模式，也不能替代 DCM 的诊断协议处理。应分别验证诊断会话状态、路由路径配置、目标可达性和通信通道状态。

## Q8. 如何验证模式管理没有死锁、抖动或错误唤醒？

**答案：** 建立模式转换表和时序测试矩阵，至少覆盖正常启动、快速重复请求、多个用户冲突、网络唤醒、诊断唤醒、通信超时、低电压复位、存储写入失败、休眠取消和异常复位。记录请求、仲裁结果、规则变化、动作执行、通知时间戳及最终状态。对每条转换定义超时、失败回退和可恢复条件。

## 模式管理调试闭环

```mermaid
flowchart TD
  A[复现模式异常] --> B[记录请求源与时间戳]
  B --> C[检查Mode Group与请求值]
  C --> D[检查Manager仲裁]
  D --> E[检查BswM Rule结果]
  E --> F[检查Action List执行及返回值]
  F --> G[检查Mode User通知与响应]
  G --> H[核对EcuM/ComM/DCM最终状态]
  H --> I[增加边界时序与故障注入回归]
```

## 工程交付检查清单

- [ ] 每个模式组都有定义、初始值、合法转换和责任方。
- [ ] 请求者、仲裁者、使用者及其接口关系清晰。
- [ ] BswM 规则覆盖正常、异常、并发和初始化输入。
- [ ] Action List 不存在循环触发、无界等待或未处理失败。
- [ ] ECU、网络、应用、诊断各状态机的边界明确。
- [ ] 启动、关机、唤醒、休眠取消和异常复位均有测试证据。
- [ ] 生成配置、代码、运行日志与需求基线可追溯。
