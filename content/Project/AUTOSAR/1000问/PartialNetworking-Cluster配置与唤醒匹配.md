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

## 关键更正：PNC 位不等于 CAN ID 仲裁字段

原笔记中“在 CAN ID 预留位打上 PNC 号”的说法不准确。AUTOSAR CAN Partial Networking 的 PNC 信息通常以 **PNC bit vector** 形式承载在配置的 NM PDU 用户数据区域；CAN ID 用于标识 NM 报文/网络，不是把 PNC 编号直接塞进仲裁 ID 的通用做法。

应区分：
- **PNC**：Partial Network Cluster，逻辑网络功能组。
- **PNC bit vector**：NM PDU 中表示哪些 PNC 被请求/激活的位向量。
- **PN filter / selective wake-up**：支持 PN 的收发器根据配置的 CAN ID、数据字节位置和掩码等过滤条件决定是否唤醒；过滤规则由收发器能力和项目配置决定。
- **CanNm / ComM / CanIf / CanTrcv / EcuM**：软件侧处理 NM、通信模式、收发器模式和唤醒原因；具体职责与接口取决于 AUTOSAR Release 和供应商实现。

**验证方法：** 检查 NM PDU 的 PNC bit vector 布局、PNC 映射表、收发器 selective-wakeup filter 配置；用 CANoe 发送命中/不命中的 NM 报文，并测量 ECU 是否唤醒、唤醒原因和休眠电流。不要只改 CAN ID 位来模拟 PNC。