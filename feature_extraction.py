# -*- coding: utf-8 -*-
"""
Created on Fri Dec 01 14:01:45 2017

@author: Aini
"""

import os
import librosa
import numpy as np
import itertools

def pathExists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        

def extractFeatures(file_dir, saved_path):
    
    features = ['rmse', 'chro', 'cens', 'ccqt','temp',
                'onst','mfcc','scon','rolf','zcrs','tonc']
    fDir = []
    for feature in features:
        fdir = saved_path+feature+'/'
        pathExists(fdir)
        fDir.append(fdir)  
    
    ydir = saved_path+'y/'
    srdir = saved_path+'sr/'
    pathExists(ydir)
    pathExists(srdir)
        
    for root, dirname, filenames in os.walk(file_dir):
        
        for filename in filenames:
            all_feat = []
            fname = filename[:-4]
            
            #load wav file 
            y, sr = librosa.load(root+filename)
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            np.save(ydir+'y_'+fname, y)
            np.save(srdir+'sr_'+fname, sr)            
            
            #extract RMSE features
            S, phase = librosa.magphase(librosa.stft(y))
            all_feat.append(librosa.feature.rmse(S=S))
            
            #extract chroma features
            all_feat.append(librosa.feature.chroma_stft(y=y, sr=sr))

            #extract chroma energy normalized feature
            all_feat.append(librosa.feature.chroma_cens(y=y, sr=sr))
     
            #extract chroma Constant-Q transform feature
            all_feat.append(librosa.feature.chroma_cqt(y=y, sr=sr))
            
            #extract tempogram feature
            all_feat.append(librosa.feature.tempogram(y=y, sr=sr, win_length=40))
            
            #extract onset strength feature
            all_feat.append(np.array([librosa.onset.onset_strength(y, sr=sr)]))
            
            #extract MFCC feature
            all_feat.append(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13))
            
            #extract spectral contrast feature
            S = np.abs(librosa.stft(y))
            all_feat.append(librosa.feature.spectral_contrast(S=S, sr=sr))
   
            #extract rolloff feature
            all_feat.append(librosa.feature.spectral_rolloff(y=y, sr=sr))
            
            #extract zero crosing rate feature
            all_feat.append(librosa.feature.zero_crossing_rate(y))
            
            #extract tonal centroid feature
            y1 = librosa.effects.harmonic(y)
            all_feat.append(librosa.feature.tonnetz(y=y1, sr=sr))
        
            for i in range(len(features)):
                np.save(fDir[i]+features[i]+'_'+fname, all_feat[i])
           
            print filename           
            

def computeMeanStd(feature_name, feature_dir, save_dir):
    Id = []
    meanstd = []
    for root, dirname, filenames in os.walk(feature_dir):
        for filename in filenames:
            feature = np.load(root+filename)
            
            try:
                index = filename.index('_') + 1
            except:
                index = 5
                feature = feature[0]
                feature = feature.T
            try:
                Id.append(int(filename[index:-4]))
            except:
                Id.append(int(filename[index+1:-4]))
            mean = (np.mean(feature, axis=1))
            std = (np.std(feature, axis=1))
            meanstd.append(np.concatenate((mean, std)))
    index_sort = np.argsort(np.array(Id))
    print np.array(filenames)[index_sort]
    meanstd = np.array(meanstd)[index_sort]
    meanstd = meanstd
    np.save(save_dir+feature_name+'_meanstd.npy', meanstd)
    return meanstd
    

def main(data_dir, save_feature_dir, saved_meanstd_dir):

    features = ['rmse', 'chro', 'cens', 'ccqt','temp',
            'onst','mfcc','scon','rolf','zcrs','tonc', 'wave']

    pathExists(save_feature_dir)
    pathExists(saved_meanstd_dir)

    extractFeatures(data_dir, save_feature_dir)

    for feat in features:
        d = p+feat+'/'
        mean_std = computeMeanStd(feat, d, saved_meanstd_dir)
        print feat
    print '\n'
        