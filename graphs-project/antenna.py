from util.propagation_model import PropagationModel

class Antenna():
    def __init__(self, idx, x, y, total, radio, frequency=None, verbose=False, tx_power=50, freq=9e8):
        """Antena que simula la transmisión de las señales 

        Args:
            idx (int): Identificador de la antena
            x (double): Posición de la antena en el eje coordenado x
            y (double): Posición de la antena en el eje coordenado y
            total (int): Cantidad de antenas total en el sistema
            radio (double): Radio de referencia indicando el máximo alcance
            frequency (int, optional): Selección de la banda de frecuencia donde transmitirá. Defaults to None.
            tx_power (int, optional): Poder de transmisión en dBm. Defaults to 50.
            verbose (bool, optional): Modo verboso. Defaults to False.
        """
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

    def get_frequency(self):
        return self.__frequency
        
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