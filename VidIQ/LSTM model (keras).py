# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 00:39:17 2020

@author: user
"""

"""
References:
    https://stackabuse.com/solving-sequence-problems-with-lstm-in-keras/ 
    https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.pearsonr.html
    https://blog.csdn.net/xys430381_1/article/details/80680167
    https://www.programcreek.com/python/example/104416/keras.callbacks.ModelCheckpoint
    https://keras.io/callbacks/
    https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/CSVLogger
    https://www.tensorflow.org/tutorials/keras/save_and_load
    https://www.tensorflow.org/tutorials/keras/overfit_and_underfit
    https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html
"""

import warnings
warnings.filterwarnings("ignore")
# Imports
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dropout, Dense
from keras.layers import LSTM, GRU
# from keras.regularizers import l1, l2
import pandas as pd
# from keras import optimizers
from scipy.stats.stats import pearsonr
from sklearn.metrics import mean_squared_error, accuracy_score
from keras.callbacks import Callback, ModelCheckpoint, CSVLogger
import matplotlib.pyplot as plt

class haltCallback(Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('loss') < 0.3 and logs.get('val_loss') <= 1):
            print("\nReached 1 val_loss value so cancelling training!")
            self.model.stop_training = True

input_num = 12

# Training Inputs
x_train = pd.read_excel('StanNormTrainingData.xlsx')
x_train = x_train.reset_index().values
x_train = np.delete(x_train, [0, 1, 3], 1)  # 3s2t:0, 1, 3, 6, 7, 8, 9, 10, 11, 12
x_train = np.reshape(x_train, (76, 180, input_num))

# Training Outputs
y_train = pd.read_excel('TrainingScores.xlsx')
y_train = y_train.reset_index().values
y_train = np.delete(y_train, [0, 1, 3, 4], 1)
y_train = np.reshape(y_train, (1, 76)).flatten()

# Testing Inputs
x_test = pd.read_excel('StanNormTestingData.xlsx')
x_test = x_test.reset_index().values
x_test = np.delete(x_test, [0, 1, 3], 1)
x_test = np.reshape(x_test, (20, 180, input_num))

# Testing Outputs
y_test = pd.read_excel('TestingScores.xlsx')
y_test = y_test.reset_index().values
y_test = np.delete(y_test, [0, 1, 3, 4], 1)
y_test = np.reshape(y_test, (1, 20)).flatten()

hidden_nodes = 80
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
model_filepath = 'Results/3 LSTM Layers D-2-2-25/12 inputs StanNormData Different Epochs/' + str(hidden_nodes) + 'nodes/weights.{epoch:02d}-{val_loss:.4f}.hdf'
model_checkpoint = ModelCheckpoint(model_filepath, monitor='val_loss', verbose=1, save_best_only=False)
log_filepath = 'Results/3 LSTM Layers D-2-2-25/12 inputs StanNormData Different Epochs/' + str(hidden_nodes) + 'nodes-training.log'
csv_logger = CSVLogger(log_filepath)
callbacks=[model_checkpoint, csv_logger] #, model_checkpoint, csv_logger
history = model.fit(x_train, y_train, epochs=10000, validation_split=0.2, verbose=1, batch_size=60, callbacks=callbacks)

# Test
showTest_output=[]
print('\n')
for i in range(0, 20):
    test_output = model.predict(np.reshape(x_test[i],(1, 180, input_num)), verbose=0)
    showTest_output.append(test_output)
    print('Real: ' + str(y_test[i]) + ', Predicted: ' + str(test_output))
    
showTest_output = np.reshape(showTest_output, (20, 1)).flatten().tolist()
y_test = y_test.tolist()
print("\nNo. of nodes = ", str(hidden_nodes)) 
print("\nNo. of Inputs = ", str(input_num)) 
# Returns (Pearson’s correlation coefficient, 2-tailed p-value)
print("\nPCC:", pearsonr(y_test, showTest_output))  
print("\nMSE:", mean_squared_error(y_test, showTest_output))  

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['loss', 'val_loss'], loc='upper left')
plt.title(str(hidden_nodes) + ' Nodes - Loss and Validation Loss Graph')
plt.grid()
plt.show()
