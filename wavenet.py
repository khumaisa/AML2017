#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 22:49:59 2017

@author: aini
"""

import os
import numpy as np
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen

def encodingWaveNet(data_directory, model_directory, sampling_rate):
	s = sampling_rate*30
    path = data_directory
    saved_path = data_directory+'/wavenet/'
    for root, dirname, filenames in os.walk(path):
        for filename in filenames:
            audio = utils.load_audio(root+filename, sr=sr, sample_length=s)
            fname = filename[:-4]
            sample_length = audio.shape[0]
            encoding = fastgen.encode(audio, model_directory, sample_length)
            np.save(saved_path+'wave'+fname+'.npy', encoding)
            del encoding, audio, fname, sample_length
            print filename
    print '\n'


