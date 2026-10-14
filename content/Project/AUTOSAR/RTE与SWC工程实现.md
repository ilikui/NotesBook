---
title: RTE 与 SWC 工程实现
tags:
  - Project
  - AUTOSAR
  - CP
  - RTE
---

# RTE 与 SWC 工程实现：从端口建模到 Runnable 执行

> [!info] 一句话定位
> SWC 描述功能与接口，系统描述组件如何连接和部署，RTE Generator 将模型与 ECU 配置转成目标 ECU 可编译的通信与调度代码。

## 1. 核心对象

| 对象 | 解决的问题 | 典型内容 |
| --- | --- | --- |
| SWC Type | 组件提供什么能力 | Application SWC、Composition SWC |
| Port | 组件如何与外界交互 | P-Port、R-Port |
| Interface | 端口交换什么 | Sender-Receiver、Client-Server、Mode-Switch |
| Connector | 组件如何逻辑连接 | Assembly Connector、Delegation Connector |
| Internal Behavior | 组件内部有哪些执行实体 | RunnableEntity、RTEEvent、IRV |
| Mapping | 运行实体如何部署与调度 | ECU Mapping、Runnable-to-Task Mapping |
| RTE | 如何落实通信和调度 | Rte_Read、Rte_Write、Rte_Call 等生成 API |

- **P-Port** 表示组件提供的数据、服务或模式能力。
- **R-Port** 表示组件需要从外部读取数据或调用服务。
- 端口类型与接口类型必须兼容；名字相似不代表可以连接。
- 连接器描述逻辑关系。是否跨 ECU、跨核及最终走哪条通信路径，还取决于系统映射和 ECU Extract。

## 2. 常见接口类型

| 范式 | 语义 | 常见 API | 建模关注点 |
| --- | --- | --- | --- |
| Sender-Receiver | 交换数据元素 | Rte_Read / Rte_Write；也可能使用隐式访问 API | 数据类型、队列策略、初始值、更新语义 |
| Client-Server | 请求操作并获得结果 | Rte_Call；异步场景可能涉及 Rte_Result | Operation、参数方向、同步/异步语义 |
| Mode-Switch | 发布或观察模式变化 | Rte_Switch、Rte_Mode 等 | ModeDeclarationGroup、事件关联 |
| Parameter / Calibration | 读取参数或标定值 | 例如 Rte_Prm | 参数来源、可变性、标定链路 |
| NvData / NvBlock | 持久化相关数据交互 | 由建模与生成接口决定 | NvM、块配置、恢复策略 |

实际函数原型、返回值和错误语义必须以当前生成的 Rte_*.h、AUTOSAR Release 和供应商工具为准。

## 3. Runnable 为什么没有运行？

Runnable 是组件内部的执行单元，不等同于 OS Task。通常需要完整链路：

~~~mermaid
flowchart TD
    A["SWC InternalBehavior"] --> B["RunnableEntity"]
    B --> C["RTE Event"]
    C --> D["Event 与 Runnable 关联"]
    D --> E["Runnable-to-Task 映射"]
    E --> F["RTE / OS 生成代码"]
    F --> G["OS 调度执行"]
    G --> H["Runnable 入口被调用"]
~~~

排查顺序：

1. 检查 InternalBehavior 中是否声明 RunnableEntity。
2. 检查 TimingEvent、DataReceivedEvent、OperationInvokedEvent、InitEvent 或 ModeSwitchEvent 是否正确关联。
3. 检查 ECU Mapping、Runnable-to-Task Mapping 与 OS Task 配置。
4. 检查生成代码是否包含对应 Runnable 包装与调度入口。
5. 在 Task 和 Runnable 入口分别打点，区分“任务没调度”与“任务执行但 Runnable 未被调用”。

## 4. S/R 数据访问的工程注意点

下面是概念示例，函数名称与原型以生成头文件为准：

~~~c
void SpeedConsumer_10ms(void)
{
    uint16 speed_kph = 0U;
    Std_ReturnType ret;

    ret = Rte_Read_R_Speed_speedValue(&speed_kph);
    if (ret == RTE_E_OK)
    {
        SpeedConsumer_Process(speed_kph);
    }
    else
    {
        SpeedConsumer_HandleReadError(ret);
    }
}
~~~

- API 返回成功不等于数据刚刚从物理总线收到。数据新鲜度应结合更新指示、超时、有效性状态或 E2E 状态判断。
- 状态量与事件量语义不同：非排队数据通常表达最新状态；排队数据适合需要保留多个样本的场景。队列深度与溢出策略需要评审。
- 不要假定 Rte_Write 一定直接发出 CAN 帧。跨 ECU 通信通常还涉及 COM、PduR、CanIf、驱动和发送调度。
- 显式访问由 Runnable 显式调用 API；隐式访问采用 RTE 提供的隐式访问语义。缓存、拷贝和一致性行为依配置与生成实现而定，不能笼统断言一定零拷贝或绝对原子。

## 5. C/S 调用链

同步 Client-Server 调用通常经历：

1. Client Runnable 调用生成的 Rte_Call API。
2. RTE 根据连接与配置转发到对应 Server Operation。
3. Server 侧 OperationInvokedEvent 与 Runnable 关联。
4. Server Runnable 执行，结果通过生成的参数 / 返回值路径回传。

排查时区分“调用 API 失败”“服务端没有被调度”“服务端执行但结果异常”。异步调用不能套用同步调用的假设。

## 6. 生成前后检查表

**生成前**
- [ ] Port、Interface、DataElement、Operation 与数据类型引用有效。
- [ ] P-Port / R-Port 兼容，Connector 完整。
- [ ] Runnable、Event、执行映射和 ECU 分配一致。
- [ ] 数据单位、缩放、无效值、队列策略与初始值已评审。
- [ ] 变更后的 ARXML 已进入正确工程与变体。

**生成后**
- [ ] 检查生成头文件中的 API 原型，不凭记忆手写调用。
- [ ] 检查 Runnable 调用入口、Task 映射和 OS 配置。
- [ ] 检查 RTE 与 COM / NvM / BSW 的生成连接。
- [ ] 编译、链接无缺失符号、重复定义和类型不匹配。
- [ ] 测试初始化、超时、无效数据、并发访问和时序预算。
- [ ] 记录工具版本、配置输入、变体与输出版本，确保可追溯。

## 相关笔记

- [[规范模块/RTE]]
- [[规范模块/SoftwareComponentTemplate]]
- [[规范模块/SystemTemplate]]
- [[规范模块/ECUConfiguration]]
- [[规范模块/COM]]
- [[规范模块/OS]]
- [[ARXML 与 RTE 代码生成实战]]
- [[AUTOSAR 故障排查手册]]
