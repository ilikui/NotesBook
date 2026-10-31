---
title: 车载通信1000问：SPI Flash、I2C EEPROM、RS485、SENT与USB
tags:
  - 车载通信
  - 1000问
  - SPI
  - I2C
---

# 车载通信1000问：SPI Flash、I2C EEPROM、RS485、SENT与USB

本篇迁移车载通信协议系列第二批 11 道问答，覆盖非易失存储、串行总线、差分通信、汽车传感器协议和 USB。具体时序、器件容量和电气参数必须以芯片数据手册与项目网络规范为准。

## 16. SPI NOR Flash 和 NAND Flash 有什么区别？

**答案：** NOR Flash 支持较方便的随机读取，适合存放代码、配置和需要直接读取的固件；NAND Flash 密度高、成本/容量比有优势，适合大容量数据存储，但通常需要 ECC、坏块管理和更复杂的控制器。

SPI NOR 常用于 MCU Bootloader 和固件镜像；NAND 常见于更大容量存储系统。不能只凭“SPI”判断 Flash 类型，SPI 是接口，NOR/NAND 是存储阵列结构。

## 17. SPI 的 CPOL、CPHA 如何决定采样边沿？

**答案：**

- CPOL：定义时钟空闲电平。
- CPHA：定义数据在第一个还是第二个时钟边沿采样。
- Mode 0–3 对应四种组合。

主从设备必须配置一致，否则可能出现首位错位、读值固定或数据随机错误。SPI 通常由主机提供 SCLK 和片选，常见全双工收发，但具体器件可能只支持单向或半双工。

~~~~mermaid
flowchart LR
  A[MCU SPI Master] -->|SCLK / CS / MOSI| B[Flash / Sensor Slave]
  B -->|MISO| A
  A --> C[CPOL / CPHA / Bit Order]
  C --> B
~~~~

## 18. SPI NOR Flash 为什么要先擦除再写入？Page Program 和 Sector Erase 有什么区别？

**答案：** NOR Flash 编程通常只能把 bit 从 1 改成 0；若要把 0 恢复成 1，需要擦除更大的块。Page Program 在页范围内写入，Sector/Block Erase 按扇区或块擦除。

因此更新一个小数据结构时，不能假设可以直接覆盖任意字节。常见做法是读出整块、修改缓冲区、擦除块、重写数据，并考虑掉电原子性和写入磨损。

## 19. Flash 的擦写寿命为什么有限？Wear Leveling 如何工作？

**答案：** Flash 单元经历编程/擦除会逐渐退化，擦写次数达到器件规格后可靠性下降。Wear Leveling 通过把写入分散到不同物理块，避免某个固定块过早耗尽。

- 静态磨损均衡：必要时搬迁长期不变的数据。
- 动态磨损均衡：新写入优先分配到擦写次数较少的块。
- 还需结合坏块管理、ECC、掉电恢复和元数据冗余。

## 20. I2C 为什么需要上拉电阻？ACK/NACK 如何表示？

**答案：** I2C 的 SDA/SCL 通常采用开漏/开集电极结构，器件只能主动拉低总线，释放后由上拉电阻拉高。这样可实现线与和多主机仲裁。ACK 通常在第九个时钟由接收方拉低 SDA；NACK 则保持高电平。

上拉电阻过大可能导致上升沿过慢，过小会增加低电平灌电流。应结合总线电容、速率、器件灌电流能力和标准模式/快速模式时序计算。

~~~~mermaid
sequenceDiagram
  participant M as Master
  participant S as Slave
  M->>S: START + Address + R/W
  S-->>M: ACK / NACK
  M->>S: Data Byte
  S-->>M: ACK / NACK
  M->>S: STOP
~~~~

## 21. I2C EEPROM 为什么写入后需要等待？Page Write 有什么限制？

**答案：** EEPROM 内部写入需要一定编程时间，写周期内器件可能不响应普通访问。主机可按数据手册采用固定等待或 ACK Polling 判断写入完成。

Page Write 通常不能跨越页边界；若一次写入长度超过当前页剩余空间，部分器件会回卷到本页开头覆盖数据。驱动应按页边界拆分写入，并验证写后数据。

## 22. RS485 为什么适合工业/车载长距离通信？终端电阻和偏置电阻怎么放？

**答案：** RS485 使用差分信号传输，对共模干扰有较强抑制能力，适合多节点和较长线路。总线通常采用线型拓扑，在物理总线两端按电缆特性阻抗配置终端电阻；偏置网络用于总线空闲时建立确定的差分状态，通常按系统设计集中配置，避免多处重复偏置造成负载过重。

不要把星型拓扑、任意支线和过多终端电阻当作默认接法。布线长度、波特率、节点负载和收发器规格都影响可靠性。

## 23. Modbus RTU 的帧如何判断边界？CRC 用来做什么？

**答案：** Modbus RTU 通常通过帧间静默时间区分报文边界，常见规范要求约 3.5 个字符时间的静默间隔；帧中包含地址、功能码、数据和 CRC。CRC 用于检测传输错误，不提供身份认证或加密保护。

波特率较高时，字符时间较短，具体帧间隔和超时实现应按 Modbus 规范及设备文档核对。

## 24. SENT 是什么协议？它和 PWM 有什么不同？

**答案：** SENT（Single Edge Nibble Transmission）是汽车传感器常见的单线数字通信协议，通常由传感器发送 ECU 接收。它用脉冲边沿间隔/脉冲长度编码数据 nibble，并通过同步/校准脉冲建立时间基准。

SENT 不是普通固定频率 PWM：PWM 常用占空比表达数值，SENT 主要通过脉冲时间编码数据帧。诊断时需检查时钟刻度、同步脉冲、数据 nibble、状态位和 CRC。

## 25. USB 枚举（Enumeration）时主机做了什么？

**答案：** USB 设备连接后，主机检测连接状态并复位端口，读取设备描述符、配置描述符、接口描述符和端点描述符，分配地址并选择配置。描述符告诉主机设备类别、支持的配置、接口和端点能力。

USB 的角色是 Host 与 Device：Host 负责总线调度，Device 响应请求。设备不能仅靠插入就任意发送数据，必须按 USB 协议完成枚举和传输安排。

## 26. USB 的 Control、Bulk、Interrupt、Isochronous 四种传输类型怎样选择？

**答案：**

- Control：用于枚举、配置和控制命令，具有可靠交付机制。
- Bulk：用于大量数据传输，重视可靠性但不保证固定带宽/时延。
- Interrupt：用于周期性轮询的小量数据，适合键盘、鼠标等低延迟输入。
- Isochronous：为音视频等实时流预留带宽，强调时间连续性，不保证错误重传。

选择应根据数据量、延迟、带宽和错误恢复要求，而不是仅按“速度快慢”排序。

## Flomo 原始来源

- 车载通信协议 1000 问总表：https://v.flomoapp.com/mine/?memo_id=MjQ2Mzc0NjYw
- SPI Flash：https://v.flomoapp.com/mine/?memo_id=MjQ5MDc4OTky
- I2C EEPROM：https://v.flomoapp.com/mine/?memo_id=MjQ5MDc5MDY4
- RS485：https://v.flomoapp.com/mine/?memo_id=MjQ5MDc5MTAz
- SENT：https://v.flomoapp.com/mine/?memo_id=MjQ5NTIwODI2
- USB：https://v.flomoapp.com/mine/?memo_id=MjQ5NTIwODgw
