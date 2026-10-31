---
title: E2E / 端到端通信保护深入 Q2：E2E 报文到达但 CRC 校验失败——丢弃还是用上次有效值？AUTOSAR 推荐做法？
tags:
  - AUTOSAR
  - 1000问
---

# E2E / 端到端通信保护深入 Q2：E2E 报文到达但 CRC 校验失败——丢弃还是用上次有效值？AUTOSAR 推荐做法？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1MjU0NDky

E2E / 端到端通信保护深入 Q2：E2E 报文到达但 CRC 校验失败——丢弃还是用上次有效值？AUTOSAR 推荐做法？

先分清：E2E 库只负责「检测 + 报告」，不替应用决定用哪个值。

推荐流程：

1. E2E check（E2E\_PXXCheck）返回状态：OK / REPEATED / WRONGSEQUENCE / ERROR / NONEWDATA 等。

2. CRC 校验失败 → 状态 ERROR。此时不使用这次到达的数据（丢弃坏数据）。

3. 是否用「上次有效值」是应用层策略，不是 E2E 默认行为。AUTOSAR 让 SW-C / RTE 根据 check status 自行决定。


实际项目（尤其安全相关）推荐：

- 对安全相关信号：CRC 失败时不更新数据，用「上次通过校验的有效值」（last good value），并在逻辑上标记为失效 / 触发 DTC、错误计数。
- 对「必须实时、旧值可能已过时」的信号：直接进入安全默认值（safe state / fallback），不用旧值——取决于是否允许用过期数据。

关键原则：丢弃坏数据是共识；「用旧值还是安全值」取决于信号类型和 ASIL 等级。别把「上次有效值」当永续有效——如果连续多帧都失败，应转入安全状态，而不是永远用旧值。

补充：有些实现把 E2E 检查做在 RTE 层（E2E wrapper），失败的数据可能不传到 SW-C、或带 state 一起传。那时 SW-C 只需按收到的状态处理。

一句话：E2E 给状态、应用层定策略。CRC 失败一律不用坏数据；用「上次有效值」还是「安全默认值」，看信号类型和 ASIL——且连续失败要转安全状态，别让旧值永续。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0OTY4OTU4><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR