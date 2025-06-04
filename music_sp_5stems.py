# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 16:44:17 2025

@author: Administrator
"""

import numpy as np
from spleeter.separator import Separator
import librosa
import soundfile as sf
import os

class MultiStemSeparator:
    def __init__(self, model_type='spleeter:5stems'):
        """
        初始化分离器
        model_type 可选值：
        - '2stems' (vocals + accompaniment)
        - '4stems' (vocals + drums + bass + other)
        - '5stems' (vocals + drums + bass + piano + other)
        """
        self.separator = Separator(model_type)
        self.model_type = model_type
    
    def separate_track(self, input_file, output_dir):
        """
        分离音轨并保存到指定目录
        
        参数:
        input_file (str): 输入音频文件路径
        output_dir (str): 输出目录路径
        """
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 执行分离
        self.separator.separate_to_file(
            input_file,
            output_dir,
            filename_format='{instrument}.wav'
        )
        
        return self._process_stems(output_dir)
    
    def _process_stems(self, output_dir):
        """
        对分离后的音轨进行后处理
        """
        stems = {}
        for stem in os.listdir(output_dir):
            if stem.endswith('.wav'):
                stem_path = os.path.join(output_dir, stem)
                audio, sr = librosa.load(stem_path, sr=None)
                stems[stem.replace('.wav', '')] = (audio, sr)
        return stems
    
    def apply_effects(self, audio, sr, effect_type='compress'):
        """
        为不同乐器轨道添加适当的音效
        """
        if effect_type == 'compress':
            # 简单的动态压缩
            threshold = 0.1
            ratio = 4.0
            audio_compressed = np.where(
                np.abs(audio) > threshold,
                threshold + (np.abs(audio) - threshold) / ratio * np.sign(audio),
                audio
            )
            return audio_compressed
        return audio
    
    def mix_stems(self, stems, output_file, volumes=None):
        """
        混音各个轨道
        
        参数:
        stems (dict): 包含各个轨道的字典
        output_file (str): 输出文件路径
        volumes (dict): 各轨道的音量设置，例如 {'vocals': 1.0, 'drums': 0.8}
        """
        if volumes is None:
            volumes = {stem: 1.0 for stem in stems}
        
        # 获取第一个音轨的采样率
        reference_sr = stems[list(stems.keys())[0]][1]
        
        # 混音
        mixed = np.zeros(len(stems[list(stems.keys())[0]][0]))
        for stem_name, (audio, sr) in stems.items():
            volume = volumes.get(stem_name, 1.0)
            mixed += audio * volume
        
        # 归一化
        mixed = mixed / np.max(np.abs(mixed))
        
        # 保存混音结果
        sf.write(output_file, mixed, reference_sr)

def main():
    """
    使用示例
    """
    # 初始化分离器
    separator = MultiStemSeparator('spleeter:5stems')
    
    # 设置输入输出路径
    input_file = r'C:\Users\Administrator\Desktop\YKIK.mp3'
    output_dir = r'C:\Users\Administrator\Desktop'
    
    print("step1")
    # 分离音轨
    #separator.separate_track(input_file, output_dir)
    stems = separator.separate_track(input_file, output_dir)
    print("step2")
    # 对各个轨道应用效果
    
    processed_stems = {}
    for stem_name, (audio, sr) in stems.items():
        processed_audio = separator.apply_effects(audio, sr, 'compress')
        processed_stems[stem_name] = (processed_audio, sr)
        sf.write(f'{stem_name}_vocals.wav', processed_audio, sr)
    print("step3")
    print(processed_stems)
    #设置各轨道音量
    volumes = {
        'vocals': 1.0,
        'drums': 0.8,
        'bass': 0.9,
        'piano': 0.85,
        'other': 0.7
    }
    
    #混音并保存
    separator.mix_stems(processed_stems, 'final_mix.wav', volumes)

if __name__ == '__main__':
    main()