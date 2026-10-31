# AUTOSAR 1000问 · CryptoStackQ2：HSM（Hardware Security Module）和 SHE（Secure Hardware Extension）的区别是什么？在 AUTOSAR 里它们对应哪个模块？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NDY2Mjcy

**AUTOSAR 1000问 · CryptoStackQ2：HSM（Hardware Security Module）和 SHE（Secure Hardware Extension）的区别是什么？在 AUTOSAR 里它们对应哪个模块？**

▎ 五大学习法：费曼——把 HSM vs SHE 讲成「独立安全卫队 vs 门口保安」

**HSM（Hardware Security Module）**

- 一个功能完整的硬件安全模块——独立安全协处理器（如英飞凌 TC3xx 的 HSM，基于 Cortex-M，跑自己固件），有自己的 CPU、内存、加密加速器
- 能力：完整密码学运算、密钥管理（密钥不离开 HSM）、安全存储、安全启动、加解密、签名 / 验签、随机数；可跑独立安全软件栈
- 用于高安全需求：OTA 验签、SecOC、安全访问、安全启动、防盗

**SHE（Secure Hardware Extension）**

- 一个较简单、受限的硬件安全扩展——不是独立 CPU，而是嵌在主 CPU 里的安全增强（常见于车身 MCU）
- 能力：密钥存储（固定密钥槽）、加解密、MAC、随机数等基础功能；比 HSM 弱（无独立 CPU、无完整安全软件栈、性能低）
- 用于中等安全需求：车身节点的 SecOC、简单报文认证

**区别对比**

- 能力：HSM = 独立安全处理器（强、功能全、跑安全栈）；SHE = 嵌入式安全扩展（弱、受限、简单）
- 独立性：HSM 有独立 CPU / 内存 / 固件；SHE 依附主 CPU
- 密钥管理：HSM 支持复杂密钥管理和安全生命周期；SHE 用固定密钥槽、简单
- 应用：HSM 用于高安全（域控 / 网关 / 动力）；SHE 用于中低安全（车身 / 简单节点）

**在 AUTOSAR 里对应哪个模块**

- HSM / SHE 本身不是 AUTOSAR 标准模块，而是「硬件」——它们作为底层密码硬件，被 Crypto Driver 访问
- 两者都通过 Crypto Driver 接入：Crypto Driver 是 Crypto Stack 最底层，访问 HSM / SHE，向上经 CryptoIf → Csm 提供密码服务
- 所以：HSM / SHE 对接到 AUTOSAR 的 Crypto Driver（硬件层），不是独立的标准模块

**一句话总结**：HSM 是「独立安全卫队」（有独立 CPU、跑安全栈、功能全、高安全），SHE 是「门口保安」（嵌入主 CPU、简单受限、中低安全）；在 AUTOSAR 里它们都不是标准模块，而是被 Crypto Driver 访问的底层密码硬件——经 Crypto Stack 的 Driver → CryptoIf → Csm 向上提供密码服务。

📎 CryptoStackQ1（Crypto Stack 分层）→ [https://v.flomoapp.com/mine/?memo\_id=MjU0NDY2MjA3](https://v.flomoapp.com/mine/?memo_id=MjU0NDY2MjA3)<br>
📎 AUTOSAR 1000问总表 → [https://v.flomoapp.com/mine/?memo\_id=MjMxMTQ2NDk4](https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4)

#Area/技术/AUTOSAR