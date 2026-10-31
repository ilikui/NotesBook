---
title: 专栏⑳·第9篇：网络安全——SecOC、HSM、OTA 安全
tags:
  - 自动驾驶
  - 专题系列
---

# 专栏⑳·第9篇：网络安全——SecOC、HSM、OTA 安全

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjUyMTU1OTU5

**专栏⑳·第9篇：网络安全——SecOC、HSM、OTA 安全**

▎ **为什么自动驾驶必须谈安全**<br>
车变成联网节点：OTA 刷写、V2X、远程诊断——攻击面打开。自动驾驶控制指令被篡改 = 直接安全事故。ISO 21434（汽车网络安全工程）。

▎ **四类威胁与对策**

1. 通信被伪造（CAN 报文注入）→ SecOC：报文认证（CMAC）+ 新鲜度值（防重放）——接时间同步专题
2. 固件被篡改 → 安全启动（Secure Boot）+ 签名校验——信任链
3. OTA 被劫持 → 双向认证 + 加密传输 + 回滚机制
4. 调试口被利用 → 安全调试、HSM 保护密钥

▎ **SecOC 详解（你 AUTOSAR 里的老朋友）**

- 认证：发送方用密钥对报文算 CMAC（截断 MAC），接收方验证——防伪造 / 篡改
- 新鲜度：计数器 / 时间戳——防重放（接 StbM 时间同步）
- 密钥管理：HSM 存密钥，认证在硬件里做——密钥不出安全域

▎ **HSM（硬件安全模块）**

- 独立安全岛：密钥存储、加解密、安全启动、随机数——主核被攻破密钥也不泄露
- TC3xx 的 HSM、AUTOSAR 的 Crypto Stack（CSM / Crypto Driver）就是这套

▎ **三个坑**

1. 只做 SecOC 不做密钥管理：密钥硬编码在 Flash——逆向一次全废；密钥必须进 HSM
2. 新鲜度值设计错误：单调计数器被回滚（rollback）——防重放失效；要和功能安全联动
3. OTA 没有回滚：新固件带 bug 直接变砖（你专栏⑦的 97% 案例）——A/B 分区 + 回滚是底线

▎ **一句话**：网络安全 = 通信认证（SecOC）+ 固件信任链（Secure Boot）+ OTA 安全 + HSM 密钥守护；SecOC 的新鲜度值正是吃 StbM 时间戳——你时间同步专题和它是一套系统。

📎 时间同步专题导航（SecOC 时间戳）→ [https://v.flomoapp.com/mine/?memo\_id=MjUxMjAzOTEx](https://v.flomoapp.com/mine/?memo_id=MjUxMjAzOTEx)<br>
📎 专栏⑦ Bootloader 导航（OTA / 变砖）→ [https://v.flomoapp.com/mine/?memo\_id=MjQ5MDI0OTQ1](https://v.flomoapp.com/mine/?memo_id=MjQ5MDI0OTQ1)<br>
📎 第6篇：通信底座 → [https://v.flomoapp.com/mine/?memo\_id=MjUyMTU1ODc2](https://v.flomoapp.com/mine/?memo_id=MjUyMTU1ODc2)

**专栏⑳进度：9/10篇**

#Area/技术/自动驾驶