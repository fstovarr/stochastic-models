import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import EarlyStopping

from joblib import load, dump
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class CognitiveAgent:
    def __init__(self, input_size):        
        self.model = Sequential()
        self.model.add(Dense(500, activation='relu', input_dim=(input_size)))
        self.model.add(Dense(250, activation='relu'))
        self.model.add(Dense(100, activation='relu'))
        self.model.add(Dense(1))
        self.model.compile(loss='mse',
              optimizer=SGD(),
              metrics=['mae', 'mse'])
        self.early_stop = EarlyStopping(monitor='val_loss', patience=30)

        self.scalers = []

    def load_state(self):
        try:
            self.model.load_weights('states/adhoc_wifi.h5')
            self.scalers = [load('states/x_scaler.joblib'), load('states/y_scaler.joblib')]
        except:
            print("WARNING | Agent states not found, please check the folder 'states'")

    def save_state(self):
        if len(self.scalers) > 0:
            dump(self.scalers[0], 'states/x_scaler.joblib') 
            dump(self.scalers[1], 'states/y_scaler.joblib')
        self.model.save_weights('states/adhoc_wifi.h5')

    def data_preprocessing(self, X, y):
        # Divide data in training and test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
        
        # Data normalization
        scaler = StandardScaler().fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        y_scaler = StandardScaler().fit(y_train.reshape(-1,1))
        y_train = y_scaler.transform(y_train.reshape(-1,1))
        y_test = y_scaler.transform(y_test.reshape(-1,1))

        self.scalers = [scaler, y_scaler]

        return (X_train, y_train, X_test, y_test)
                
    def learn(self, X, y, validation_data=None, epochs=3):
        if validation_data == None:
            X_train, X_test, y_train, y_test = self.data_preprocessing(X, y)
            validation_data = (X_test, y_test)
        return self.model.fit(X, y, epochs=epochs, validation_data=validation_data, verbose=1, callbacks=[self.early_stop])
        
    def get_action(self, x):
        x = np.array(x).reshape(-1, 3)
        prediction = self.scalers[1].inverse_transform(self.model.predict(x))
        return np.round(prediction.reshape(1)[0])