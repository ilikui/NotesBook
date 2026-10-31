# Partial Network Cluster 配置：一个支持 PN 的 ECU 靠「PN 位匹配」判断该不该醒

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzcwNzgw

Partial Network Cluster 配置：一个支持 PN 的 ECU 靠「PN 位匹配」判断该不该醒

配置链路四步：

1. 划 Cluster、分 PNC 号：把整车 ECU 按功能分组（如门窗组、动力组、诊断组），每组一个 PNC（Partial Network Cluster）号，是配置里的逻辑身份。

2. 给 ECU 配 filter mask：每个 ECU 声明自己属于哪些 PNC——PnMask（掩码）。收报文时硬件只对「命中自己 mask 的 PNC 位」产生唤醒。

3. 给报文配 PNC 位：发送端在 CAN ID 预留位打上所属 PNC 号。这样一条报文醒来的是「它标记的那个 group」，不是全网。

4. 硬件做匹配：靠带 PN 支持的收发器/控制器（如 TJA1145 这类）在报文仲裁段解析 PNC 位，跟本 ECU 的 mask 比对。命中 → 唤醒 ECU 走正常接收；不命中 → 报文丢弃、ECU 继续睡，静态电流不掉。


软件侧配合：CanNm（PN 相关 NM 报文）、CanIf/CanTrcv（PN filter 配置）、EcuM（PN 唤醒源）。配置工具里主要落在 CanNm、CanTrcv、CanIf 的 PnMask / PncId 参数上。

一句话：PN Cluster 是「按功能把 ECU 分组」，mask 是「ECU 声明自己是哪组的」，报文 PNC 位是「这条消息想唤醒哪组」，硬件负责把三者对上。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzcwNDc5><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR