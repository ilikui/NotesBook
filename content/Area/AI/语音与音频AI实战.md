---
title: 语音与音频 AI 实战
tags:
  - AI
  - 语音识别
  - 音频
---

# 语音与音频 AI 实战

语音与音频 AI 不仅是把声音转成文字，还包括语音合成、说话人识别、声音事件检测、音乐理解和实时语音交互。

## 1. 任务地图

| 任务 | 目标 | 指标 |
|---|---|---|
| ASR 自动语音识别 | 语音转文字 | WER、CER |
| TTS 语音合成 | 文本生成语音 | MOS、自然度、可懂度、延迟 |
| 说话人识别 | 判断是谁说话 | EER、minDCF |
| 说话人分离/日志 | 区分说话人及时间段 | DER |
| 声音事件检测 | 识别警报、机器声、环境声 | Macro-F1、mAP |
| 音频分类 | 判断音频类别 | Accuracy、F1 |
| 语音增强 | 降噪、去混响 | SI-SDR、PESQ（结合听感） |

## 2. 信号处理基础

- 采样率：每秒采样次数；重采样需使用合适滤波，不能简单改写元数据。
- 位深：量化精度与动态范围。
- STFT：把时域信号转换为时频表示。
- Mel Spectrogram：按 Mel 频率尺度组织能量。
- MFCC：传统语音特征。
- VAD：语音活动检测。
- CTC：处理输入帧与输出 token 长度不一致的序列对齐。
- Encoder-Decoder / Transducer：现代 ASR 常见结构。

## 3. WER 与 CER

词错误率：

\[
WER=\frac{S+D+I}{N}
\]

其中 S 为替换、D 为删除、I 为插入，N 为参考文本词数。中文通常还会报告字符错误率 CER。评测前要统一文本规范化规则，例如标点、大小写、数字和空格，否则结果不可直接比较。

## 4. 开源工具

- [Whisper](https://github.com/openai/whisper)：多语言语音识别与转写。
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)：基于 CTranslate2 的 Whisper 推理实现。
- [SpeechBrain](https://github.com/speechbrain/speechbrain)：语音任务工具箱。
- [ESPnet](https://github.com/espnet/espnet)：端到端语音处理工具包。
- [FunASR](https://github.com/modelscope/FunASR)：语音识别与相关任务工具。
- [ torchaudio](https://github.com/pytorch/audio)：音频数据处理与模型组件。
- [Piper](https://github.com/rhasspy/piper)：本地 TTS 项目，检查当前维护状态和模型许可。

## 5. 数据集

- [Mozilla Common Voice](https://commonvoice.mozilla.org/)：多语言语音数据。
- [LibriSpeech](https://www.openslr.org/12/)：英语朗读语音识别。
- [AISHELL-1](https://www.openslr.org/33/)：普通话语音识别。
- [AISHELL-4](https://www.openslr.org/111/)：会议场景语音数据。
- [AudioSet](https://research.google.com/audioset/)：大规模声音事件数据集。
- [FSD50K](https://zenodo.org/records/4060432)：声音事件数据集入口。

数据集使用前必须确认版本、许可、录音授权、说话人隐私和数据用途限制。

## 6. 项目阶梯

1. 对一段 WAV 文件提取波形和 Mel Spectrogram，理解采样率与频谱。
2. 使用 Whisper/FunASR 做离线转写，比较噪声、口音、语速下的 WER/CER。
3. 加入 VAD 和分段，检查长音频切分对识别结果的影响。
4. 构建说话人日志，评估 DER 和说话人混淆。
5. 进行实时流式转写，测量首字延迟、实时因子和资源占用。

## 7. 论文阅读

- [Deep Speech 2](https://arxiv.org/abs/1512.02595)：端到端语音识别。
- [Listen, Attend and Spell](https://arxiv.org/abs/1508.01211)：注意力式语音识别。
- [wav2vec 2.0](https://arxiv.org/abs/2006.11477)：自监督语音表示学习。
- [Whisper](https://arxiv.org/abs/2212.04356)：大规模弱监督多任务语音识别。

## 相关

- [[AI专业方向]]
- [[深度学习]]
- [[AI论文与数据集]]
- [[AI项目实战路线]]
