---
title: NvM 块管理策略深入 Q1 Redundant 块怎么判断「哪一份是好的」？NvM 用什么机制判断数据完整性？
tags:
  - AUTOSAR
  - 1000问
---

# NvM 块管理策略深入 Q1：Redundant 块怎么判断「哪一份是好的」？NvM 用什么机制判断数据完整性？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1MjU1NTgw

NvM 块管理策略深入 Q1：Redundant 块怎么判断「哪一份是好的」？NvM 用什么机制判断数据完整性？

NvM 判断完整性主要靠 CRC 校验 + Block 状态标记（可能加序列号）。

机制：

1. CRC / 校验：每个 NvM Block 存储时附带 CRC（NvM 的 Block 配置可开 CRC），写入时算 CRC、读时校验。

2. Redundant 双副本读写：
   - 写入：把数据写两份（主副本 \+ 冗余副本）。
   - 读取：NvM 先校验主副本的 CRC——通过就返回；失败则尝试冗余副本。若两份都失败，判定块损坏，NvM 走默认值 / 恢复逻辑（如回写默认值、触发 DET / DEM 记录）。
3. Block 状态 / 序列号：
   - Block 附带状态标记（如 BLOCK\_STATE）和可能的序列号 / 计数器，防止读到旧数据（用来区分哪份是最新、哪份是有效）。

所以「哪一份是好」的判定流程：CRC 校验优先，主副本失败切冗余副本，双失败视为坏块（用默认值 / 恢复）。

补充：NvM 还依 MemIf / Fee 保证底层数据一致性（掉电时 Block 完整性）；NvM 的 CRC 是针对「NvM 数据块 + 冗余副本」级别，不是底层 Flash 校验。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU1MjU1NTEz><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR