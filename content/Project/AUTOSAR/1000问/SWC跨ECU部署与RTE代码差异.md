# SW-C 跨 ECU 部署与 RTE 代码差异

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzcxMzAz

同一组 SW-C 部署到不同 ECU，RTE 生成代码差多少？哪些重配、哪些复用？

RTE 是 **基于每个 ECU 的 ECU Extract** 生成的，所以同一组 SW-C 部署到不同 ECU，生成的 RTE 代码差别很大——因为每个 ECU 的通信拓扑、可用总线、部署的 SW-C 集合都不同。

会不同的部分（需按 ECU 重配）：

1. RTE 收发实现：同 ECU 内的 S/R 通信走 RTE 内部（直接拷贝/引用）；跨 ECU 通信要经 COM→PduR→CanIf 等 BSW 栈。同一个 Rte\_Write/Rte\_Read，本地和远端生成的实现完全不同。

2. 通信 BSW 配置：各 ECU 挂的总线、帧 ID、DLC、PDU 映射不同，CanIf/PduR/COM 配置要按 ECU 重做。

3. 可用信号 / PDU 集合：ECU Extract 裁剪后，每个 ECU 只含自己相关的 PDU 和信号，生成的 RTE 接口集、端口集不同。

4. 调度映射：各 ECU 的 OS Task、Schedule Table 不同，RTE 触发 Runnable 的方式（SchM 调用）也不同。

5. 内存映射 / 标定：地址映射、A2L 地址按 ECU 不同。


可以复用的部分：

1. SW-C 应用代码本身：只依赖 Rte\_Read/Rte\_Write 的函数签名，不依赖具体实现。只要端口/接口/数据类型一致，源码原样复用、不用改。

2. SW-C 的 VFB 层接口定义：ports、interfaces、data types 在 VFB 层面定义，不因部署 ECU 改变。

3. 通用 BSW 配置模板：同总线类型时模板可以搬，具体值按 ECU 调。


一句话：SW-C 之所以"一次编写、多 ECU 部署"，靠的是 RTE 做解耦——SW-C 只认 RTE 接口签名，RTE 负责为每个 ECU 生成不同的"胶水代码"。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzcxMTk1><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR