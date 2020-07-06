from util.propagation_model import PropagationModel

class Antenna():
    def __init__(self, idx, x, y, total, radio, frequency=None, verbose=False, tx_power=50, freq=9e8):
        self.position = {'x': x, 'y': y}
        self.__total = total
        self.__frequency = frequency
        self.__idx = idx
        self.__verbose = verbose
        self.__tx_power = tx_power
        self.__freq = freq

        self.__radio = radio
        
        self.name = "Tower {}".format(idx)
        self.shortname = "T{}".format(idx)

    def get_radio(self):
        return self.__radio

    def get_signal(self, distance):
        if self.__frequency == None:
            raise Exception("Frequency not assigned")
        return (self.__frequency, self.__calc_signal__(distance))
    
    def set_frequency(self, frequency):
        self.__frequency = frequency

    def __calc_signal__(self, distance):
        if self.__frequency == None:
            raise Exception("Frequency not assigned")
        
        if self.__verbose:
            print(self.__idx, distance, self.__radio)

        loss = PropagationModel.log(distance, self.__tx_power, self.__freq)

        signal = [0] * self.__total
        signal[self.__idx] = 1 if loss > 0 else 0

        return signal
    
    def __str__(self):
        return "Antenna {}: frequency {}".format(self.__idx, self.__frequency)