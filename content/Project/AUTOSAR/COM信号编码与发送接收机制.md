---
title: COM 信号编码与发送接收机制
tags:
  - Project
  - AUTOSAR
  - CP
  - COM
  - CAN
---

# COM 信号编码与发送接收机制

> [!info] 本专题解决什么问题
> 面对“CANoe 原始字节正确，但应用值不对”“Rte_Write 已调用但总线上没有帧”“接收信号一直是旧值”等问题，能从信号定义、位布局、I-PDU、发送控制与接收监控逐层找到证据。

## 1. COM 在通信链路中的位置

~~~mermaid
flowchart LR
    A["SWC / RTE"] --> B["COM Signal"]
    B --> C["COM I-PDU"]
    C --> D["PduR"]
    D --> E["CanIf"]
    E --> F["CanDrv / CAN"]
~~~

COM 负责面向信号的数据处理；PduR 负责按配置路由 PDU；CanIf 负责 CAN 接口抽象。COM 不负责定义整车业务语义，也不直接决定物理 CAN 仲裁是否成功。

## 2. 先区分四种数据表示

| 层次 | 示例 | 需要确认的内容 |
| --- | --- | --- |
| 应用值 | 车速 123.4 km/h | 单位、范围、有效性 |
| 原始信号值 | Raw = 1234 | 位宽、有无符号、枚举与保留值 |
| I-PDU 字节 | 例如 `D2 04 00 00` | 信号起始位、长度、端序、填充值 |
| CAN 帧 | CAN ID、DLC、Data | ID 类型、DLC、发送周期与总线状态 |

常见物理值换算公式：

~~~text
PhysicalValue = RawValue * Factor + Offset
RawValue = (PhysicalValue - Offset) / Factor
~~~

反向换算时还要考虑取整规则、饱和范围、无效值与可表示范围。不能只用浮点公式推断最终编码字节。

## 3. 位宽、端序与符号属性

### 3.1 位宽与范围

对无符号 N 位原始值，理论范围为：

~~~text
0 .. (2^N - 1)
~~~

对二进制补码有符号 N 位值，理论范围为：

~~~text
-2^(N-1) .. (2^(N-1) - 1)
~~~

例如 12 位无符号值最大为 4095；12 位有符号值范围为 -2048 到 2047。若配置值超出可表示范围，工具或生成代码如何处理取决于配置和实现，必须验证而不是假设会自动饱和。

### 3.2 Intel / Little Endian 与 Motorola / Big Endian

- **Little Endian（常被称为 Intel 格式）**：多字节数值中，低有效字节位于较低字节地址。
- **Big Endian（常被称为 Motorola 格式）**：多字节数值中，高有效字节位于较低字节地址。
- **Start bit 不能脱离工具约定理解**：DBC、AUTOSAR 模型、通信矩阵编辑器和生成器界面可能采用不同的位编号展示方式，尤其是 Motorola 信号的起始位表示。应使用项目实际配置与工具导出的解码结果交叉验证。

以两个数据字节 `34 12` 为例，若定义为 16 位小端无符号整数，则 Raw = `0x1234` = 4660。这个例子只说明字节序，不代表任意项目的信号起始位或 Motorola 映射规则。

### 3.3 手工解码的可靠步骤

1. 从 CANoe Trace 复制完整 Data 字节和 DLC。
2. 找到信号定义：起始位、长度、端序、符号属性。
3. 按项目采用的位编号规则提取原始值；Motorola 信号优先使用通信矩阵工具或经过单元测试的解码器交叉核验。
4. 应用符号扩展、Factor 和 Offset。
5. 处理无效值、保留值、枚举、范围限制和单位。
6. 与 ECU 内部 Raw 值和 Physical 值比较，记录误差和采样时间。

不要仅凭信号名称或十六进制字节“看起来合理”就判定解码正确。

## 4. COM 发送流程

