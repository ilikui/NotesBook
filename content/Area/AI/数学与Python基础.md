---
title: 数学与 Python 基础
tags:
  - AI
  - 数学
  - Python
---

# 数学与 Python 基础

数学不是开始 AI 学习前必须一次学完的门槛。建议围绕正在实现的算法补齐数学知识：先理解几何/概率直觉，再学习公式，最后用代码验证。

## 数学路线

| 模块 | 核心内容 | AI 中的用途 | 推荐资源 |
|---|---|---|---|
| 线性代数 | 向量、矩阵、点积、特征值、SVD | Embedding、线性层、PCA | [3Blue1Brown 线性代数](https://www.3blue1brown.com/topics/linear-algebra) |
| 微积分 | 导数、偏导、链式法则、梯度 | 反向传播与优化 | [3Blue1Brown 微积分](https://www.3blue1brown.com/topics/calculus) |
| 概率统计 | 分布、条件概率、贝叶斯、期望方差 | 分类、不确定性、生成模型 | [StatQuest](https://statquest.org/) |
| 优化 | SGD、Momentum、Adam、正则化 | 模型训练 | [Dive into Deep Learning](https://d2l.ai/) |
| 信息论 | 熵、交叉熵、KL 散度 | 分类损失、语言模型训练 | [Information Theory, Inference, and Learning Algorithms](https://www.inference.org.uk/itprnn/book.html) |

## Python 科学计算栈

- [Python 官方教程](https://docs.python.org/3/tutorial/)
- [NumPy 文档](https://numpy.org/doc/stable/user/quickstart.html)
- [Pandas 入门](https://pandas.pydata.org/docs/getting_started/index.html)
- [Matplotlib 教程](https://matplotlib.org/stable/tutorials/index.html)
- [SciPy 文档](https://docs.scipy.org/doc/scipy/)
- [Jupyter 文档](https://docs.jupyter.org/)
- [Python Data Science Handbook（在线版）](https://jakevdp.github.io/PythonDataScienceHandbook/)

## PyTorch 基础

学习顺序：Tensor → 自动微分 autograd → Dataset/DataLoader → nn.Module → loss → optimizer → training loop → checkpoint → inference。

- [PyTorch 官方 60 分钟入门](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [PyTorch 文档](https://pytorch.org/docs/stable/index.html)

## 动手练习

1. 用 NumPy 实现向量点积、矩阵乘法和标准化。
2. 从零实现线性回归和梯度下降，绘制损失曲线。
3. 用 Pandas 清洗一个 CSV 数据集，并说明缺失值处理策略。
4. 用 PyTorch 实现一个两层 MLP，比较不同学习率。
5. 固定随机种子，记录训练/验证损失与实验配置。

## 自测标准

- 能解释矩阵乘法、梯度、损失函数和概率分布的直觉。
- 能用 NumPy 写出简单的数值计算。
- 能读懂 PyTorch 的训练循环并定位维度错误。
- 能区分训练、验证、测试数据的用途。

## 相关

- [[人工智能]]
- [[机器学习]]
- [[深度学习]]
- [[数学]]
