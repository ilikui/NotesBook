# ECU Extract 与 System Description 映射

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzcxMTk1

VFB 的 System Description 怎么「提取」出单个 ECU 的配置？ECU Extract 是裁剪还是映射？

System Description（系统描述）：在 VFB 层面描述整个系统——所有 SW-C、所有连接、所有接口、所有 ECU 的抽象。它不含任何具体 ECU 的实现信息（内存地址、总线映射、周期细节都没有）。

ECU Extract of System Description（ECU 抽取）：从系统描述里抽出「属于某个特定 ECU」的那一部分——只包含部署在这个 ECU 上的 SW-C、这些 SW-C 需要的接口连接、以及相关的 VFB 通信。它等于从全局描述里"切"出一块。

是「裁剪 \+ 映射」的结合：

- 映射（Mapping）：System Description 在 Partitioning 阶段已经记录了「每个 SW-C 部署在哪个 ECU」（SW-C→ECU 的部署映射）。
- 裁剪（Cut / Filter）：ECU Extract 依据这套映射，把不属于这个 ECU 的 SW-C 和连接全部过滤掉，只留下本 ECU 相关的部分。

所以本质是 **先有映射、再执行裁剪**——映射提供"该拿哪些"的依据，裁剪执行"切出这一块"的动作。ECU Extract 本身不新增内容，只做摘取。

产出：一份只针对该 ECU 的 ARXML（Ecu Extract），交给该 ECU 的配置工具。RTE 基于它生成这个 ECU 的 RTE——内部通信（同 ECU SW-C 之间）在 ECU 内实现，跨 ECU 的连接会通过 COM/PduR 路由到总线上，而不是生成别的 ECU 的连接。

一句话：System Description 是"全车逻辑描述"，ECU Extract 是按部署映射裁剪出来的"单 ECU 视图"，供 RTE / BSW 配置用。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzcxMDUx><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR