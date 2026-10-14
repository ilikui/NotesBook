---
title: ARXML 与 RTE 代码生成实战
tags:
  - Project
  - AUTOSAR
  - ARXML
  - RTE
---

# ARXML 与 RTE 代码生成实战

> [!info] 核心原则
> ARXML 是模型交换与配置描述，不是简单的 XML 转 C。RTE 生成依赖多层模型、引用关系、ECU 映射、配置约束和具体生成器的输入规则。

## 1. ARXML 输入分层

| 层次 | 描述内容 | 主要回答的问题 |
| --- | --- | --- |
| Data Types | Application / Implementation Data Type、CompuMethod、DataConstr | 数据是什么，如何表示、缩放和约束 |
| SWC Description | SWC Type、Port、Interface、InternalBehavior、Runnable、Event | 组件提供 / 需要什么，何时执行 |
| System Description | Composition、Connector、System Signal、I-Signal、I-PDU | 组件如何连接，逻辑信号如何映射 |
| ECU Mapping / Extract | ECU 分配、通信映射、组件部署 | 哪个 ECU 实现哪些功能与通信 |
| ECU Configuration | RTE、OS、COM、PduR、CanIf 等配置值 | 目标 ECU 如何配置运行时和 BSW |
| Generator Configuration | 工具特定设置、变体与输入集合 | 本次生成器究竟读取什么 |

文件拆分、包名和引用路径取决于项目方法论、供应商工具与项目约定，不能把某一种目录结构当作标准强制规则。

## 2. 典型生成流程

~~~mermaid
flowchart TD
    A["需求与接口设计"] --> B["数据类型 / SWC ARXML"]
    B --> C["System Description 与 Connector"]
    C --> D["ECU Extract / Mapping"]
    D --> E["ECUC 与 OS / COM 等配置"]
    E --> F["RTE Contract Phase"]
    F --> G["检查生成的 SWC API 头文件"]
    G --> H["RTE Generation Phase"]
    H --> I["RTE / BSW 生成代码"]
    I --> J["编译、链接、静态分析"]
    J --> K["集成测试与时序验证"]
    K --> L["版本归档与可追溯记录"]
~~~

这是概念流程，不代表所有工具使用完全相同的阶段名称或按钮顺序；以项目采用的 AUTOSAR Release 与工具文档为准。

## 3. ARXML 引用检查

检查 SWC Port 时，不要只看 XML 片段是否格式正确，还应确认：

1. Port 引用的 Interface 存在，路径指向正确的 SHORT-NAME 层级。
2. Interface 的 DataElement / Operation 类型与 SWC 使用方式一致。
3. DataElement 引用的数据类型存在，CompuMethod、DataConstr、单位和缩放符合接口约定。
4. Runnable 的 Event 关联目标有效，Event 类型与行为相匹配。
5. Assembly Connector 的 Provider / Requester 端口存在且类型兼容。
6. ECU Mapping 和 Extract 包含本次需要生成的对象。
7. ECUC 参数 Definition 引用与实际配置值匹配。
8. 输入文件的 AUTOSAR Schema / Release 兼容，避免不同版本元素混用。

## 4. 生成失败的分层定位

| 症状 | 优先检查 | 避免的误操作 |
| --- | --- | --- |
| XML 解析失败 | XML 语法、编码、Schema、命名空间 | 不要改业务模型绕过语法错误 |
| 模型加载但引用 unresolved | DEST、SHORT-NAME 路径、包层级、导入顺序 | 不要只按文件名猜引用 |
| Contract Phase 失败 | SWC 接口、Runnable API、数据类型 | 不要先去改 OS Task |
| RTE Generation 失败 | ECU Extract、连接、映射、约束、输入集合 | 不要只重跑而不保存日志 |
| 生成成功但编译失败 | include 路径、类型定义、生成文件集、编译选项 | 不要混用不同轮次的生成输出 |
| 链接缺符号 | 声明与实现、源文件列表、变体一致性 | 不要用弱符号掩盖配置问题 |
| 运行时没有数据 | RTE → COM → PduR → If / Driver、I-PDU Group、Task | 不要把代码生成成功当成通信正常 |

## 5. 增量生成与版本追溯

- 变更前保存 ARXML、ECUC、工具版本和生成配置。
- 明确影响范围：接口、数据类型、连接、Runnable / Event、ECU 映射或 BSW 配置。
- 使用项目规定的增量或全量生成策略；依赖影响不清晰时，先做全量生成验证。
- 清理或隔离旧输出，避免新旧生成文件混编。
- 比较生成代码差异，解释 API、Runnable 包装、Task 入口与通信路径的变化。
- 编译、链接、单元测试和集成测试通过后再归档。
- 记录输入版本、工具版本、变体、命令 / 选项、日志和输出提交号。

## 6. 推荐排查顺序

~~~mermaid
flowchart TD
    A["生成或集成失败"] --> B{"XML / Schema 通过？"}
    B -- 否 --> C["修复语法、命名空间、版本"]
    B -- 是 --> D{"模型引用完整？"}
    D -- 否 --> E["修复 DEST、路径与对象引用"]
    D -- 是 --> F{"连接与 ECU 映射完整？"}
    F -- 否 --> G["修复 Connector、Extract、Mapping"]
    F -- 是 --> H{"ECUC / OS / COM 配置一致？"}
    H -- 否 --> I["检查配置约束与模块依赖"]
    H -- 是 --> J["检查生成日志、输出、编译与链接"]
~~~

## 相关笔记

- [[方法论]]
- [[规范模块/SoftwareComponentTemplate]]
- [[规范模块/SystemTemplate]]
- [[规范模块/ECUConfiguration]]
- [[规范模块/RTE]]
- [[RTE 与 SWC 工程实现]]
- [[AUTOSAR 故障排查手册]]
