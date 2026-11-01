# 运行时问题定位 Q1：某路 CAN 报文没发出来——从 Rte\_Write 顺藤摸瓜，逐层查哪个返回值？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzczMjE3

运行时问题定位 Q1：某路 CAN 报文没发出来——从 Rte\_Write 顺藤摸瓜，逐层查哪个返回值？

关键思路：沿发送链路逐层看返回值，哪一层返回 E\_NOT\_OK 就锁定在哪一层（或它的下游配置）。

发送链路与检查点：

1. RTE：Rte\_Write 返回 E\_OK / E\_NOT\_OK。返回错 → 端口/接口或该 PDU 配置有问题。

2. COM：Com\_TransmitSignal / Com\_UpdateShadowSignal 是否接受信号、信号是否映射到 PDU。返回错 → 信号没映射到 PDU 或 PDU 未配置。

3. PduR：PduR\_Transmit 把 PDU 路由到对应通信接口。返回错 → 路由表项缺失（没配到 CanIf）。

4. CanIf：CanIf\_Transmit 把 PDU 交给 Can 驱动。返回错 → CanIf 底层（Tx Buffering / Can Controller）未就绪。

5. Can 驱动：Can\_Write 发到硬件。看返回值 + 发送队列是否满 / Bus-off。


容易漏的补充排查点：

- 周期性 PDU 还没到发送周期（没触发）。
- PDU 的传输方向（Tx / Rx）配反了。
- Can 控制器还没到 Normal mode（Can\_ControllerModeChange 是否成功、有没有 Bus-off）。
- 被 Bus-off 压住：Can 驱动在 Bus-off 时不发送。
- 信号值被判为 InvalidValue 而没发送。

一句话：从 Rte\_Write 到 Can\_Write 逐层看返回值，顺带查方向、周期、Bus-off/控制器模式；先定位到层，再深入层内配置。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzczMTY2><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR

## API 与排查边界修订

不能把每条 Rte_Write 都当成直接调用 Com_TransmitSignal：RTE 根据通信类型、生成策略和 ECU 部署实现数据写入；COM 的信号/PDU 发送由相应 COM 配置和 MainFunction/触发机制推进。Rte_Write 的返回类型/可检查返回值也取决于生成的 API 原型和接口配置，应以工程 Rte_* 头文件为准。

建议结合三类证据，而不只追返回值：
- RTE/COM 生成代码与 API 原型：确认写入是否成功、数据是否进入正确 buffer。
- CANoe/CANalyzer Trace：确认 PDU 是否被提交、实际发送时间、错误状态和 BusOff。
- CanIf/Can Driver 状态与控制器模式：确认发送队列、HTH、控制器状态、Tx confirmation 和错误计数。

若使用周期发送，Rte_Write 成功只说明数据写入接口成功，不代表该帧已立即上总线。