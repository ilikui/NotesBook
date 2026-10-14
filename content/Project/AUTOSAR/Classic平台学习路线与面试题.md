---
title: Classic 平台学习路线与面试题
tags:
  - Project
  - AUTOSAR
  - CP
  - Interview
---

# AUTOSAR Classic 平台学习路线与面试题

## 1. 学习路线：从模型到运行时

~~~mermaid
flowchart TD
    A["全局架构：CP / AP、VFB、分层"] --> B["数据与模型：ARXML、Data Type、SWC"]
    B --> C["接口与执行：Port、Interface、Runnable、Event"]
    C --> D["RTE：API、映射、生成阶段"]
    D --> E["通信栈：COM → PduR → CanIf → CanDrv"]
    D --> F["OS：Task、Alarm、Event、时序"]
    E --> G["诊断：Dcm / CanTp / PduR"]
    E --> H["网络管理：ComM / CanNm"]
    D --> I["存储：NvM / MemIf / Fee 或 Ea"]
    G --> J["集成、测试、故障定位"]
    H --> J
    I --> J
    F --> J
~~~

建议每学一个模块，都输出四类笔记：

1. **职责卡**：模块解决什么问题，不负责什么。
2. **调用链卡**：上下游模块、关键 API、回调和异步边界。
3. **配置卡**：关键参数、依赖约束、生成输入和版本差异。
4. **故障卡**：现象、证据采集点、定位路径和回归测试。

## 2. 必须能够画出来的三条链路

- **信号发送**：Runnable → RTE API → COM Signal / I-PDU → PduR → CanIf → CanDrv → CAN Controller。
- **诊断请求**：CAN / CanIf → PduR → CanTp → Dcm；响应方向由对应传输与路由配置返回。
- **非易失存储**：使用者 → NvM → MemIf → Fee 或 Ea → 底层存储驱动。具体介质和模块组合由项目决定。

## 3. 面试问题与回答框架

### Q1：RTE 是什么？它是不是普通中间件？

RTE 是 CP 中 VFB 的 ECU 级实现，为 SWC 提供生成的通信 API，并衔接 SWC、BSW 与 OS。它依赖 SWC 描述、系统连接、ECU 映射和配置输入生成；不等同于独立 OS，也不意味着所有通信都走物理总线。

### Q2：Rte_Write 成功但对端没有收到，怎么排查？

1. 确认 Runnable 执行、写入值和 API 返回值。
2. 检查 SWC 连接和 ECU 映射。
3. 检查 COM 信号、I-PDU、发送模式、I-PDU Group 和触发条件。
4. 检查 PduR 路由、CanIf、CanDrv 与控制器状态。
5. 抓包确认帧是否发送，再排查接收侧解包与超时。
6. 每层用计数器、返回值、日志或波形形成证据链。

### Q3：COM 与 PduR 的职责有什么区别？

COM 面向信号，负责信号打包 / 解包、发送模式、更新与超时等行为。PduR 面向 PDU，按静态配置在上层模块与下层接口 / TP 模块间路由。不要混淆信号语义与 PDU 路由职责。

### Q4：ARXML 合法是否代表可以成功生成代码？

不代表。XML 语法 / Schema 校验、模型引用完整性、配置约束、ECU Extract 与映射、工具支持范围、生成器输入集合是不同层次，应结合日志逐层定位。

### Q5：Runnable 与 Task 是什么关系？

Runnable 是 SWC 内的可运行实体；Task 是 OS 的调度执行上下文。Runnable 通常通过 RTE Event、映射和生成代码进入 OS 调度，不应把 Runnable 直接等同于 Task。

### Q6：Explicit 与 Implicit 数据访问有什么区别？

Explicit 由 Runnable 显式调用读写 API；Implicit 使用 RTE 提供的隐式访问语义。实际缓存、拷贝和一致性行为依配置与生成实现，不应描述成始终零拷贝或绝对一致。

### Q7：为什么要区分 CP 与 AP？

CP 面向资源受限、强调静态配置与实时控制的 ECU 软件；AP 面向高性能计算、服务化通信与动态部署等需求。二者执行环境、API 和架构假设不同，不能把 CP 的 RTE / BSW 机制直接套用到 AP。

## 4. 工程化回答模板

回答 AUTOSAR 问题时，按以下顺序组织：

1. **定义**：一句话说明模块职责。
2. **位置**：它在架构和调用链中的位置。
3. **输入 / 输出**：模型、配置、API、PDU 或信号。
4. **运行过程**：调用链、同步 / 异步边界和调度关系。
5. **关键配置**：需要核对的参数类别与约束。
6. **故障定位**：观察点、证据和验证步骤。
7. **版本边界**：AUTOSAR Release、供应商工具和项目配置的影响。

## 相关笔记

- [[AUTOSAR]]
- [[软件架构]]
- [[规范模块]]
- [[规范模块/RTE]]
- [[规范模块/COM]]
- [[规范模块/PDURouter]]
- [[RTE 与 SWC 工程实现]]
- [[ARXML 与 RTE 代码生成实战]]
- [[AUTOSAR 故障排查手册]]
