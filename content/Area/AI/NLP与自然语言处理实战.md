---
title: NLP 与自然语言处理实战
tags:
  - AI
  - NLP
  - 自然语言处理
---

# NLP 与自然语言处理实战

自然语言处理（NLP）研究如何让机器处理文本、语言和语义。现代 NLP 的主线是从规则与统计方法，发展到神经网络、Transformer、预训练模型和大语言模型。

## 1. 任务地图

| 任务 | 目标 | 常用指标 |
|---|---|---|
| 文本分类 | 情感、主题、意图识别 | Accuracy、Macro-F1 |
| 序列标注 | 分词、词性、实体识别 | Token/Entity F1 |
| 信息抽取 | 关系、事件、结构化字段 | Precision、Recall、F1 |
| 机器翻译 | 源语言到目标语言 | BLEU、COMET（结合人工评估） |
| 摘要 | 压缩长文本 | ROUGE、事实一致性 |
| 问答 | 从材料中回答问题 | EM、F1、引用准确率 |
| 语义检索 | 找到相关文本 | Recall@K、MRR、nDCG |
| 对话与生成 | 生成连贯且符合指令的文本 | 人工评测、任务成功率、安全性 |

## 2. 从传统 NLP 到 Transformer

1. 文本规范化、分句、分词、词形还原。
2. 词袋模型、TF-IDF、N-gram。
3. Word2Vec、GloVe、FastText 等静态词向量。
4. RNN、LSTM、GRU 与序列建模。
5. Attention 与 Transformer。
6. BERT 类编码器：分类、抽取、检索表示。
7. GPT 类解码器：自回归生成与指令跟随。
8. Embedding、Reranker、RAG 与工具调用。

TF-IDF 的直觉是提高“在当前文档中重要、但在整个语料中不常见”的词的权重。它是很好的检索基线，但无法充分理解同义表达和上下文。

## 3. Transformer 核心公式

Scaled Dot-Product Attention：

\[
Attention(Q,K,V)=softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\]

多头注意力并行学习不同的关系子空间。理解时要跟踪张量形状：Batch、Sequence Length、Head、Head Dimension。

Transformer 还包括位置表示、残差连接、LayerNorm 和前馈网络。实践时应掌握 padding mask、causal mask、上下文长度与注意力复杂度。

## 4. 代码实验：TF-IDF 文本分类

```python
from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

train = fetch_20newsgroups(subset="train", remove=("headers", "footers", "quotes"))
test = fetch_20newsgroups(subset="test", remove=("headers", "footers", "quotes"))

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=100_000),
    LogisticRegression(max_iter=2000, C=4)
)
model.fit(train.data, train.target)
pred = model.predict(test.data)
print(classification_report(test.target, pred, target_names=train.target_names))
```

先建立传统方法基线，再用预训练 Transformer 比较效果、训练成本、推理延迟和模型体积。数据集仅作教学示例，正式使用应审查数据许可与类别分布。

## 5. 数据与评测资源

- [GLUE](https://gluebenchmark.com/) / [SuperGLUE](https://super.gluebenchmark.com/)：语言理解基准。
- [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/)：阅读理解。
- [CoNLL-2003](https://www.clips.uantwerpen.be/conll2003/ner/)：命名实体识别经典数据。
- [Hugging Face Datasets](https://huggingface.co/datasets)：数据集发现与加载。
- [BEIR](https://github.com/beir-cellar/beir)：信息检索基准。
- [MTEB](https://github.com/embeddings-benchmark/mteb)：Embedding 多任务评测。
- [XTREME](https://github.com/google-research/xtreme)：跨语言评测资源。

## 6. 开源工具

- [spaCy](https://github.com/explosion/spaCy)：工业 NLP 管线。
- [NLTK](https://github.com/nltk/nltk)：语言处理教学工具。
- [Transformers](https://github.com/huggingface/transformers)：预训练模型。
- [Sentence Transformers](https://github.com/UKPLab/sentence-transformers)：句向量与语义检索。
- [Tokenizers](https://github.com/huggingface/tokenizers)：高性能分词器。
- [Stanza](https://github.com/stanfordnlp/stanza)：多语言 NLP。
- [HanLP](https://github.com/hankcs/HanLP)：中文自然语言处理。

## 7. 项目阶梯

1. 用 TF-IDF + Logistic Regression 做新闻分类，建立 Macro-F1 基线。
2. 用 Transformer 做同一任务，分析错分样本和领域偏差。
3. 做命名实体识别，评估实体级 Precision/Recall/F1。
4. 建立语义搜索系统，比较 BM25、Embedding 和混合检索的 Recall@K。
5. 做一个带证据引用的问答/RAG 系统，单独评估检索和生成质量。

## 8. 论文阅读

- [Word2Vec](https://arxiv.org/abs/1301.3781)：分布式词表示。
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)：Transformer。
- [BERT](https://arxiv.org/abs/1810.04805)：双向预训练。
- [T5](https://arxiv.org/abs/1910.10683)：Text-to-Text 框架。
- [Sentence-BERT](https://arxiv.org/abs/1908.10084)：句向量语义相似度。
- [RAG](https://arxiv.org/abs/2005.11401)：检索增强生成。

## 相关

- [[AI专业方向]]
- [[生成式AI与大模型]]
- [[大模型与RAG实战手册]]
- [[AI论文与数据集]]
