---
title: CEM 软件结构：DTC、DID、NvM、接口配置与通信栈
tags:
  - CEM
  - AUTOSAR
  - 软件架构
  - 诊断
  - 存储
---

# CEM 软件结构：DTC、DID、NvM、接口配置与通信栈

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MTIyNjM5NjMx

> 本页把原始“待研究问题”转化为可执行的架构学习与排查说明。CEM 在不同 OEM/项目中可能代表不同的中央电子模块或功能域；以下以 AUTOSAR Classic ECU 的典型分层为参照。实际模块、容器、接口和工具操作必须以项目 ARXML、软件需求、接口矩阵、网络矩阵、供应商配置手册和生成代码为准。

## 1. CEM 软件总体结构

~~~~mermaid
flowchart TB
  APP[应用层：SWC / Runnable]
  RTE[RTE：Port / Interface / Event]
  BSW[基础软件 BSW]
  DIAG[诊断：Dcm / Dem]
  COM[通信：ComM / CanSM / COM / PduR / CanIf / CanTp]
  MEM[存储：NvM / MemIf / Fee or Ea / Fls or Eep]
  OS[OS / EcuM / BswM / WdgM]
  HW[MCU / CAN收发器 / Flash / EEPROM / 外设]
  APP <--> RTE
  RTE <--> BSW
  BSW --> DIAG
  BSW --> COM
  BSW --> MEM
  BSW --> OS
  DIAG --> MEM
  COM --> HW
  MEM --> HW
  OS --> HW
~~~~

## 2. DTC 是怎样实现的？

DTC（Diagnostic Trouble Code）用于表示已识别的故障事件。典型链路：

~~~~mermaid
flowchart LR
  A[SWC / BSW监测逻辑] -->|事件状态| B[Dem]
  B --> C[防抖与使能条件]
  C --> D[Event / DTC状态管理]
  D --> E[FreezeFrame / ExtendedData]
  D --> F[NvM持久化]
  G[诊断仪] -->|UDS 0x19| H[Dcm]
  H --> B
  H --> I[诊断响应]
~~~~

关键概念：

- **Event**：软件监测点上报的故障事件，通常通过 Dem 接口报告。
- **Debounce**：计数器或时间防抖，避免瞬态噪声立即确认为故障。
- **Operation Cycle / Enable Condition**：限定监测何时有效，影响故障确认和老化。
- **DTC Status**：反映 testFailed、pending、confirmed、testNotCompleted 等状态位；位语义应对照项目采用的 UDS/AUTOSAR 版本。
- **FreezeFrame / ExtendedData**：保存故障发生时的环境数据或扩展信息。
- **NvM**：用于保存需要跨掉电保留的诊断数据，具体保存策略受 Dem/NvM 配置影响。

排查 DTC 不出现时，按顺序检查监测条件、EventId、事件上报、Debounce、OperationCycle、EnableCondition、DTC 映射、存储条件和诊断会话/权限。不要只检查 Dcm 的 0x19 响应。

## 3. DID 是怎样读取的？

DID（Data Identifier）是 UDS 中用于标识诊断数据记录的编号。典型读取过程：

1. 诊断仪发送 UDS ReadDataByIdentifier（0x22）和一个或多个 DID。
2. Dcm 检查会话、安全等级、长度、访问权限和数据条件。
3. Dcm 按 DID 配置读取静态数据、RTE 数据或调用项目定义的读数据回调。
4. Dcm 返回正响应 0x62、DID 和数据记录；条件不满足时返回相应 NRC。

DID 的数据来源并非都来自 Dem：DID 可以读取 ECU 软件版本、VIN、标定信息、运行状态、测量值等。DTC 与 DID 是不同的诊断对象，不能混为一谈。

## 4. NvM 从应用到非易失存储的链路是什么？

~~~~mermaid
flowchart TB
  A[SWC / BSW User] --> B[NvM]
  B --> C[MemIf]
  C --> D[Fee]
  C --> E[Ea]
  D --> F[Fls]
  E --> G[Eep]
  F --> H[Flash]
  G --> I[EEPROM]
~~~~

- **NvM**：管理逻辑块、RAM Block、ROM 默认值、CRC、冗余/数据集及异步请求。
- **MemIf**：统一上层对 Fee/Ea 的访问接口。
- **Fee**：在 Flash 上模拟 EEPROM，涉及块管理、垃圾回收和擦写策略。
- **Ea**：EEPROM 抽象层。
- **Fls/Eep**：底层 Flash/EEPROM 驱动。

