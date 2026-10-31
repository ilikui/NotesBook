---
title: MATLAB10000问：面向对象、GPU、图像、深度学习与测试
tags:
  - MATLAB
  - Simulink
  - 10000问
---

# MATLAB10000问：面向对象、GPU、图像、深度学习与测试

本篇迁移 MATLAB/Simulink 10000 问第五批 15 道题，覆盖 MATLAB OOP、App Designer、并行计算、GPU、图像处理、深度学习、参数估计、系统辨识、单元测试和变体系统。

## 57. MATLAB classdef 和 C++ class 有什么不同？

**答案：** MATLAB classdef 定义类的属性、方法、事件和继承关系；C++ class 还涉及更广泛的编译期类型系统、模板、析构/RAII、运算符重载、指针与引用语义等。两者都支持封装和继承，但对象生命周期、值语义、句柄语义和内存管理方式不同。

MATLAB 类更适合在 MATLAB 工作流中组织数据和算法；若要生成嵌入式 C 代码，需确认 MATLAB Coder 对所用类特性的支持范围，不能认为所有 classdef 代码都能直接生成 C。

## 58. MATLAB 的 value class 和 handle class 有什么区别？

**答案：** value class 按值语义工作，赋值通常得到逻辑上独立的值；handle class 按引用语义工作，多个变量可以引用同一个对象，修改对象属性会反映到所有引用该对象的变量上。

- value class：适合不可变数据对象或希望赋值后隔离修改的场景。
- handle class：适合需要共享状态、图形对象、设备连接和大型对象引用的场景。

选择时要考虑副作用、复制成本和对象生命周期。

## 59. property listener 如何在属性变化时自动执行函数？

**答案：** 对可观察属性（SetObservable），可用 addlistener 注册 PostSet 等事件监听器。属性变化时，监听器回调被触发。需要保存 listener 句柄，并在不再需要时删除；否则监听器生命周期和对象生命周期可能不符合预期。

监听器适合 UI 状态同步、模型参数变化通知和对象间事件响应，但应避免回调互相修改属性形成递归或难以调试的副作用。

## 60. App Designer 与 GUIDE 最大的架构差异是什么？

**答案：** GUIDE 是较早的 GUI 开发工具，通常围绕 figure、控件句柄和回调函数组织；App Designer 以 app 类为核心，界面组件成为 app 对象属性，回调方法属于类的方法，数据和状态可通过 properties 管理。

App Designer 更适合封装、复用、版本管理和面向对象开发。GUIDE 已属于旧工作流，维护旧项目时可继续理解其句柄和回调机制，但新项目应优先评估 App Designer。

## 61. App Designer 的回调函数如何共享状态？为什么不建议滥用全局变量？

**答案：** 推荐把应用状态放在 app 的 properties 中，回调通过 app 对象读写这些属性。全局变量会扩大共享状态范围，造成命名冲突、隐藏依赖和测试困难；在 callback 内临时定义的局部变量则不会自动跨回调保存。

例如按钮回调更新 app.Counter，另一个回调读取 app.Counter。复杂状态可封装为独立对象或数据模型。

## 62. parfor 和 for 什么时候可以互换？

**答案：** parfor 的每次迭代必须能被并行执行，循环变量需要符合 MATLAB 的分类规则（sliced、broadcast、reduction 等）。若第 n 次迭代依赖第 n−1 次迭代的结果，就不能简单改成 parfor。

并行化还要考虑任务粒度、数据传输和 worker 启动开销；循环很短或数据量很小时，并行反而可能更慢。

## 63. GPU 计算是否一定比 CPU 快？

**答案：** 不一定。GPU 适合大量并行、规则、计算密集的工作负载；小矩阵或低并行度任务可能被数据传输和 kernel 启动开销抵消。应先把数据放入 gpuArray，尽量减少 CPU/GPU 来回传输，再用 tic/toc 和 gputimeit 等适当方式测量。

是否加速取决于矩阵规模、算子支持、显存带宽、GPU 型号、数据精度和并发负载。

## 64. imread 读取彩色图片返回什么数据结构？

**答案：** 常见 RGB 图像返回 m×n×3 数组，第三维分别表示 R、G、B 通道；灰度图通常返回 m×n 数组；索引图像可能返回索引矩阵和 colormap。数据类型可能是 uint8、uint16、logical 或其他格式，不能默认所有图像都是 double。

读取后应检查 size、class 和颜色映射，再决定归一化、颜色空间转换和通道处理方式。

## 65. imfilter 和 conv2 有什么区别？高斯核大小怎样影响去噪？

**答案：** imfilter 面向图像滤波，支持多维数组、边界处理选项和相关/卷积模式；conv2 是二维卷积运算，默认边界处理通常相当于零填充。imfilter 默认执行相关运算，可通过参数指定卷积。

