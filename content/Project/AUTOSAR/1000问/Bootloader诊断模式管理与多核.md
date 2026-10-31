---
title: AUTOSAR1000问：Bootloader、诊断、模式管理与多核集成
tags:
  - AUTOSAR
  - 1000问
  - Bootloader
  - UDS
  - OS
---

# AUTOSAR1000问：Bootloader、诊断、模式管理与多核集成

本篇迁移第五批 10 张 Flomo 问答卡，覆盖 Partial Networking、Bootloader 跳转与回滚、UDS DID/0x19、BswM、DaVinci Task、多核 IOC、PDU 配置排查和 SW-C 端口映射。

## 41. Partial Networking（PN）解决什么问题？

**答案：** PN 通过选择性唤醒能力，让 ECU 只对与自身相关的网络请求/报文保持唤醒，减少整车休眠时无关 ECU 被唤醒造成的静态电流消耗。

- 传统网络管理在某些拓扑/配置下会让不相关节点也被唤醒。
- PN 通过 PN 信息、收发器选择性唤醒能力和网络管理策略，让节点按配置判断是否需要保持通信。
- 实际效果依赖支持 PN 的收发器、报文设计、网络管理配置和 OEM 网络架构；不能把所有 CAN 网络都概括成“一个节点醒、全网必醒”。

## 42. Bootloader 跳转到 App 前需要做哪些检查？

**答案：** 跳转不是简单地把 PC 指向 App 入口，而是把处理器和外设状态安全地交接给 App。典型检查包括：

1. 验证 App 镜像范围、向量表、CRC/签名和版本有效性。
2. 关闭或屏蔽 Bootloader 使用的中断源，避免跳转窗口内执行旧 ISR。
3. 停止 DMA、定时器、通信控制器等正在运行的外设，并按架构要求复位/交接。
4. 将中断向量表重定位到 App。
5. 从 App 向量表读取初始栈指针和复位入口，检查地址合法。
6. 按芯片启动要求设置 MSP/栈指针、特权状态和必要寄存器。
7. 看门狗策略要明确：可以继续由 App 接管，也可在硬件允许时按安全策略重新配置；不能一概要求跳转前关闭。

~~~~mermaid
flowchart TD
  A[收到跳转请求] --> B[验证 App 镜像与签名]
  B --> C{镜像有效？}
  C -->|否| X[留在 Bootloader / 恢复模式]
  C -->|是| D[停用中断源与 DMA]
  D --> E[外设状态交接]
  E --> F[设置 VTOR / MSP / 入口地址]
  F --> G[跳转 App Reset Handler]
  G --> H[App 自检并接管系统]
~~~~

具体寄存器步骤依赖 MCU 内核和芯片手册，不能把某一 Cortex-M 的 VTOR/MSP 流程套到所有处理器。

## 43. 新固件刷写后启动失败，A/B 回滚怎样设计？

**答案：** 常见设计包含 A/B 分区、镜像有效标志、启动尝试计数、启动健康确认和失败记录。新镜像先写入非活动分区，校验通过后切换启动选择；App 在完成关键自检并稳定运行后确认升级成功。若连续启动失败或自检失败，Bootloader 可回到上一个有效镜像。

**防回滚注意：** Anti-rollback 用于阻止降级到存在已知安全漏洞的旧版本；它与“故障时回到上一个已批准版本”需要协调设计。回滚候选镜像必须满足 OEM 安全策略，不能简单把安全版本计数器倒退。

~~~~mermaid
stateDiagram-v2
  [*] --> A_Active
  A_Active --> B_Update: 下载新镜像
  B_Update --> B_Verify: 写入完成
  B_Verify --> B_Pending: 签名与完整性通过
  B_Pending --> B_Trial: 首次试启动
  B_Trial --> B_Confirmed: App 自检成功
  B_Trial --> A_Rollback: 超时 / 连续失败
  A_Rollback --> A_Active
  B_Confirmed --> [*]
~~~~

## 44. UDS 0x22 和 0x2E 中 DID 如何分配？

**答案：** DID（Data Identifier）是诊断数据项的标识符。0x22 通过 DID 读取数据，0x2E 在允许条件下写入数据。项目通常由 OEM 维护 DID 分配表，按车辆识别、软件版本、标定参数、运行状态等类别规划范围。

必须同时管理：

- 唯一性：同一诊断域内不能发生冲突。
- 语义稳定：DID 含义和数据格式变更需要版本管理。
- 访问权限：只读 DID 不应允许 0x2E 写入。
- 安全条件：敏感写操作可能要求特定 Session、安全访问和其他前置条件。

具体 DID 区间由 ISO 14229 规定的标准项与 OEM/供应商自定义范围共同组成；不能把某个项目的区间表当作全行业统一规则。

## 45. UDS 0x19 排查 DTC 时最常用哪些子功能？

**答案：** 常见诊断流程包括：

- 0x19 0x01：按状态掩码统计 DTC 数量。
- 0x19 0x02：按状态掩码报告 DTC。
- 0x19 0x04：读取指定 DTC 的 FreezeFrame/Snapshot Record（若该 DTC 配置了相应记录）。
- 0x19 0x06：读取指定 DTC 的 Extended Data Record。
- 0x19 0x0A：报告 ECU 支持的 DTC（服务支持情况依标准版本和实现）。

DTC 的状态位、快照和扩展数据由 Dem 配置和项目诊断规范决定。并非每个 DTC 都一定有完整快照或相同扩展数据记录。

