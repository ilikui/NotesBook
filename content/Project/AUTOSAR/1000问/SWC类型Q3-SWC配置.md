---
title: AUTOSAR 1000问 · SWC类型Q3 如何配置 SWC？
tags:
  - AUTOSAR
  - 1000问
---

# AUTOSAR 1000问 · SWC类型Q3：如何配置 SWC？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjYxMzU1MTQ3

**AUTOSAR 1000问 · SWC类型Q3：如何配置 SWC？**

▎ 五大学习法：麦肯锡金字塔——把「配置 SWC」拆成 MECE 四件事

**费曼（一句话本质）**：配置 SWC 就是给它装一块「插座面板」——定好对外说什么话（Port/Interface）、内部做什么事（Runnable），怎么接到车上交给 ECU 集成。

**先分清两层**：SWC 是设计层（逻辑上提供什么、需要什么）；Task 是运行层（什么时候跑）。桥梁是 Runnable——SWC 里可被调度的函数单元，最终映射到某个 Task。

**SQ3R（去哪找）——两个工具配合**：

- DaVinci Developer：设计 SWC 本体
- DaVinci Configurator：集成到 ECU、生成 RTE

**麦肯锡金字塔（配置就四件事，MECE）**：

1. 对外接口：Port（P 提供 / R 需求）+ Port Interface（S/R 数据、C/S 操作、Mode-Switch、NvData）
2. 内部行为：Runnable + 触发事件（TimingEvent 周期 / DataReceivedEvent 收数据 / OperationInvokedEvent 被调用 / InitEvent 初始化）
3. 数据类型：Data Type（Application / Implementation Data Type）
4. 接到哪（Configurator 侧）：SWC→ECU 映射、Runnable→Task 映射、Port Connector（SWC↔SWC、SWC↔BSW 服务口）、Partition/核分配

**西蒙（核心流程）**：Developer 建 SWC（Port + Runnable）→ 导出 ARXML → Configurator 导入 → Runnable 映射到 Task → 连 Port → 生成 RTE。

**四个常见的坑**：

- Runnable 触发方式跟 Task 类型不匹配（TimingEvent 的 Runnable 必须挂周期 Task）
- SWC 之间没连 Connector，RTE 生成后端口空转
- 一个 Runnable 不能映射到多个 Task，会报错
- 改了 SWC 必须重新导 ARXML + Configurator 重新导入，否则两边不同步

**卢曼卡片盒**：与 SWC类型Q2（Composition SW-C）、OS&调度Q2（DaVinci 新增 Task）互链。

📎 上一题（OS&调度Q2）→ [https://v.flomoapp.com/mine/?memo\_id=MjYxMzU1MDgy](https://v.flomoapp.com/mine/?memo_id=MjYxMzU1MDgy)<br>
📎 同专题（SWC类型Q2）→ [https://v.flomoapp.com/mine/?memo\_id=MjU0NDY1ODM1](https://v.flomoapp.com/mine/?memo_id=MjU0NDY1ODM1)<br>
📎 AUTOSAR 1000问总表 → [https://v.flomoapp.com/mine/?memo\_id=MjMxMTQ2NDk4](https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4)

#Area/技术/AUTOSAR