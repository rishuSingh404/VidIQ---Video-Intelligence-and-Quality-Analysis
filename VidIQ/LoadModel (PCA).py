# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 23:20:13 2020

@author: user
"""

import glob
import warnings
warnings.filterwarnings("ignore")
# Imports
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dropout, Dense
from keras.layers import LSTM
# from keras.regularizers import l1, l2
import pandas as pd
# from keras import optimizers
from scipy.stats.stats import pearsonr
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
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

input_num = 6
pca = PCA(n_components = input_num)
mscaler = preprocessing.MinMaxScaler()

# Training Inputs
x_train = pd.read_excel('StanNormTrainingData.xlsx')
x_train = x_train.reset_index().values
x_train = np.delete(x_train, [0, 1, 3], 1)
x_train = pca.fit_transform(x_train)
x_train = mscaler.fit_transform(x_train)

# Training Outputs
y_train = pd.read_excel('TrainingScores.xlsx')
y_train = y_train.reset_index().values
y_train = np.delete(y_train, [0, 1, 3, 4], 1)
y_train = np.reshape(y_train, (1, 76)).flatten()

# Testing Inputs
x_test = pd.read_excel('StanNormTestingData.xlsx')
x_test = x_test.reset_index().values
x_test = np.delete(x_test, [0, 1, 3], 1)
x_test = pca.transform(x_test)
x_test = mscaler.transform(x_test)

# Testing Outputs
y_test = pd.read_excel('TestingScores.xlsx')
y_test = y_test.reset_index().values
y_test = np.delete(y_test, [0, 1, 3, 4], 1)
y_test = np.reshape(y_test, (1, 20)).flatten()

# Entire Dataset Inputs
x_all =  np.concatenate((x_train, x_test), axis=0)

# Entire Dataset Outputs
y_all = pd.read_excel('AllScores.xlsx')
y_all = y_all.reset_index().values
y_all = np.delete(y_all, [0, 1, 3, 4], 1)
y_all = np.reshape(y_all, (1, 96)).flatten().tolist()

x_train = np.reshape(x_train, (76, 180, input_num))
x_test = np.reshape(x_test, (20, 180, input_num))
x_all = np.reshape(x_all, (96, 180, input_num))

hidden_nodes = 20

# Train
model = Sequential()
model.add(LSTM(hidden_nodes, return_sequences=True, input_shape=(180, input_num)))
model.add(Dropout(0.2))
model.add(LSTM(hidden_nodes, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(hidden_nodes))
model.add(Dropout(0.25))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
print(model.summary())
print('\n')

i=4857      # Enter the epoch which you want to test for the testing set
# if i < 10: 
#     name = glob.glob('C:/Users/user/OneDrive - The Hong Kong Polytechnic University/EIE4433 FYP/Results/3 LSTM Layers D-2-2-25/' + str(input_num) +' inputs StanNormData Diffferent Epochs/' + str(hidden_nodes) + 'nodes/weights.0' + str(i) + '-*.hdf')
# else:
#     name = glob.glob('C:/Users/user/OneDrive - The Hong Kong Polytechnic University/EIE4433 FYP/Results/3 LSTM Layers D-2-2-25/' + str(input_num) +' inputs StanNormData Different Epochs/' + str(hidden_nodes) + 'nodes/weights.' + str(i) + '-*.hdf')
name = glob.glob('C:/Users/user/OneDrive - The Hong Kong Polytechnic University/EIE4433 FYP/Results/3 LSTM Layers D-2-2-25/' + str(input_num) +' PCA inputs StanNormData Diffferent Epochs/' + str(hidden_nodes) + 'nodes/weights.' + str(i) + '-*.hdf')
weights_path = name[0]
model.load_weights(weights_path)

# Load Data
print("\nNo. of nodes = ", str(hidden_nodes)) 
print("No. of Inputs = ", str(input_num)) 

showTest_output=[]
print('\nTraining Set: ')
print('---------------------------------------------------------')
for i in range(0, 76):
    test_output = model.predict(np.reshape(x_train[i],(1, 180, input_num)), verbose=0)
    showTest_output.append(test_output)
    # print('Real: ' + str(y_test[i]) + ', Predicted: ' + str(test_output))
showTest_output = np.reshape(showTest_output, (76, 1)).flatten().tolist()
y_train = y_train.tolist()
print("MSE:", mean_squared_error(y_train, showTest_output)) 
# Returns (Pearson’s correlation coefficient, 2-tailed p-value)
print("PCC:", pearsonr(y_train, showTest_output)[0])  
 
showTest_output=[]
print('\nTesting Set: ')
print('---------------------------------------------------------')
for i in range(0, 20):
    test_output = model.predict(np.reshape(x_test[i],(1, 180, input_num)), verbose=0)
    showTest_output.append(test_output)
    print(TestName[i] + ':\n    Real = ' + str(y_test[i]) + ', Predicted = ' + str(test_output) + '\n')
showTest_output = np.reshape(showTest_output, (20, 1)).flatten().tolist()
y_test = y_test.tolist()
print("MSE:", mean_squared_error(y_test, showTest_output))  
# Returns (Pearson’s correlation coefficient, 2-tailed p-value)
print("PCC:", pearsonr(y_test, showTest_output)[0])  

# showTest_output=[]
# print('\nEntire Dataset: ')
# for i in range(0, 96):
#     test_output = model.predict(np.reshape(x_all[i],(1, 180, input_num)), verbose=0)
#     showTest_output.append(test_output)
#     # print('Real: ' + str(y_all[i]) + ', Predicted: ' + str(test_output))
# showTest_output = np.reshape(showTest_output, (96, 1)).flatten().tolist()
# print("\nMSE:", mean_squared_error(y_all, showTest_output))  
# # Returns (Pearson’s correlation coefficient, 2-tailed p-value)
# print("PCC:", pearsonr(y_all, showTest_output))  



