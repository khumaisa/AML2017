# -*- coding: utf-8 -*-
"""
Created on Tue May 09 16:48:37 2017

@author: Aini
"""
import os
from pydub import AudioSegment


def converterMp3toWav (input_path, output_path):
    AudioSegment.converter = "C:/FFMPEG/bin/ffmpeg.exe"
    sound_mp3 = AudioSegment.from_mp3(input_path)
    sound_mp3.export(output_path, format="wav")
    

def audioSegmenting (input_dir, output_dir, lenght=30):
    half_lenght = lenght/2
    trim_lenght = half_lenght * 1000
    for root, dirname, filenames in os.walk(input_dir):
        for filename in filenames:
            audio = AudioSegment.from_wav(root+filename)
            half = len(audio)/2
            new_audio = audio[half-trim_lenght:half+trim_lenght]
            with open(output_dir+filename, 'wb') as f:
                new_audio.export(f, format='wav')
            
                
def minMaxScaler(data, min_value, max_value, range_scaler=(-1,1)):
    data = range_scaler[0]+((data-min_value)*(range_scaler[1]-range_scaler[0]))/(max_value-min_value)
    return data
    