~~~mermaid
sequenceDiagram
    participant SWC as SWC Runnable
    participant RTE as RTE
    participant COM as COM
    participant PDUR as PduR
    participant CANIF as CanIf
    participant BUS as CAN Bus
    SWC->>RTE: 写入 DataElement
    RTE->>COM: 更新映射的信号数据
    COM->>COM: 更新信号 / I-PDU 缓存
    COM->>COM: 判断发送模式与触发条件
    COM->>PDUR: 请求发送 I-PDU
    PDUR->>CANIF: 路由发送请求
    CANIF->>BUS: 经驱动提交 CAN 帧
~~~

以上是逻辑路径示意。具体 API、缓存更新时间、发送触发点与确认机制由 AUTOSAR Release、配置方式和供应商实现决定。

### 发送排查清单

- [ ] Runnable 确实执行，写入前后的值符合预期。
- [ ] RTE Port、DataElement、System Mapping 与生成接口匹配。
- [ ] COM Signal 指向正确的 I-PDU，位布局与数据类型一致。
- [ ] I-PDU Group 已启动，发送方向未被模式控制禁用。
- [ ] 发送模式、周期、重复次数、最小延迟和触发条件符合设计。
- [ ] PduR 源 / 目标 PDU 与 CanIf Tx PDU 映射正确。
- [ ] CanIf 控制器 / PDU 模式与 CanDrv 状态允许发送。
- [ ] CANoe Trace 中确认实际 CAN ID、DLC、Data 和周期。

## 5. COM 接收流程

~~~mermaid
sequenceDiagram
    participant BUS as CAN Bus
    participant CANIF as CanIf
    participant PDUR as PduR
    participant COM as COM
    participant RTE as RTE
    participant SWC as Consumer Runnable
    BUS->>CANIF: 接收帧
    CANIF->>PDUR: Rx PDU 指示
    PDUR->>COM: 转发目标 I-PDU
    COM->>COM: 解包并更新信号缓存
    COM->>RTE: 提供信号数据 / 状态
    RTE->>SWC: 消费者读取数据
~~~

接收侧应分开验证三个问题：帧是否抵达 ECU、COM 信号是否更新、SWC 是否在预期时刻读取到更新值。三个问题对应不同的故障边界。

## 6. 发送模式、触发与确认

项目常见的发送行为包括周期发送、直接触发、混合模式，以及由配置和 API 触发的发送请求。排查时不要只看一个“周期时间”参数，还要核对：

- I-PDU 的发送模式选择与触发条件。
- 信号更新是否按预期触发 I-PDU，或只更新缓存等待周期发送。
- 重复发送与最小延迟等参数。
- I-PDU Group 启停与通信模式控制。
- Tx Confirmation 是否按预期到达，以及它代表的层次。

**Tx Confirmation 不等于接收 ECU 的业务逻辑已经处理成功。** 它只能说明对应发送链路到达了该确认机制定义的阶段；应用层接收和处理需要独立证据。

## 7. 接收超时、更新指示与无效值

这些机制目的不同，不要混为一谈：

| 机制 | 要回答的问题 | 典型排查证据 |
| --- | --- | --- |
| Rx Deadline Monitoring / Timeout | 期望的接收更新是否在规定时间内到达？ | 超时计数、通知回调、替代行为、时间戳 |
| Update indication / update bit（若配置） | 该信号或数据是否按配置标记为更新？ | I-PDU 原始字节、更新位定义、COM 状态 |
| Invalid value / invalidation | 收到或写入的数据是否被定义为无效？ | 信号定义、原始值、无效值策略 |
| Signal filtering | 当前值是否满足配置的过滤 / 通知条件？ | 过滤参数、前后值、通知调用 |
| Initial value / substitution | 初始化或超时后使用什么数据？ | 初始化顺序、替代值配置、状态切换 |

超时不一定意味着数据被自动清零；无效值也不一定等于超时。最终行为必须对照项目需求、COM 配置与生成代码。

## 8. 最小 C 代码：物理值与原始值转换

下面的代码演示通用的 16 位无符号线性转换，不是 AUTOSAR 生成代码，也不代替 COM 的位打包。工程使用时应把 Factor、Offset、量程和舍入策略替换为接口定义中的真实值。

~~~c
#include <stdbool.h>
#include <stdint.h>
#include <math.h>

