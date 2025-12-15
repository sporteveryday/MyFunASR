#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""FunASR 本地测试脚本"""

import torch
import os

# 检测设备
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"使用设备: {device}")

# 添加源码路径到最前面
import sys
sys.path.insert(0, r"d:\workspace\FunASR")

print("正在导入 funasr...")

# 手动导入并注册模型
import importlib
import pkgutil

def import_submodules_debug(package_name):
    """Import all submodules with debug info"""
    package = importlib.import_module(package_name)
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            importlib.import_module(name)
        except Exception as e:
            pass  # 忽略导入错误

# 导入核心模块
import_submodules_debug("funasr.models")
import_submodules_debug("funasr.frontends")

from funasr import AutoModel

print("正在加载语音识别模型 (paraformer-zh)...")

model = AutoModel(
    model="paraformer-zh",  # 中文语音识别模型
    vad_model="fsmn-vad",   # 语音端点检测
    punc_model="ct-punc",   # 标点恢复
    device=device,
)

print("模型加载完成！")

# 使用 soundfile 加载音频文件
wav_file = r"d:\workspace\FunASR\runtime\funasr_api\asr_example.wav"

print(f"\n正在识别音频文件: {wav_file}")
print("-" * 50)

# 使用 soundfile 读取音频
import soundfile as sf
import numpy as np

audio_data, sample_rate = sf.read(wav_file)
print(f"音频信息: 采样率={sample_rate}, 长度={len(audio_data)/sample_rate:.2f}秒")

# 如果是多通道，转为单通道
if len(audio_data.shape) > 1:
    audio_data = audio_data.mean(axis=1)

# 如果采样率不是16000，重采样
if sample_rate != 16000:
    import librosa
    audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
    sample_rate = 16000

# 确保是 float32
audio_data = audio_data.astype(np.float32)

# 进行语音识别
res = model.generate(
    input=audio_data,
    batch_size_s=300,
)

print("\n识别结果:")
for item in res:
    print(f"文本: {item['text']}")
