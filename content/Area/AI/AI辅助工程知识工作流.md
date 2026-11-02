---
title: AI辅助工程知识工作流：MCP、需求追溯与工具化
tags:
  - AI工程
  - MCP
  - 需求追溯
  - 汽车电子
---

# AI辅助工程知识工作流：MCP、需求追溯与工具化

AI 工具的工程价值不在于“接入了模型”，而在于能否把需求、代码、证据、测试和知识连接起来，并让结果可复核、可追踪。

## 一、MCP 的定位

Model Context Protocol（MCP）是一种让 AI 应用以统一方式访问外部工具和上下文的开放协议。它不是模型本身，也不等于 Agent 框架。

| 概念 | 主要职责 |
|---|---|
| LLM | 理解输入、生成文本或结构化输出 |
| MCP Host | 承载 AI 交互的应用，例如支持 MCP 的编辑器或桌面应用 |
| MCP Client | Host 内负责连接 MCP Server 的协议客户端 |
| MCP Server | 对外提供 Tools、Resources、Prompts 等能力 |
| Agent | 在目标约束下组织模型、工具和状态的执行逻辑 |

~~~~mermaid
flowchart LR
  H[AI Host / IDE] --> C[MCP Client]
  C <-->|MCP 协议| S[MCP Server]
  S --> T[Tools：查询 / 分析 / 校验]
  S --> R[Resources：模型 / 文档 / 元数据]
  S --> P[Prompts：可复用任务模板]
  T --> D[本地文件 / Git / 测试系统]
~~~~

### 传输方式与安全边界

- **stdio**：适合本机开发和单用户工具；Host 启动 Server 子进程，通过标准输入输出通信。
- **Streamable HTTP**：适合远程服务或多客户端接入；应配置身份认证、TLS、访问控制、速率限制和审计。
- 不要把本地开发配置直接复制到生产环境；Host 对配置文件格式、字段和支持的协议版本可能随版本变化。
- Server 只开放完成任务所需的最小工具权限；写文件、执行命令、访问网络等能力应单独授权和记录。
- 不要将访问令牌、客户数据、内部源代码或受限工程文档发送到未获批准的模型或服务。

### 一个可逐步落地的 MCP 项目

先做只读、低风险的单一工具，再扩展，不要一开始就搭建复杂的“全能 Agent”。

| 阶段 | 最小交付 | 验收方式 |
|---|---|---|
| 1. 本地启动 | 一个 stdio Server | Host 能连接并列出工具 |
| 2. 只读查询 | 查询本地知识条目或项目元数据 | 输入输出可预测，错误可解释 |
| 3. 结构化结果 | 返回 JSON，包含来源和状态 | Schema 校验通过 |
| 4. 工程工具 | 需求检索、代码定位、静态检查摘要 | 每条结果可回到原始文件 |
| 5. 受控写入 | 生成草稿或补丁，不自动覆盖 | 人工审阅后再合并 |
| 6. 团队部署 | HTTP 服务、鉴权、审计和监控 | 权限测试与故障演练通过 |

示例项目结构（仅作组织参考，实际 SDK API 与配置以所用版本文档为准）：

~~~~text
engineering-mcp/
├── server/
│   ├── main.py
│   ├── tools/
│   │   ├── search_requirements.py
│   │   ├── locate_implementation.py
│   │   └── summarize_test_evidence.py
│   └── schemas/
├── tests/
├── docs/
└── pyproject.toml
~~~~

## 二、需求—代码—测试追溯

需求追溯的核心是建立可验证的映射，不是单纯画一张关系图。

| 实体 | 建议字段 | 示例 |
|---|---|---|
| Requirement | id、版本、来源、正文、状态 | REQ-COM-012 |
| Implementation | repo、commit、path、symbol | src/Com/Com.c::Com_MainFunction |
| Test | test_id、环境、结果、日志链接 | TC-COM-034 |
| Relation | from、to、关系类型、证据、置信状态 | implemented_by / verified_by |

~~~~mermaid
flowchart TD
  R[系统 / 软件需求] -->|分解| D[详细设计]
  D -->|实现于| C[代码文件与符号]
  C -->|验证于| T[单元 / 集成测试]
  T --> E[测试报告与原始证据]
  R -->|变更影响分析| I[受影响设计、代码、测试]
  I --> V[人工确认与变更评审]
~~~~

### 推荐的 MVP

1. 选择一个边界清晰的模块，不要一开始覆盖整个 ECU。
2. 从受控版本的需求文档中提取稳定 ID，保留文档版本和段落定位。
3. 通过符号索引、静态分析或人工确认定位代码，不让模型凭函数名猜实现。
4. 将映射保存为 JSON/YAML 或数据库记录，并记录 Git commit、工具版本和证据位置。
5. 生成需求树、调用链和测试覆盖视图。
6. 对低置信度、缺少证据或一对多映射标记为“待确认”，不自动判定已实现。
7. 在需求或代码变更时，仅提示可能受影响的映射，由工程师审核。

示例映射记录：

~~~~json
{
  "requirement_id": "REQ-COM-012",
  "requirement_revision": "1.3",
  "implementation": [
    {
      "repository": "example-ecu",
      "commit": "REPLACE_WITH_REVIEWED_COMMIT",
      "path": "src/Com/Com.c",
      "symbol": "Com_MainFunction"
    }
  ],
  "tests": ["TC-COM-034"],
  "relation_status": "needs_review",
  "evidence": ["docs/test-report/TC-COM-034.pdf"],
  "reviewed_by": null
}
~~~~

> 这类映射可以辅助 ISO 26262 / ASPICE 项目的追溯和评审准备，但工具生成的关系本身不等于合规证据。需求正确性、实现符合性、验证充分性和配置管理仍需按项目流程评审。

## 三、将 AI 放进工程闭环

~~~~mermaid
flowchart TD
  A[需求 / 缺陷 / 变更] --> B[检索相关资料]
  B --> C[定位代码与配置]
  C --> D[生成候选解释和影响范围]
  D --> E[静态检查 / 测试 / 实验]
  E --> F{证据是否充分？}
  F -->|否| B
  F -->|是| G[工程师评审]
  G --> H[提交变更与追溯记录]
  H --> I[知识库沉淀]
~~~~

AI 输出至少应包含：结论、依据、来源位置、适用版本、未确认事项和下一步验证建议。不要只保留一段没有来源的自然语言总结。

## 四、相关实践

- 先验证检索质量，再考虑向量数据库和 RAG。
- 先生成只读报告，再考虑自动修改代码。
- 对模型生成的代码、测试用例和需求映射执行与人工产物同等的评审和验证。
- 对每个自动化步骤记录输入版本、工具版本、输出和人工确认状态。

## 参考入口

- [MCP 官方规范](https://github.com/modelcontextprotocol/specification)
- [MCP 官方文档](https://modelcontextprotocol.io/)
- [VS Code MCP 文档](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)

## Flomo 来源

- MCP in VS Code 技术方案：https://v.flomoapp.com/mine/?memo_id=MjU3NTg0ODY5
- MCP 全景方案：https://v.flomoapp.com/mine/?memo_id=MjU3Mzc2NTg4
- AI 需求与代码索引方案：https://v.flomoapp.com/mine/?memo_id=MjU3MzczMTYy