## 46. BswM 如何对 ComM、EcuM 等模式请求进行仲裁？

**答案：** BswM（BSW Mode Manager）依据配置的规则评估来自 ComM、EcuM、CanNm、应用等模块的模式请求，再触发相应 Action List。典型动作可能包括切换 PDU Group、请求通信模式或通知其他 BSW 模块。

~~~~mermaid
flowchart TD
  A[ComM Communication Mode] --> D[BswM Rules]
  B[EcuM ECU Mode] --> D
  C[CanNm / Application Mode] --> D
  D --> E[条件评估与仲裁]
  E --> F[Action List]
  F --> G[PduR / Com / CanIf / EcuM 等动作]
~~~~

BswM 是规则驱动的模式协调模块，不是所有模块状态的唯一全局状态机。具体请求、规则和动作需按 ECU 配置核对。

## 47. 在 DaVinci Configurator 中新增一个 AUTOSAR OS Task，通常要配置什么？

**答案：** 新增 Task 至少要确认：

- Task 名称、类型（Basic/Extended）和优先级。
- 调度属性：可抢占/非抢占、最大激活次数等。
- 栈大小与内存保护配置。
- 所属 OS-Application、核/分区和 Autostart。
- 若为 Extended Task，配置等待/设置的 Event。
- Runnable/BSW MainFunction 到 Task 的映射及对应调度周期。

字段名和具体配置路径会随 DaVinci 版本及 OS 供应商实现变化。生成后应检查 OS 配置校验、任务入口、链接映射、栈水位和运行时调度。

## 48. AUTOSAR 多核如何工作？IOC 的作用是什么？

**答案：** AUTOSAR OS 多核系统通常通过静态核分配、核间中断、Spinlock 和 IOC 等机制实现协作。IOC（Inter-OS-Application Communication）提供跨 OS-Application 的通信服务，可用于不同核或不同 OS-Application 之间的数据交换。

- 静态任务/应用分配：配置时确定运行核和分区。
- IPI：核间中断通知另一个核发生事件。
- Spinlock：保护跨核共享资源，需控制持锁时间。
- IOC：提供受控的跨应用消息/数据通信，具体使用共享缓冲、队列或其他实现由 OS 供应商决定。

~~~~mermaid
flowchart LR
  A[Core 0 / OS-Application A] --> B[IOC Send]
  B --> C[共享通信缓冲 / OS 同步]
  C --> D[IOC Receive]
  D --> E[Core 1 / OS-Application B]
  F[Spinlock / IPI] -.保护与通知.-> C
~~~~

## 49. PDU 收发异常，配置排查应从哪里开始？

**答案：** 建议按“PDU 定义 → 信号映射 → 路由/接口 → RTE/应用 → 总线物理层”逐层检查：

1. PDU ID、长度、方向、类型和 ECU 映射。
2. COM Signal 的起始位、长度、字节序、数据类型和 I-PDU 绑定。
3. PduR 路由源/目的、CanIf Tx/Rx PDU、CAN ID 和过滤配置。
4. RTE 端口、数据元素和 Runnable 的读写映射。
5. Can 控制器状态、波特率、收发器使能和 CANoe Trace/总线波形。

先用生成配置和 ARXML 定义确认逻辑映射，再用生成代码验证工具输出，最后用 CANoe/示波器确认运行时行为。不要默认“问题一定不在硬件”或“九成都是某一层”，应以证据逐层排除。

## 50. SW-C 端口映射错误，应该先看 ARXML 还是生成代码？

**答案：** 先看 ARXML/系统模型，因为它是配置源头；生成代码用于验证配置是否按预期投影为实际实现。

- Port：检查方向（P-Port/R-Port）和类型。
- Interface：检查绑定的 Port Interface、DataElement/Operation。
- Connector：检查发送端和接收端连接是否正确。
- ECU/Composition 映射：检查组件是否部署到预期 ECU。
- 生成代码：查看 Rte_Read/Rte_Write 实际访问的缓冲区或调用路径。
- 运行时：在 RTE API 和发送端设置断点，对比值和返回状态。

手动修改生成代码通常会在下次生成时被覆盖，正确修复应回到 ARXML/配置工具，再重新生成和回归测试。

## Flomo 原始来源

- AUTOSAR 1000 问总表：https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4
- Partial Networking：https://v.flomoapp.com/mine/?memo_id=MjU0NzcwNDc5
- Bootloader 跳转检查：https://v.flomoapp.com/mine/?memo_id=MjUzNTQxMDEw
- 固件失败回滚：https://v.flomoapp.com/mine/?memo_id=MjUzNTQxMTM4
- UDS DID 分配：https://v.flomoapp.com/mine/?memo_id=MjU0MDI3ODk1
- UDS 0x19 子功能：https://v.flomoapp.com/mine/?memo_id=MjU0MDI4MDU1
- BswM 模式仲裁：https://v.flomoapp.com/mine/?memo_id=MjU0MDI2MjQz
- DaVinci 新增 Task：https://v.flomoapp.com/mine/?memo_id=MjYxMzU1MDgy
- 多核 IOC：https://v.flomoapp.com/mine/?memo_id=MjUzNTQxNTcz
- PDU 配置排查：https://v.flomoapp.com/mine/?memo_id=MjUzNzAyNjI0
- SW-C 端口映射排查：https://v.flomoapp.com/mine/?memo_id=MjUzNTQxNzc1
