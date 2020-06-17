import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import EarlyStopping

from joblib import load, dump
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from agent import Agent

class CognitiveAgent(Agent):
    def __init__(self, input_size):
        """Class constructor

        Arguments:
            input_size {integer} -- Size of the input of the neuronal network
        """
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
        """Load a pre-saved agent
        """
        try:
            self.model.load_weights('states/adhoc_wifi.h5')
            self.scalers = [load('states/x_scaler.joblib'), load('states/y_scaler.joblib')]
        except:
            print("WARNING | Agent states not found, please check the folder 'states'")

    def save_state(self):
        """Save the learning of the agent and the data scalers
        """
        if len(self.scalers) > 0:
            dump(self.scalers[0], 'states/x_scaler.joblib') 
            dump(self.scalers[1], 'states/y_scaler.joblib')
        self.model.save_weights('states/adhoc_wifi.h5')

    def data_preprocessing(self, X, y):
        """Function to divide the data in train and test, and normalize it

        Arguments:
            X {array} -- Observations
            y {array} -- Targets

        Returns:
            tuple -- Train and test data divied, normalized and mixing
        """
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
        """Function to fit the neuronal network to certain data

        Arguments:
            X {array} -- Observations
            y {array} -- Targets

        Keyword Arguments:
            validation_data {tuple} -- Custom validation data, if None is calculated (default: {None})
            epochs {int} -- Epochs of the training model (default: {3})

        Returns:
            history -- Learning performance
        """
        if validation_data == None:
            X_train, X_test, y_train, y_test = self.data_preprocessing(X, y)
            validation_data = (X_test, y_test)
        return self.model.fit(X, y, epochs=epochs, validation_data=validation_data, verbose=1, callbacks=[self.early_stop])
        
    def get_action(self, x):
        """Get an action according to an determined observation

        Arguments:
            x {array} -- Sample to get a prediction

        Returns:
            integer -- Action to perform
        """
        x = np.array(x).reshape(-1, 3)
        prediction = self.scalers[1].inverse_transform(self.model.predict(x))
        return int(np.round(prediction.reshape(1)[0]))