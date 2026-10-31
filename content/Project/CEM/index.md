---
title: CEM 项目知识地图
tags:
  - CEM
  - 汽车电子
---

# CEM 项目知识地图

CEM（Central Electronic Module / 中央电子模块，具体项目命名以 OEM 架构定义为准）相关记录入口。当前归档来自历史 Flomo 需求和问题线索，尚未等同于完整设计规格；具体接口、诊断和休眠唤醒逻辑仍需结合项目 ARXML、软件架构和 OEM 需求确认。

## 需求与功能域

- [[需求分析/CEM功能域与诊断需求]]：执行器/传感器、Climate、驾驶员信息、ECU 平台、车灯、门锁、低压能源管理、远程控制、安全、TPMS、车窗后视镜等功能域，以及诊断需求线索。

## 软件架构与问题清单

- [[软件架构/CEM软件结构与待研究问题]]：DTC/DID、NvM 分层实现、接口配置和协议栈等待研究问题。
- [[100问/CEM工作问题清单]]：接口配置与休眠唤醒逻辑问题。

## 工具链

- [[工具链/ARXML数据可视化需求]]：ARXML 配置数据可视化。
- [[工具链/ARXML转JSON与n8n自动化]]：ARXML 解析为 JSON，并通过 n8n 串联自动化流程。

## 后续完善建议

1. 以项目实际 ARXML 和需求基线为准，明确 CEM 的 ECU 边界与功能分配。
2. 将接口配置拆分为 SWC、Port、Interface、Runnable、RTE 与通信链路。
3. 将休眠唤醒拆分为 EcuM、BswM、CanSM、ComM、网络管理和电源模式时序。
4. 将诊断拆分为 Dcm、Dem、DID、DTC、NRC 与故障存储。
5. 对 NvM 链路明确 NvM、MemIf、Fee/Ea、Fls/Eep 的调用关系及掉电保护。