写入调用返回“请求已接受”不等于数据已经可靠落盘。应继续检查 NvM 请求结果、作业状态、MainFunction 调度、Fee/Fls 状态、CRC、掉电时间预算、块配置和恢复默认值行为。验证需覆盖正常关机、突然掉电、写入中断电、重复写入、数据损坏和版本迁移。

## 5. 接口配置如何从需求走到 RTE/代码？

接口配置必须建立从需求到实现的追踪关系：

~~~~mermaid
flowchart TD
  A[系统需求 / 接口矩阵] --> B[数据类型与约束]
  B --> C[Sender-Receiver / Client-Server Interface]
  C --> D[SWC Port：P-Port / R-Port]
  D --> E[Runnable / Event / Data Access]
  E --> F[SWC到ECU部署]
  F --> G[Runnable到OS Task映射]
  G --> H[RTE生成 / 编译]
  H --> I{是否跨ECU通信}
  I -->|是| J[COM / PduR / CanIf等网络映射]
  I -->|否| K[本地RTE通信]
  J --> L[集成与台架验证]
  K --> L
~~~~

逐项检查信号方向、数据类型、单位、范围、初始值、无效值、超时、队列/非队列语义、Runnable 触发方式、Task 映射、跨 ECU 路由、端序和缩放。生成后必须检查 RTE API、生成报告、编译结果和映射文件，不能只凭工具 GUI 显示“无错误”判断配置正确。

## 6. 通信协议栈如何分层排查？

周期信号的典型发送路径：

~~~~mermaid
flowchart LR
  A[SWC] --> B[RTE]
  B --> C[COM]
  C --> D[PduR]
  D --> E[CanIf]
  E --> F[Can Driver]
  F --> G[CAN Controller / Transceiver]
  G --> H[CAN Bus]
~~~~

接收方向反向流动。诊断多帧传输通常还涉及 CanTp 与 Dcm，网络管理则涉及 ComM、CanSM、Nm 等模块。按层排查：

1. **应用/RTE**：Runnable 是否执行，数据值和 API 返回值是否正确。
2. **COM**：信号映射、发送模式、周期、更新位、超时、端序、缩放和无效值。
3. **PduR**：源/目标 PDU、路由方向、ID 映射和路由组状态。
4. **CanIf/Can**：Controller、HTH/HRH、Mailbox、波特率、过滤器、错误状态。
5. **Transceiver/物理层**：供电、Standby/Enable、终端电阻、线束、差分波形、ACK、错误帧和 BusOff。
6. **接收应用**：超时监控、Invalidation、通知回调和应用消费周期。

## 7. 工程问题闭环模板

每个 CEM 问题都应按以下模板补齐，避免停留在“知道模块名称”：

- **现象与需求**：发生了什么，期望行为是什么？
- **架构定位**：涉及 SWC/RTE、BSW、MCAL、硬件还是外部网络？
- **配置证据**：ARXML、工具配置、接口矩阵、网络矩阵和版本基线。
- **运行证据**：生成代码、编译日志、Trace、DTC、寄存器和波形。
- **根因分析**：区分配置错误、代码错误、时序竞争、硬件故障和需求歧义。
- **修复与回归**：给出可复现步骤、测试用例、边界条件和回归结果。

## 相关问答与资料

- [[100问/CEM工作问题清单]] —— 已展开接口配置、休眠唤醒、DTC/DID、NvM 与通信栈问题。
- [[../AUTOSAR/基础资料与分层补充]] —— AUTOSAR 分层、BSW 服务、规范阅读与历史资料。
- [[../AUTOSAR/诊断栈 Dcm Dem UDS 工程实战]]
- [[../AUTOSAR/NvM MemIf Fee Ea 非易失存储实战]]
- [[../AUTOSAR/RTE与SWC工程实现]]
- [[../AUTOSAR/通信栈工程实战与CANoe验证]]

## 项目待补证据（不是标准答案）

以下内容必须从实际 CEM 项目资料补充，不能凭空假设：
- CEM 的全称、功能边界、MCU/SoC 和 AUTOSAR Release。
- 项目使用的 Dcm/Dem/NvM/Fee/通信栈供应商及版本。
- 关键 SWC、Port、Runnable、DID、DTC、NvM Block 与网络信号映射。
- 休眠唤醒状态机、唤醒源、功耗目标和台架测量记录。
