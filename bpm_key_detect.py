# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 01:08:10 2025

@author: Administrator
"""

import librosa
import numpy as np

# 加载音频文件
file_path = r'C:\Users\Administrator\Desktop\ai audio\Midnight Glass.mp3'  # 替换为你的音频文件路径
y, sr = librosa.load(file_path)

# 识别 BPM（节拍速度）
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
print(f"BPM（节奏速度）: {tempo}")

# 识别调式
chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
key = np.argmax(np.mean(chroma, axis=1))
print(key)
keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
print(f"调式: {keys[key]}")