typedef struct
{
    double factor;
    double offset;
    uint16_t raw_min;
    uint16_t raw_max;
} LinearSignalConfig;

bool PhysicalToRawU16(double physical,
                      const LinearSignalConfig *cfg,
                      uint16_t *raw)
{
    double value;
    double rounded;

    if ((cfg == 0) || (raw == 0) ||
        (cfg->factor <= 0.0) ||
        (cfg->raw_min > cfg->raw_max))
    {
        return false;
    }

    value = (physical - cfg->offset) / cfg->factor;

    if (!isfinite(value))
    {
        return false;
    }

    /* 此处选择拒绝越界；项目也可能规定饱和或错误替代策略。 */
    if ((value < (double)cfg->raw_min) ||
        (value > (double)cfg->raw_max))
    {
        return false;
    }

    /* 四舍五入到最近整数；需与项目通信矩阵的量化规则一致。 */
    rounded = floor(value + 0.5);

    if ((rounded < (double)cfg->raw_min) ||
        (rounded > (double)cfg->raw_max))
    {
        return false;
    }

    *raw = (uint16_t)rounded;
    return true;
}

bool RawU16ToPhysical(uint16_t raw,
                      const LinearSignalConfig *cfg,
                      double *physical)
{
    if ((cfg == 0) || (physical == 0) ||
        (cfg->factor <= 0.0) ||
        (raw < cfg->raw_min) ||
        (raw > cfg->raw_max))
    {
        return false;
    }

    *physical = ((double)raw * cfg->factor) + cfg->offset;
    return isfinite(*physical);
}
~~~

注意事项：

- 该示例需要链接数学库（例如某些工具链中的 `-lm`），具体取决于编译器和运行库。
- 负数、无符号与有符号信号、非线性信号、枚举和无效值需要独立策略。
- 转换成功只代表数值转换成功，不代表 COM 信号映射、I-PDU 打包或 CAN 发送成功。

## 9. 常见故障定位矩阵

| 现象 | 最可能的检查方向 | 能证明问题边界的证据 |
| --- | --- | --- |
| 物理值与 Trace 解码值存在固定比例偏差 | Factor、单位、Raw / Physical 混淆 | 原始值、Factor、Offset、单位定义 |
| 值偏移固定 | Offset、默认值、信号定义版本 | 计算过程与配置差异 |
| 只有部分值错误 | 位宽、符号扩展、越界、枚举 / 保留值 | 边界值测试、Raw 值与类型 |
| Motorola 信号解码错误 | 起始位编号、位跨字节规则、工具约定 | 配置导出、已知测试向量、独立解码结果 |
| RTE 写入正确但帧没有出现 | 发送模式、I-PDU Group、PduR / CanIf、控制器状态 | 分层计数、返回值、Trace |
| 帧周期不符合预期 | 周期模式、直接触发、重复发送、最小延迟、任务时序 | Trace 时间戳与配置 |
| 接收帧正确但应用值不变 | Rx PDU 路由、COM 解包、超时 / 过滤、RTE 连接与调度 | 同一帧的 Raw、COM、SWC 观测值 |
| 通信停止后应用仍保留旧值 | Timeout 配置、替代值策略、通知处理 | 停止发送前后时间线、超时状态与应用策略 |

## 10. 推荐测试向量

对每个关键数值信号，至少准备以下测试：

- 最小合法值、最大合法值、中间典型值。
- 0、1、位边界值（如 7/8、15/16 等，按位宽选择）。
- 有符号信号的 -1、最小负值、最大正值。
- 无效值、保留值和超量程值。
- 多字节跨边界值，用于验证端序和位布局。
- 超时前后、I-PDU Group 停止 / 启动前后。
- 在 Trace 与 ECU 内部观测点同步记录的测试。

测试向量应同时写明预期 Raw、预期 Physical、预期 Data 字节和有效性状态，才能形成可复现的验证证据。

## 相关笔记

- [[规范模块/COM]]
- [[规范模块/RTE]]
- [[规范模块/PDURouter]]
- [[规范模块/CANInterface]]
- [[通信栈工程实战与 CANoe 验证]]
- [[AUTOSAR 故障排查手册]]
