---
title: EcuM 状态机深入 Q2 PostRun 是干什么用的？SW-C 都停了 EcuM 还在 PostRun 期间哪些模块在工作？正写 NvM 收到 Shutdown 请求，强制掉电还是等写完？
tags:
  - AUTOSAR
  - 1000问
---

# EcuM 状态机深入 Q2：PostRun 是干什么用的？SW-C 都停了 EcuM 还在 PostRun 期间哪些模块在工作？正写 NvM 收到 Shutdown 请求，强制掉电还是等写完？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1MjU1ODIy

EcuM 状态机深入 Q2：PostRun 是干什么用的？SW-C 都停了 EcuM 还在 PostRun 期间哪些模块在工作？正写 NvM 收到 Shutdown 请求，强制掉电还是等写完？

PostRun 的用途：

- EcuM 在 RUN 之后、Shutdown 之前的一个过渡态。用于「应用（SW-C）已停止，但系统还需做收尾工作」的场景——主要给「必须落盘的数据」最后一次写机会，也允许诊断收尾。

PostRun 期间仍在工作的模块：

- NvM（WriteAll / 写数据：持久化关键参数、状态、计数、故障快照）。
- Fee / MemIf（NvM 底层，为写数据服务）。
- Dcm / 诊断（如需在关机前完成某些写入 / 记录）。
- WdgM / 看门狗（维持，避免复位）。
- EcuM / BswM（做关机前模式收尾）。

正在 NvM 写数据时收到 Shutdown 请求：

- 取决于配置。通常 EcuM 不会在 NvM 写入中途强制掉电，否则破坏数据一致性（NvM 写是异步的，可能没写完）。
- 做法：EcuM 通过 NvM 的写入完成回调（NvM\_JobEndNotification）协调——进入最终 Shutdown 前，等 NvM 完成未完成写入 / 查询写入状态，再掉电或进低功耗。
- 若有强制时间限制（看门狗 / 超时）：NvM 写有超时，EcuM 超时后仍会关机，但那是「尽力而为」。
- 量产设计：EcuM 的 Shutdown Sequence 会包含 NvM 写，等它完成（回调确认）才掉电——保证数据一致性，避免损坏。

一句话：PostRun 是「应用停、做数据收尾」的过渡态，期间 NvM 等还在存数据。收到 Shutdown 时 EcuM 会等 NvM 写完（通过完成回调）再掉电，而不是中途强断——为了数据一致性。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU1MjU1NzUw><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR