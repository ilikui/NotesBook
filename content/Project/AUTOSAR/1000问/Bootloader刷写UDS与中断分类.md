---
title: AUTOSAR1000问：Bootloader刷写、UDS到SWC与中断分类
tags:
  - AUTOSAR
  - 1000问
  - UDS
  - Bootloader
---

# AUTOSAR1000问：Bootloader刷写、UDS到SWC与中断分类

本篇迁移第七批 6 张 Flomo 问答/参考卡，补齐 UDS 刷写链路、诊断请求触发 SW-C、Session/SecurityAccess、中断 Category 1/2 和 BSW 服务分类。

## 61. UDS Bootloader 刷写从诊断会话到 Flash 写入的完整链路是什么？

**答案：** 典型 UDS on CAN 刷写流程为：

1. 0x10 02：进入 Programming Session（具体会话条件按项目定义）。
2. 0x27：执行 SecurityAccess，完成授权。
3. 可选 0x85：控制 DTC Setting；可选 0x28：控制通信。
4. 0x31：执行擦除、前置条件检查等 Routine。
5. 0x34：RequestDownload，协商地址、长度和传输参数。
6. 0x36：TransferData，分块传输数据。
7. 0x37：RequestTransferExit，结束传输。
8. 0x31：执行 CRC/签名/完整性校验和编程后检查。
9. 0x11：ECUReset，复位后 Bootloader 验证镜像并选择启动。

~~~~mermaid
sequenceDiagram
  participant T as Tester
  participant D as Dcm / Bootloader
  participant P as PduR / CanTp
  participant F as Flash Driver
  T->>D: 10 02 Programming Session
  T->>D: 27 SecurityAccess
  T->>D: 31 Erase Routine
  D->>F: 擦除目标分区
  T->>D: 34 RequestDownload
  loop 分块传输
    T->>P: 36 TransferData
    P->>D: 组包后的数据
    D->>F: 写入 Flash
  end
  T->>D: 37 TransferExit
  T->>D: 31 Checksum / Verify
  D->>F: 读回校验
  T->>D: 11 ECUReset
~~~~

Dcm 处理诊断服务与会话、安全条件；传输层处理多帧传输；具体擦写由 Bootloader 刷写逻辑与 Flash Driver 协同完成。服务顺序和例程 ID 以 OEM 诊断规范为准。

## 62. 如何让一个 UDS 诊断请求最终触发 SW-C 的 Runnable？

**答案：** 诊断报文从 CAN 到 SW-C 的典型路径是 Can → CanIf → CanTp → PduR → Dcm → RTE → SW-C。真正把诊断服务映射到 SW-C 的是 Dcm 与 RTE/Port/Interface 的配置。

常见方式：

- 0x31 RoutineControl：Dcm 将例程请求映射到配置的 Server Call/例程处理函数，进而调用应用服务。
- 0x2E WriteDataByIdentifier：写入允许写的诊断数据；若应用需要响应新值，还要配置对应 DataElement、Runnable 触发事件或应用轮询机制。
- Client-Server：Dcm 通过 RTE 调用 SW-C 提供的服务操作。

**注意：** 不是每个 0x2E 写 DID 都会自动触发 Runnable。是否触发、触发哪个事件，必须检查 Dcm、RTE、Port Interface 和 Runnable Event 的完整配置。

~~~~mermaid
flowchart LR
  A[CAN Frame] --> B[CanIf]
  B --> C[CanTp]
  C --> D[PduR]
  D --> E[Dcm：UDS 服务 / 权限检查]
  E --> F[RTE Client-Server / DataElement]
  F --> G[SW-C Runnable]
~~~~

## 63. 诊断会话（0x10）和安全访问（0x27）是什么关系？

**答案：** 诊断会话决定 ECU 当前允许使用哪些诊断服务；安全访问决定请求方是否获得受保护操作的权限。可以理解为“会话定义可进入的工作模式，安全访问授予额外权限”。

- Default Session：基础诊断能力。
- Extended Session：开放项目配置允许的扩展服务。
- Programming Session：用于刷写等编程场景。
- SecurityAccess：通常通过 Seed/Key 或项目规定的认证机制解锁特定安全等级。

刷写通常要求进入编程会话，并通过安全访问；但具体哪些服务需要哪种会话/安全等级，应查 OEM 诊断规范和 Dcm 配置，不能认为所有写服务都统一要求同一 Security Level。

## 64. AUTOSAR OS 的 Category 1 与 Category 2 中断有什么区别？

**答案：**

- Category 1 ISR：不由 OS 按 Category 2 方式管理，不能调用需要 OS 上下文的服务；适合极低延迟、无需任务交互的处理。
- Category 2 ISR：由 OS 管理，可调用标准允许的 OS 服务，例如 ActivateTask/SetEvent 等，适合需要通知任务的中断处理。

选择依据不是“越快越好”，而是是否需要 OS 服务、优先级管理和任务交互。具体 ISR 类型、可调用服务和嵌套规则要按所用 AUTOSAR OS 版本与供应商实现核对。

## 65. BSW Service Layer 常见服务类别有哪些？

**答案：** BSW Service Layer 面向应用和其他 BSW 模块提供系统级服务，常见类别包括：

- I/O 服务：对 I/O 和信号访问提供抽象服务。
- 存储服务：NvM、MemIf 等非易失存储管理。
- 通信服务：Com、PduR、ComM、CanNm、诊断通信等。
- 加密/安全服务：Crypto、Csm、KeyM、SecOC 等（具体模块按版本和配置）。
- 系统服务：EcuM、BswM、OS 相关服务、看门狗管理、时间同步等。

这是一种便于学习的分类，不是说每个模块都只属于一个绝对互斥的类别。实际 BSW 分层还包括 ECU Abstraction、MCAL 和 Complex Device Driver 等层次。

~~~~mermaid
flowchart TB
  A[BSW Service Layer] --> B[I/O 服务]
  A --> C[存储服务]
  A --> D[通信服务]
  A --> E[加密与安全]
  A --> F[系统服务]
  G[ECU Abstraction / MCAL / CDD] --> A
~~~~

## Flomo 原始来源

- AUTOSAR 1000 问总表：https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4
- Bootloader UDS 刷写链路：https://v.flomoapp.com/mine/?memo_id=MjUyNTg3Mzgy
- 诊断请求触发 SW-C：https://v.flomoapp.com/mine/?memo_id=MjU0MDI3OTky
- Session 与 SecurityAccess：https://v.flomoapp.com/mine/?memo_id=MjUzNzAyMTM5
- ISR Category 1/2：https://v.flomoapp.com/mine/?memo_id=MjUzNzA0NjA2
- BSW 服务分类：https://v.flomoapp.com/mine/?memo_id=ODQwNDI0MDg