高斯核越大，平滑范围越广，噪声抑制可能增强，但细节和边缘也更容易模糊；核大小和标准差 σ 应一起考虑。滤波器设计要在去噪和细节保留之间权衡。

## 66. 一个最基础的 CNN 图像分类网络由哪些层组成？

**答案：** 常见教学结构为：

1. imageInputLayer：输入图像。
2. convolution2dLayer：提取局部特征。
3. reluLayer：引入非线性。
4. maxPooling2dLayer：降低空间尺寸。
5. fullyConnectedLayer：映射到类别得分。
6. softmaxLayer：把得分转成概率分布。
7. classificationLayer 或当前版本推荐的分类输出接口。

具体 API 随 MATLAB 版本和训练工作流变化；网络层数应由任务、数据量和部署约束决定，不存在适合所有问题的“最少固定层数”。

~~~~mermaid
flowchart LR
  A[Image Input] --> B[Convolution]
  B --> C[ReLU]
  C --> D[Pooling]
  D --> E[Fully Connected]
  E --> F[Softmax / Class Output]
~~~~

## 67. MiniBatchSize、MaxEpochs、InitialLearnRate 如何影响训练？

**答案：**

- MiniBatchSize：每次参数更新使用的样本数；大 batch 可能提高吞吐但增加显存需求，梯度噪声也会变化。
- MaxEpochs：训练集完整遍历次数；过少可能欠拟合，过多可能过拟合。
- InitialLearnRate：初始学习率；过大可能发散，过小可能收敛慢。

还要结合验证集、学习率调度、正则化、数据增强、早停和随机种子进行实验。不要只凭一次训练曲线选择参数。

## 68. Simulink Design Optimization 怎样从实测曲线反推电机参数？

**答案：** 先建立可仿真的电机模型，再定义待估参数（电阻、电感、惯量、摩擦等）、实测数据、输入激励和代价函数。优化器调整参数，使仿真输出与测量曲线差异最小。

代价函数不应只盲目采用未加权的平方误差：电流、转速的量纲和尺度不同，可使用归一化或加权误差；若有时间延迟或初始条件偏差，应先识别/估计这些因素，否则优化器可能用错误参数补偿时延。

## 69. System Identification 为什么强调 Persistently Exciting 输入？

**答案：** 输入信号必须包含足够丰富的频率成分和变化，才能让模型参数在数据中可辨识。若输入几乎恒定或只激励很窄的频段，某些参数可能无法从输出中区分。

常见激励包括阶跃、PRBS、多正弦和扫频，但选择要考虑系统安全、线性工作范围、采样频率和目标频带。充分激励是模型可辨识的重要条件，不代表只要输入复杂就一定得到正确模型。

## 70. matlab.unittest 的 TestMethodSetup 和 TestMethodTeardown 做什么？

**答案：** TestMethodSetup 在每个测试方法执行前运行，用于建立该测试需要的初始状态；TestMethodTeardown 在每个测试方法结束后运行，用于清理资源。TestClassSetup/Teardown 则用于整个测试类级别的一次性初始化和清理。

不要把“重置 base workspace”当成唯一做法；更好的单元测试应通过 fixture、临时目录、依赖注入和独立测试数据控制外部依赖。

## 71. TemporaryFolderFixture 和 PathFixture 解决什么问题？

**答案：** TemporaryFolderFixture 为测试创建临时目录，并在清理阶段移除；PathFixture 临时调整 MATLAB 搜索路径，测试结束后恢复。Fixtures 让测试不依赖开发者机器上的固定路径或长期残留文件，提升可重复性。

对外部函数可使用 mock/stub 或可替换依赖，避免单元测试必须连接真实硬件、数据库或网络服务。

## 72. Variant Subsystem 怎样管理高配/低配车型差异？

**答案：** Variant Subsystem 在同一模型中保留多个实现分支，通过 Variant Control 选择某个配置。控制变量可来自模型工作区、数据字典或配置对象；选择时机（例如模型更新、仿真启动或代码生成编译期）应按当前 Simulink 版本和目标工作流设置。

若车型差异在生产代码编译前确定，通常采用编译期变体，便于移除未选分支；若需要运行时切换，则必须确认目标支持、内存预算和安全策略，不能把编译期 Variant 当作运行时热切换机制。

~~~~mermaid
flowchart TD
  A[Variant Control：车型配置] --> B{选择变体}
  B -->|高配| C[CAN FD 实现]
  B -->|低配| D[传统 CAN 实现]
  C --> E[统一接口]
  D --> E
  E --> F[仿真 / 代码生成 / 集成]
~~~~

## Flomo 原始来源

- MATLAB/Simulink 10000 问总表：https://v.flomoapp.com/mine/?memo_id=MjQ2Mzc1Mzg4
