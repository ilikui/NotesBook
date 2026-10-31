---
title: AUTOSAR 1000问 · OS&调度Q2 如何在 DaVinci 新增一个 Task？
tags:
  - AUTOSAR
  - 1000问
---

# AUTOSAR 1000问 · OS&调度Q2：如何在 DaVinci 新增一个 Task？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjYxMzU1MDgy

**AUTOSAR 1000问 · OS&调度Q2：如何在 DaVinci 新增一个 Task？**

▎ 五大学习法：费曼——把「新增 Task」讲成「给 OS 报户口」

**费曼（本质一句话）**：新增 Task = 告诉 OS「多了一个可被调度的执行单元」——给它身份（名字/优先级）、调度规则（能不能抢、能激活几次）、资源（栈），再由代码给它一个身体。

**SQ3R（去哪找）**：DaVinci Configurator 配置树 → Os 模块 → OsTask 容器 → Add OsTask。（Task 是 OS 的概念；RTE 那边对应 Runnable，最后映射到 Task）

**麦肯锡金字塔（必配项，MECE 四类）**：

- 身份：OsTaskName、OsTaskPriority（数值越大优先级越高，须落在所属 OsApplication 的优先级区间内）
- 调度：OsTaskSchedule（FULL 可抢占 / NON 非抢占）、OsTaskActivation（1=基本任务只能激活一次；>1=扩展任务可多次激活 + 等事件）
- 资源：OsTaskStackSize（栈大小，静态分配）
- 关联：OsApplication/Partition（挂哪个核/分区）、OsTaskEventRef（扩展任务等的 Event）、Autostart（是否开机自启）

字段名各版本略有差异，以工程版本为准。

**西蒙（核心四步）**：Add OsTask → 填四类属性 → Validate 查错 → Generate，代码里实现 TASK(TaskName){...}。

**三个最常见的坑**：

- 优先级方向搞反（AUTOSAR OS 数字大 = 优先级高）或超出 OsApplication 区间，校验直接报错
- 扩展任务（Activation>1）没配 WaitEvent，会退化成「跑完就没了」
- 新增后没重新 Generate / 没更新链接脚本，跑不起来；栈给太小直接溢出

**卢曼卡片盒**：与 OS&调度Q1（AUTOSAR OS vs FreeRTOS）互链。

📎 上一题（OS&调度Q1）→ [https://v.flomoapp.com/mine/?memo\_id=MjUzNTQxMjIz](https://v.flomoapp.com/mine/?memo_id=MjUzNTQxMjIz)<br>
📎 AUTOSAR 1000问总表 → [https://v.flomoapp.com/mine/?memo\_id=MjMxMTQ2NDk4](https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4)

#Area/技术/AUTOSAR