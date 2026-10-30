---
title: AI 书籍与课程
tags:
  - AI
  - 书籍
  - 课程
---

# AI 书籍与课程

本页整理人工智能领域的经典教材、工程实践书籍、前沿方向读物与公开课程。书籍按知识主题归档，优先链接作者、出版社、官方配套代码和合法在线阅读入口。

> [!warning] 关于电子书下载与版权
> GitHub 中只收录书目信息、官方购买/试读入口、作者公开的合法全文，以及配套代码和课程。出版社付费电子书、受版权保护的 PDF/EPUB 不复制到仓库，也不提供未经授权的网盘或盗版下载地址。页面标注“免费在线版”时，表示作者或出版社公开提供阅读/下载；仍应遵守原站许可。

## 一、本次精选：十本 AI 进阶书单

这十本书覆盖机器学习原理、Transformer、大模型、AI 工程、知识图谱、生成模型、强化学习、AI 评估与安全，以及边缘设备部署。建议按学习目标选读，不必一次读完。

### 1. Why Machines Learn

- **作者**：Anil Ananthaswamy
- **主题**：机器学习原理、数学直觉、算法思想
- **推荐理由**：从数学与科学思想解释机器如何学习，帮助建立对机器学习底层机制的整体理解。
- **阅读入口**：[Princeton University Press 图书页](https://press.princeton.edu/books/hardcover/978069124્ઠ?utm_source=notesbook)（请以出版社检索页为准）、[Google Books 检索](https://books.google.com/books?q=Why+Machines+Learn+Anil+Ananthaswamy)
- **建议配合**：[[数学与Python基础]]、[[机器学习]]

### 2. Hands-On Large Language Models

- **作者**：Jay Alammar、Maarten Grootendorst
- **主题**：Token、Embedding、Transformer、语义搜索、生成模型
- **推荐理由**：通过可视化和代码案例解释大语言模型的关键组件，适合从概念过渡到实践。
- **阅读入口**：[出版社 O'Reilly](https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/)、[配套代码与笔记](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models)
- **建议配合**：[[生成式AI与大模型]]、[[大模型与RAG实战手册]]

### 3. Designing Machine Learning Systems

- **作者**：Chip Huyen
- **主题**：数据工程、训练数据、部署、监控、模型迭代
- **推荐理由**：从系统视角解释机器学习项目如何从实验走向生产，重点关注数据分布、可靠性和持续维护。
- **阅读入口**：[出版社 O'Reilly](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)、[作者网站](https://huyenchip.com/)
- **建议配合**：[[AI工程与部署]]、[[机器学习]]

### 4. Natural Language Processing with Transformers

- **作者**：Lewis Tunstall、Leandro von Werra、Thomas Wolf
- **主题**：Transformer、预训练模型、Hugging Face、NLP 应用
- **推荐理由**：以 Hugging Face 生态为主线，实践文本分类、问答、摘要等任务，理解 Transformer 模型的使用与微调。
- **阅读入口**：[出版社 O'Reilly](https://www.oreilly.com/library/view/natural-language-processing/9781098103231/)、[配套代码仓库](https://github.com/nlp-with-transformers/notebooks)
- **建议配合**：[[深度学习]]、[[生成式AI与大模型]]

### 5. Knowledge Graphs and LLMs in Action

- **作者**：Alessandro Negro
- **主题**：知识图谱、图数据、LLM、GraphRAG
- **推荐理由**：帮助理解结构化知识与大语言模型如何互补，适合探索知识检索、实体关系和知识增强问答。
- **阅读入口**：[Manning 官方图书页](https://www.manning.com/books/knowledge-graphs-and-llms-in-action)、[Manning 在线试读入口](https://livebook.manning.com/)
- **建议配合**：[[生成式AI与大模型]]、[[大模型与RAG实战手册]]、知识管理专题

### 6. Generative Deep Learning

- **作者**：David Foster
- **主题**：VAE、GAN、Transformer、扩散模型与生成式学习
- **推荐理由**：系统了解生成模型的主要思想与实现路径，适合希望理解图像、文本等内容生成机制的读者。
- **阅读入口**：[出版社 O'Reilly](https://www.oreilly.com/library/view/generative-deep-learning/9781098134174/)、[第二版配套代码](https://github.com/davidADSP/Generative_Deep_Learning_2nd_Edition)
- **建议配合**：[[深度学习]]、[[生成式AI与大模型]]

### 7. Reinforcement Learning: An Introduction

- **作者**：Richard S. Sutton、Andrew G. Barto
- **主题**：马尔可夫决策过程、动态规划、Monte Carlo、时序差分、策略梯度
- **推荐理由**：强化学习领域的经典教材，适合研究智能体如何通过环境反馈学习策略。
- **阅读入口**：[作者提供的第二版官方页面与 PDF](http://incompleteideas.net/book/the-book-2nd.html)（作者公开版本）、[MIT Press 图书页](https://mitpress.mit.edu/9780262039246/reinforcement-learning/)
- **建议配合**：[[强化学习实战路线]]、[[机器人与具身智能实战路线]]

### 8. AI Snake Oil

- **作者**：Arvind Narayanan、Sayash Kapoor
- **主题**：AI 能力评估、预测系统局限、技术宣传辨别
- **推荐理由**：帮助读者区分真正有效的 AI 技术与被夸大的产品承诺，建立批判性判断能力。
- **阅读入口**：[作者维护的官方网站](https://www.aisnakeoil.com/)、[出版社 Princeton University Press](https://press.princeton.edu/)
- **建议配合**：[[AI工程与部署]]、AI 项目评估与风险分析

### 9. The Alignment Problem

- **作者**：Brian Christian
- **主题**：机器学习偏见、奖励函数、人类价值与 AI 对齐
- **推荐理由**：从技术案例与研究发展理解机器学习目标与人类意图之间的差距，建立 AI 安全与可信 AI 的基础认知。
- **阅读入口**：[作者官方网站](https://brianchristian.org/the-alignment-problem/)、[Google Books 检索](https://books.google.com/books?q=The+Alignment+Problem+Brian+Christian)
- **建议配合**：AI 评估、安全、可信系统设计

### 10. Practical Deep Learning for Cloud, Mobile, and Edge

- **作者**：Anirudh Koul、Siddha Ganju、Meher Kasam
- **主题**：计算机视觉、深度学习部署、云端、移动端、边缘推理
- **推荐理由**：把深度学习模型与真实设备和应用场景连接起来，适合关注嵌入式 AI、边缘计算和端侧部署的工程师。
- **阅读入口**：[出版社 O'Reilly](https://www.oreilly.com/library/view/practical-deep-learning/9781492034858/)、[配套代码检索](https://github.com/search?q=Practical+Deep+Learning+for+Cloud+Mobile+and+Edge&type=repositories)
- **建议配合**：[[AI工程与部署]]、[[机器人与具身智能实战路线]]、嵌入式与汽车电子专题

## 二、按专题归档的扩展书单

### 入门与人工智能全景

| 书籍 | 作者 | 适合用途 | 资源 |
|---|---|---|---|
| Artificial Intelligence: A Modern Approach | Stuart Russell / Peter Norvig | AI 全景、搜索、逻辑、规划与概率推理 | [官方书籍页](https://aima.cs.berkeley.edu/) |
| Artificial Intelligence: Foundations of Computational Agents | David Poole / Alan Mackworth | 计算智能与智能体基础 | [作者公开在线教材](https://artint.info/) |
| The Hundred-Page Machine Learning Book | Andriy Burkov | 快速建立机器学习知识地图 | [作者网站](https://themlbook.com/) |

### 机器学习与数据科学

| 书籍 | 作者 | 价值 | 资源 |
|---|---|---|---|
| Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow | Aurélien Géron | 从数据处理到模型训练的实战教材 | [配套代码](https://github.com/ageron/handson-ml3) |
| Pattern Recognition and Machine Learning | Christopher Bishop | 概率机器学习理论 | [出版社页面](https://link.springer.com/book/9780387310732) |
| The Elements of Statistical Learning | Hastie / Tibshirani / Friedman | 统计学习理论与方法 | [作者公开教材](https://hastie.su.domains/ElemStatLearn/) |
| Python for Data Analysis | Wes McKinney | Pandas 与数据处理 | [作者配套仓库](https://github.com/wesm/pydata-book) |

### 深度学习

| 书籍 | 作者 | 价值 | 资源 |
|---|---|---|---|
| Deep Learning | Ian Goodfellow / Yoshua Bengio / Aaron Courville | 深度学习理论基础 | [作者公开在线版](https://www.deeplearningbook.org/) |
| Dive into Deep Learning | Aston Zhang 等 | 公式、代码、练习结合 | [中文在线版](https://zh.d2l.ai/) |
| Deep Learning with Python | François Chollet | Keras 深度学习实践 | [出版社页面](https://www.manning.com/books/deep-learning-with-python) |
| Understanding Deep Learning | Simon J. D. Prince | 现代深度学习数学直觉 | [作者公开在线版](https://udlbook.github.io/udlbook/) |

### 大模型与 AI 工程

| 书籍 | 作者 | 价值 | 资源 |
|---|---|---|---|
| Build a Large Language Model (From Scratch) | Sebastian Raschka | 从零实现 GPT 类语言模型 | [配套代码](https://github.com/rasbt/LLMs-from-scratch) |
| AI Engineering | Chip Huyen | 基础模型应用、评估、RAG、Agent 与生产工程 | [配套资源](https://github.com/chiphuyen/aie-book) |
| Full Stack Deep Learning | 课程团队 | 从模型到完整 AI 产品的工程实践 | [课程与资料](https://fullstackdeeplearning.com/) |

## 三、中文优质教材与课程

- [《神经网络与深度学习》邱锡鹏](https://nndl.github.io/)：中文理论教材与配套资料。
- [《动手学深度学习》中文版](https://zh.d2l.ai/)：中文系统教材，适合边学边练。
- [李沐：动手学深度学习课程](https://space.bilibili.com/1567748478)：配合教材学习。
- [Datawhale 开源学习社区](https://github.com/datawhalechina)：中文开源课程与实践项目。
- [InternLM 教程](https://github.com/InternLM/Tutorial)：大模型相关教程与实践入口。
- [面向开发者的 LLM 入门课程](https://github.com/mlabonne/llm-course)：从基础到进阶的开源学习材料。

## 四、大学公开课程

| 课程 | 重点 | 链接 |
|---|---|---|
| Stanford CS229 | 机器学习 | [课程主页](https://cs229.stanford.edu/) |
| Stanford CS231n | 计算机视觉与 CNN | [课程主页](https://cs231n.stanford.edu/) |
| Stanford CS224n | NLP 与深度学习 | [课程主页](https://web.stanford.edu/class/cs224n/) |
| Stanford CS336 | 从零构建语言模型 | [课程主页](https://stanford-cs336.github.io/spring2025/) |
| MIT 6.S191 | 深度学习导论 | [课程主页](https://introtodeeplearning.com/) |
| Berkeley CS188 | 人工智能导论 | [课程主页](https://inst.eecs.berkeley.edu/~cs188/) |
| Google ML Crash Course | 机器学习基础 | [课程主页](https://developers.google.com/machine-learning/crash-course) |

## 五、建议阅读路径

1. **建立基础**：选择《Artificial Intelligence: A Modern Approach》或《The Hundred-Page Machine Learning Book》建立全景认识。
2. **掌握机器学习**：使用《Hands-On Machine Learning》完成数据处理、训练、验证和误差分析。
3. **理解深度学习**：结合《Dive into Deep Learning》与《Deep Learning》学习网络结构和优化原理。
4. **进入大模型**：阅读《Hands-On Large Language Models》和《Natural Language Processing with Transformers》，再用《Build a Large Language Model (From Scratch)》验证理解。
5. **工程落地**：阅读《Designing Machine Learning Systems》和《AI Engineering》，学习评估、部署、监控和成本控制。
6. **形成特色方向**：知识工程读《Knowledge Graphs and LLMs in Action》；机器人方向读《Reinforcement Learning》；端侧部署读《Practical Deep Learning for Cloud, Mobile, and Edge》。
7. **建立技术判断**：结合《AI Snake Oil》和《The Alignment Problem》关注能力边界、安全与社会影响。

## 六、大学公开课程与书籍的搭配

| 学习主题 | 推荐教材 | 配套课程 |
|---|---|---|
| 机器学习 | Hands-On Machine Learning | [Stanford CS229](https://cs229.stanford.edu/) |
| 计算机视觉 | Deep Learning / Dive into Deep Learning | [Stanford CS231n](https://cs231n.stanford.edu/) |
| NLP | Natural Language Processing with Transformers | [Stanford CS224n](https://web.stanford.edu/class/cs224n/) |
| 大语言模型 | Hands-On Large Language Models | [Stanford CS336](https://stanford-cs336.github.io/spring2025/) |
| 强化学习 | Reinforcement Learning: An Introduction | [OpenAI Spinning Up](https://spinningup.openai.com/) |
| AI 产品工程 | Designing Machine Learning Systems | [Full Stack Deep Learning](https://fullstackdeeplearning.com/) |

## 七、阅读与笔记模板

每读一本书，建议在对应专题下沉淀一份永久笔记：

- **核心问题**：本书试图解决什么问题？
- **知识地图**：主要章节、概念及其依赖关系。
- **关键原理**：用自己的话解释重要算法、公式和架构。
- **代码实验**：记录运行环境、代码、输入、输出和复现步骤。
- **实践案例**：它能解决什么真实问题？
- **局限与争议**：作者假设、适用边界和未解决问题。
- **关联主题**：链接到机器学习、深度学习、大模型、Agent、知识管理或嵌入式 AI。
- **阅读状态**：待读 / 阅读中 / 已读 / 已整理。

## 相关专题

- [[人工智能]]
- [[数学与Python基础]]
- [[机器学习]]
- [[深度学习]]
- [[生成式AI与大模型]]
- [[大模型与RAG实战手册]]
- [[AI工程与部署]]
- [[AI论文与数据集]]
- [[智能体]]
