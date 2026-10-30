---
title: GitHub 开源 AI 学习项目
tags:
  - AI
  - GitHub
  - 开源项目
---

# GitHub 开源 AI 学习项目

本页按学习阶段整理可运行、可阅读的开源项目。项目活跃度、依赖和 API 会变化，开始学习前先查看仓库 README、License、Release 和最近提交；不要只按 Star 数选择。

## 1. 零基础与综合课程

| 项目 | 适合阶段 | 内容 |
|---|---|---|
| [Microsoft AI-For-Beginners](https://github.com/microsoft/AI-For-Beginners) | 入门 | 12 周、24 课，覆盖 AI 基础、练习和实验 |
| [Berkeley AI Textbook](https://github.com/BerkeleyAI/textbook) | 入门 | AI 搜索、推理、决策与学习的课程教材 |
| [Datawhale](https://github.com/datawhalechina) | 入门到进阶 | 中文开源课程与实践项目集合 |
| [AI Learning Roadmap](https://github.com/bishwaghimire/ai-learning-roadmaps) | 入门 | AI/ML/DL 学习路线和资源索引 |

## 2. Python、数据科学与机器学习

- [scikit-learn](https://github.com/scikit-learn/scikit-learn)：经典机器学习算法与 Pipeline。
- [scikit-learn examples](https://scikit-learn.org/stable/auto_examples/index.html)：可运行的官方案例。
- [Hands-On ML](https://github.com/ageron/handson-ml3)：机器学习与深度学习实践代码。
- [XGBoost](https://github.com/dmlc/xgboost)：梯度提升树。
- [LightGBM](https://github.com/microsoft/LightGBM)：高效梯度提升框架。
- [CatBoost](https://github.com/catboost/catboost)：类别特征友好的梯度提升框架。

## 3. 深度学习与 PyTorch

- [PyTorch](https://github.com/pytorch/pytorch)：深度学习框架。
- [PyTorch Tutorials](https://github.com/pytorch/tutorials)：官方入门和进阶示例。
- [Dive into Deep Learning 中文版](https://github.com/d2l-ai/d2l-zh)：理论、代码和练习相结合的开源教材。
- [fastbook](https://github.com/fastai/fastbook)：fast.ai 深度学习课程配套书。
- [timm](https://github.com/huggingface/pytorch-image-models)：视觉模型、预训练权重和训练工具。

## 4. 计算机视觉

- [Ultralytics](https://github.com/ultralytics/ultralytics)：YOLO 系列视觉任务工具。
- [OpenMMLab](https://github.com/open-mmlab)：目标检测、分割、姿态估计等视觉算法生态。
- [MMDetection](https://github.com/open-mmlab/mmdetection)：目标检测工具箱。
- [Detectron2](https://github.com/facebookresearch/detectron2)：检测与分割研究平台。
- [Segment Anything](https://github.com/facebookresearch/segment-anything)：通用图像分割研究项目。

## 5. NLP、Transformer 与大语言模型

- [Hugging Face Transformers](https://github.com/huggingface/transformers)：模型加载、训练和推理。
- [Hugging Face Datasets](https://github.com/huggingface/datasets)：数据集处理和加载。
- [Hugging Face PEFT](https://github.com/huggingface/peft)：LoRA 等参数高效微调。
- [TRL](https://github.com/huggingface/trl)：SFT、偏好优化等后训练工具。
- [LLMs from Scratch](https://github.com/rasbt/LLMs-from-scratch)：从零实现语言模型。
- [nanoGPT](https://github.com/karpathy/nanoGPT)：简洁 GPT 训练代码。
- [Dive into LLMs](https://github.com/InternLM/Tutorial)：中文大模型课程与实践入口。
- [LLM Course](https://github.com/mlabonne/llm-course)：LLM 学习路线与实践资源。
- [Stanford CS336](https://stanford-cs336.github.io/spring2025/)：从零构建语言模型的课程材料。

## 6. RAG、Agent 与应用开发

- [LangChain](https://github.com/langchain-ai/langchain)：LLM 应用开发框架。
- [LangGraph](https://github.com/langchain-ai/langgraph)：有状态 Agent 工作流。
- [LlamaIndex](https://github.com/run-llama/llama_index)：数据接入、索引和 RAG。
- [Haystack](https://github.com/deepset-ai/haystack)：检索与生成应用框架。
- [Microsoft AutoGen](https://github.com/microsoft/autogen)：多 Agent 应用框架。
- [CrewAI](https://github.com/crewAIInc/crewAI)：多 Agent 协作框架。
- [Model Context Protocol](https://github.com/modelcontextprotocol/specification)：模型上下文协议规范。

## 7. 推理、部署与评估

- [vLLM](https://github.com/vllm-project/vllm)：高吞吐 LLM 推理服务。
- [llama.cpp](https://github.com/ggml-org/llama.cpp)：CPU/GPU 本地模型推理。
- [Ollama](https://github.com/ollama/ollama)：本地模型运行工具。
- [OpenCompass](https://github.com/open-compass/OpenCompass)：大模型评测平台。
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)：语言模型标准化评测。
- [MLflow](https://github.com/mlflow/mlflow)：实验追踪和模型生命周期管理。
- [DVC](https://github.com/iterative/dvc)：数据与模型版本管理。

## 8. 建议的仓库学习顺序

1. Microsoft AI-For-Beginners：建立 AI 全景。
2. Hands-On ML + scikit-learn：完成经典机器学习项目。
3. Dive into Deep Learning + PyTorch Tutorials：掌握神经网络训练。
4. Hugging Face LLM Course + LLMs from Scratch：理解 Transformer 和 LLM。
5. LlamaIndex/LangChain + RAGAS：构建并评估 RAG。
6. vLLM/llama.cpp + OpenCompass：部署和评测模型。

## 项目选择与许可证

- 优先选择官方组织、作者本人或长期维护的仓库。
- 检查代码 License；模型权重、数据集、文档可能使用不同许可。
- GitHub 仓库可见不代表其中所有数据、模型权重或第三方文件都允许商用。
- 复现研究时固定 commit、依赖版本和数据版本，记录运行硬件与指标。
