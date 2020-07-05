from math import sin, pi
import numpy.random as rd

class SpectrumAnalyzer():
    def __init__(self, bounds, speed=0.5, initial_direction=None, initial_position={'x': 0, 'y': 0}, verbose=False):
        self.__speed = speed
        self.__direction = dict()
        self.__position = initial_position
        self.perceived_signals = dict()
        self.__verbose = verbose

        self.change_direction(initial_direction)
    
    def move(self):
        flag = False

        while not flag:
            alpha = 90 - self.__direction['deg']
            c = sin(alpha * pi / 180) * self.__speed + self.__position['x']
            d = sin(self.__direction['rad']) * self.__speed + self.__position['y']

            self.__position['x'] = c
            self.__position['y'] = d

            if not self.__in_bounds(self.__position):
                self.change_direction(90 - self.__direction['deg'])
            else:
                flag = True
        if self.__verbose:
            print(self.__position)
        return self.__position

    def change_direction(self, direction=None):
        if direction == None:
            direction = self.__get_random_direction()

        self.__direction['deg'] = direction
        self.__direction['rad'] = direction * pi / 180
        
        if self.__verbose:
            print(self.__direction)

    def record_signals(self, antennas):
        for a in antennas:
            frequency, signal = a.get_signal()
            if not frequency in self.perceived_signals:
                self.perceived_signals[frequency] = signal
            else:
                self.perceived_signals[frequency] = [a + b for a, b in zip(signal, self.perceived_signals[frequency])]

        if self.__verbose:
            print(self.perceived_signals)
    
    def clear_signals(self):
        self.perceived_signals.clear()

    def reset(self, initial_position=None):
        self.__position = { 'x': 0, 'y': 0 }
        self.change_direction()
        self.clear_signals()

    def __get_random_direction(self):
        return rd.randint(0, 360)

    def __in_bounds_(self, position):
        return (position['x'] >= self.__bounds[0][0] and
            position['x'] < self.__bounds[1][0] and
            position['y'] >= self.__bounds[0][1] and
            position['y'] < self.__bounds[2][1])