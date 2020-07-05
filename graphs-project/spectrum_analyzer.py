from math import sin, pi
import numpy.random as rd
from util.graph_helper import GraphHelper

class SpectrumAnalyzer():
    def __init__(self, bounds, speed=0.01, initial_direction=None, initial_position={'x': 0, 'y': 0}, verbose=False):
        self.__speed = speed
        self.__direction = dict()
        self.__position = initial_position
        self.__bounds = bounds
        self.perceived_signals = dict()
        self.__verbose = verbose
        self.__overlapping = 0

        self.change_direction(initial_direction)
    
    def move(self):
        flag = False

        while not flag:
            alpha = (90 - self.__direction['deg']) % 360
            c = sin(alpha * pi / 180) * self.__speed + self.__position['x']
            d = sin(self.__direction['rad']) * self.__speed + self.__position['y']

            self.__position['x'] = c
            self.__position['y'] = d

            if not self.__in_bounds__(self.__position):
                #self.change_direction((self.__direction['deg'] - 90) % 360)
                self.change_direction()
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
            print("Dir ", self.__direction)

    def record_signals(self, antennas):
        modified = [False] * len(antennas)
        
        for a in antennas:
            frequency, signal = a.get_signal(GraphHelper.calc_distance(a.position, self.__position))

            if not frequency in self.perceived_signals:
                self.perceived_signals[frequency] = signal
            else:
                for i in range(len(signal)):
                    if modified[frequency]:
                        self.__overlapping += 1
                    self.perceived_signals[frequency][i] = self.perceived_signals[frequency][i] + signal[i]
            modified[frequency] = True

        if self.__verbose:
            print(self.perceived_signals, self.__overlapping)
    def get_overlapping(self):
        return self.__overlapping

    def clear_signals(self):
        self.perceived_signals.clear()

    def reset(self, initial_position=None):
        self.__position = { 'x': 0, 'y': 0 }
        self.change_direction()
        self.clear_signals()

    def __get_random_direction(self):
        return rd.randint(0, 360)

    def __in_bounds__(self, position):
        return (position['x'] >= self.__bounds[0][0] and
            position['x'] < self.__bounds[1][0] and
            position['y'] >= self.__bounds[0][1] and
            position['y'] < self.__bounds[2][1])