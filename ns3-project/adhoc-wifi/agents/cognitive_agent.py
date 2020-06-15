import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical
import numpy as np
import tf_slim as slim
from math import ceil

class CognitiveAgent:
    def __init__(self, input_size, output_size):
        self.numClasses = output_size
        
        self.model = Sequential()
        self.model.add(Dense(256, input_shape=(input_size,)))
        self.model.add(Activation('sigmoid'))
        self.model.add(Dense(output_size))
        self.model.add(Activation('softmax'))
        
        self.model.compile(loss='categorical_crossentropy',
              optimizer=SGD(),
              metrics=['accuracy'])
    
    def evaluate(X_test, Y_test):
        return self.model.evaluate(X_test, Y_test, verbose=2)
                
    def learn(self, X, Y, epochs=3, validation_data=None, verbose=False):
        Y = to_categorical(Y, self.numClasses)
        y_test = to_categorical(validation_data[1], self.numClasses)
        if verbose:
            k_ver = 2
        else:
            k_ver = 0
        return self.model.fit(X, Y, epochs=epochs, validation_data=(validation_data[0], y_test), verbose=k_ver)
        
    def get_action(self, time, distance, radio):
        prediction = self.model.predict([[time, distance, radio]])
        return np.argmax(prediction)