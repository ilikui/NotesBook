---
title: AI 项目实战路线
tags:
  - AI
  - 项目实战
  - 学习路线
---

# AI 项目实战路线

本路线用项目验证能力，而不是按“看完多少课程”衡量进度。每个项目都要提交代码、README、数据说明、实验结果、错误分析和可复现步骤。

## 项目阶梯

| 阶段 | 项目 | 核心能力 | 完成标准 |
|---|---|---|---|
| 入门 | 鸢尾花/房价预测 | Python、数据清洗、基线 | 可运行脚本、指标与图表 |
| 机器学习 | 客户流失/信用风险分类 | Pipeline、交叉验证、阈值 | PR-AUC、混淆矩阵、错误分析 |
| 深度学习 | Fashion-MNIST/CIFAR 分类 | PyTorch、训练循环、调参 | checkpoint、曲线、混淆矩阵 |
| NLP | 文本分类/语义检索 | Tokenizer、Embedding、评估 | 固定测试集与错误样本 |
| LLM | 文档问答 RAG | 切分、召回、重排、引用 | 引用可核验、无证据可拒答 |
| Agent | 工具调用工作流 | 状态、工具权限、异常处理 | 可追踪执行、人工确认边界 |
| 进阶 | 论文复现 | 阅读论文、复现实验、消融 | 与论文设置差异说明及复现报告 |
| 工程 | 模型服务与监控 | API、容器、监控、成本 | 健康检查、延迟与错误率指标 |

## 统一项目目录

```text
project/
├── README.md
├── pyproject.toml          # 或 requirements.txt
├── configs/
│   └── baseline.yaml
├── data/
│   └── README.md           # 数据来源与许可证，不提交受限原始数据
├── notebooks/
│   └── exploration.ipynb
├── src/
│   ├── data.py
│   ├── features.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── tests/
├── reports/
│   ├── metrics.json
│   └── error-analysis.md
└── models/                 # 大模型文件通常不直接提交 Git
```

## 项目 README 必须回答

1. 要解决什么问题？谁会使用结果？
2. 数据从哪里来？许可证和隐私限制是什么？
3. 如何安装依赖、准备数据和运行训练？
4. 训练/验证/测试如何划分？是否存在时间或实体泄漏？
5. 与 Dummy/简单基线相比提升多少？
6. 指标如何定义？为何适合业务目标？
7. 哪些样本预测失败？错误有什么规律？
8. 实验使用什么硬件、随机种子和模型版本？
9. 已知局限性是什么？哪些用途不适合？

## 实验记录模板

每次实验建议记录以下字段：

| 字段 | 示例/说明 |
|---|---|
| experiment_id | exp-001 |
| git_commit | 对应代码提交 |
| dataset_version | 数据快照或版本号 |
| split | 随机/分组/时间切分 |
| seed | 随机种子 |
| model | 模型与架构版本 |
| config | 超参数配置文件 |
| metrics | 主指标及辅助指标 |
| runtime | 训练时间、硬件、显存 |
| notes | 偏差、失败样本、下一步 |

## 12 周参考安排

- 第 1–2 周：Python、NumPy、Pandas、可视化；完成数据分析项目。
- 第 3–4 周：回归、分类、交叉验证和模型解释；完成表格数据项目。
- 第 5–7 周：PyTorch、MLP、CNN、优化器和正则化；完成图像分类项目。
- 第 8–9 周：Transformer、Tokenizer、Embedding；完成文本任务。
- 第 10–11 周：RAG、评估、引用和权限；完成文档问答。
- 第 12 周：整理代码、复现实验、编写技术报告和演示。

实际节奏应根据每周可投入时间调整；不要为了赶进度跳过评估和数据合规。

## 代码质量与交付检查

- [ ] 新环境按 README 能从零运行。
- [ ] 数据来源、版本和许可证已记录。
- [ ] 训练、验证、测试职责明确，无数据泄漏。
- [ ] 有简单基线和合理指标。
- [ ] 固定随机种子并记录环境；说明无法完全复现的因素。
- [ ] 有测试、日志、配置和模型版本。
- [ ] 报告失败案例、局限性和潜在偏差。
- [ ] 不提交密钥、隐私数据、受限数据和超大模型权重。

## 推荐项目资源

- [scikit-learn Examples](https://scikit-learn.org/stable/auto_examples/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [Hugging Face Learn](https://huggingface.co/learn)
- [Made With ML](https://madewithml.com/)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/)
- [Papers with Code](https://paperswithcode.com/)

## 相关

- [[人工智能]]
- [[机器学习实验手册]]
- [[深度学习实验手册]]
- [[大模型与RAG实战手册]]
- [[AI工程与部署]]
- [[AI论文与数据集]]
