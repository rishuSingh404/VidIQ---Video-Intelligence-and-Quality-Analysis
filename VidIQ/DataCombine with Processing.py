# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:06:05 2020

@author: user
"""

"""
References:
    https://machinelearningmastery.com/rescaling-data-for-machine-learning-in-python-with-scikit-learn/
    https://scikit-learn.org/stable/modules/preprocessing.html
    https://towardsdatascience.com/scale-standardize-or-normalize-with-scikit-learn-6ccc7d176a02
"""

import numpy as np
import pandas as pd
from sklearn import preprocessing

TrainName = ['BigBuckBunny_H264_1', 'BigBuckBunny_H264_2', 'BigBuckBunny_H264_3', 'BigBuckBunny_SDH264HD_1', 'BigBuckBunny_SDH264HD_2', 'BigBuckBunny_SDH264HD_3',
             'BirdsInCage_H264_1', 'BirdsInCage_H264_4', 'BirdsInCage_SDH264HD_1', 'BirdsInCage_SDH264HD_2', 'BirdsInCage_SDH264HD_3', 'BirdsInCage_SDH264HD_4',
             'BQTerrace_H264_3', 'BQTerrace_H264_4', 'BQTerrace_SDH264HD_1', 'BQTerrace_SDH264HD_2', 'BQTerrace_SDH264HD_3', 'BQTerrace_SDH264HD_4',
             'CrowdRun_H264_2', 'CrowdRun_H264_3', 'CrowdRun_H264_4', 'CrowdRun_SDH264HD_1', 'CrowdRun_SDH264HD_2', 'CrowdRun_SDH264HD_3', 'CrowdRun_SDH264HD_4',
             'DanceKiss_H264_1', 'DanceKiss_H264_2', 'DanceKiss_H264_3', 'DanceKiss_H264_4', 'DanceKiss_SDH264HD_1', 'DanceKiss_SDH264HD_2', 'DanceKiss_SDH264HD_3',
             'ElFuente1_H264_1', 'ElFuente1_H264_2', 'ElFuente1_H264_3', 'ElFuente1_SDH264HD_1', 'ElFuente1_SDH264HD_3', 'ElFuente1_SDH264HD_4',
             'ElFuente2_H264_1', 'ElFuente2_H264_3', 'ElFuente2_H264_4', 'ElFuente2_SDH264HD_2', 'ElFuente2_SDH264HD_3', 'ElFuente2_SDH264HD_4',
             'FoxBird_H264_2', 'FoxBird_H264_4', 'FoxBird_SDH264HD_1', 'FoxBird_SDH264HD_2', 'FoxBird_SDH264HD_3', 'FoxBird_SDH264HD_4',
             'Kimono1_H264_1', 'Kimono1_H264_2', 'Kimono1_H264_3', 'Kimono1_H264_4', 'Kimono1_SDH264HD_1', 'Kimono1_SDH264HD_3',
             'OldTownCross_H264_1', 'OldTownCross_H264_2', 'OldTownCross_H264_4', 'OldTownCross_SDH264HD_1', 'OldTownCross_SDH264HD_2', 'OldTownCross_SDH264HD_3', 'OldTownCross_SDH264HD_4',
             'Seeking_H264_1', 'Seeking_H264_2', 'Seeking_H264_3', 'Seeking_H264_4', 'Seeking_SDH264HD_2', 'Seeking_SDH264HD_4',
             'Tennis_H264_1', 'Tennis_H264_2', 'Tennis_H264_3', 'Tennis_H264_4', 'Tennis_SDH264HD_2', 'Tennis_SDH264HD_3', 'Tennis_SDH264HD_4']

TestName = ['BigBuckBunny_H264_4', 'BigBuckBunny_SDH264HD_4', 'BirdsInCage_H264_2', 'BirdsInCage_H264_3',
             'BQTerrace_H264_1', 'BQTerrace_H264_2', 'CrowdRun_H264_1', 'DanceKiss_SDH264HD_4',
             'ElFuente1_H264_4', 'ElFuente1_SDH264HD_2', 'ElFuente2_H264_2', 'ElFuente2_SDH264HD_1',
             'FoxBird_H264_1', 'FoxBird_H264_3', 'Kimono1_SDH264HD_2', 'Kimono1_SDH264HD_4',
             'OldTownCross_H264_3', 'Seeking_SDH264HD_1', 'Seeking_SDH264HD_3', 'Tennis_SDH264HD_1']

artifactName = ['G-Noise', 'Blurry', 'Sharperness', 'Blocky', 'Freeze-100%',
                'Freeze-90%', 'Freeze-85%', 'Freeze-80%', 'Freeze-75%', 'Freeze-Percent',
                'Jerkiness', 'Flickering', 'MosquitoNoise']

# Training Inputs
x_train = pd.read_excel('TrainingData.xlsx')
x_train = x_train.reset_index().values
trainName = x_train[:, 1]
trainfreeze = np.delete(x_train, [0, 1, 2, 3, 4, 5, 12, 13, 14], 1)
x_train = np.delete(x_train, [0, 1, 6, 7, 8, 9, 10, 11], 1)

# Testing Inputs
x_test = pd.read_excel('TestingData.xlsx')
x_test = x_test.reset_index().values
testName = x_test[:, 1]
testfreeze = np.delete(x_test, [0, 1, 2, 3, 4, 5, 12, 13, 14], 1)
x_test = np.delete(x_test, [0, 1, 6, 7, 8, 9, 10, 11], 1)

allData = np.concatenate((x_train, x_test), axis=0)
allFreeze = np.concatenate((trainfreeze, testfreeze), axis=0)

scaler = preprocessing.StandardScaler()
standardised_all = scaler.fit_transform(allData)

mscaler = preprocessing.MinMaxScaler()
scaled_all = mscaler.fit_transform(standardised_all)

# destination array, position to insert, array to be inserted, axis (0 for horizontal, 1 for vertical)
scaled_all = np.insert(scaled_all, [4], allFreeze, axis = 1)
trainData = scaled_all[0:13680, :]
testData = scaled_all[13680:, :]

# scaler = preprocessing.StandardScaler()
# standardised_train = scaler.fit_transform(x_train)
# standardised_test = scaler.transform(x_test)

# mscaler = preprocessing.MinMaxScaler()
# scaled_train = mscaler.fit_transform(standardised_train)
# scaled_test = mscaler.transform(standardised_test)

# scaled_train = np.insert(scaled_train, [4], trainfreeze, axis = 1)
# scaled_test = np.insert(scaled_test, [4], testfreeze, axis = 1)

df = pd.DataFrame(data=trainData, index=trainName, columns=artifactName)
df.to_excel('StanNormTrainingData.xlsx', engine='xlsxwriter')  
df = pd.DataFrame(data=testData, index=testName, columns=artifactName)
df.to_excel('StanNormTestingData.xlsx', engine='xlsxwriter')  

