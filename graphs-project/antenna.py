class Antenna():
    def __init__(self, idx, x, y, total, frequency=None):
        self.position = {'x': x, 'y': y}
        self.__total = total
        self.__frequency = frequency
        self.__idx = idx
        
        self.name = "Tower {}".format(idx)
        self.shortname = "T{}".format(idx)

    def get_signal(self, distance):
        if self.__frequency == None:
            raise Exception("Frequency not assigned")
        return (self.__frequency, self.__calc_signal__(distance))
    
    def set_frequency(self, frequency):
        self.__frequency = frequency

    def __calc_signal__(self, distance):
        if self.__frequency == None:
            raise Exception("Frequency not assigned")

        signal = [0] * self.__total
        signal[self.__idx] = 1
        return signal
    
    def __str__(self):
        return "<index {}, frequency {}>".format(self.__idx, self.__frequency)