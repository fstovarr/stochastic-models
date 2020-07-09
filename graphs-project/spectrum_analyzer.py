from math import sin, pi
import numpy.random as rd
import numpy as np
from util.graph_helper import GraphHelper

class SpectrumAnalyzer():
    def __init__(self, bounds, speed=0.01, initial_direction=None, initial_position={'x': 0, 'y': 0}, verbose=False, seed=0):
        """Spectrum analyzer constructor

        Args:
            bounds (tuple): Tuple with coordinates of the spacial system bounds. It starts from top-left and continues clockwise
            speed (float, optional): Speed of spectrum analyzer. Defaults to 0.01.
            initial_direction (int, optional): Initial direction in degrees (0, 360). Defaults to None.
            initial_position (dict | tuple, optional): Tuple or dict containing initial coordinates (x,y) of the analyzer. Defaults to {'x': 0, 'y': 0}.
            verbose (bool, optional): Verbose mode. Defaults to False.
            seed (int, optional): Seed of random generator. Defaults to 0.
        """
        
        rd.seed(seed)

        if type(initial_position) is tuple:
            initial_position = {'x': initial_position[0], 'y': initial_position[1]}

        self.position = initial_position
        self.perceived_signals = dict()

        self.__speed = speed
        self.__direction = dict()
        self.__bounds = bounds
        self.__verbose = verbose
        self.__overlapping = 0

        self.change_direction(initial_direction)
    
    def move(self):
        flag = False

        alpha = (90 - self.__direction['deg']) % 360
        c = sin(alpha * pi / 180) * self.__speed + self.position['x']
        d = sin(self.__direction['rad']) * self.__speed + self.position['y']

        if not self.__in_bounds__({'x': c, 'y': d}): 
            self.change_direction()
        else:
            self.position['x'] = c
            self.position['y'] = d

        if self.__verbose:
            print(self.position)
        return self.position

    def change_direction(self, direction=None):
        if direction == None:
            direction = self.__get_random_direction()

        self.__direction['deg'] = direction
        self.__direction['rad'] = direction * pi / 180
        
        if self.__verbose:
            print("Direction {}, position: {} ".format(self.__direction, self.position))

    def record_signals(self, antennas):
        perceived = dict()

        for a in antennas:
            overlap = 0
            distance = GraphHelper.calc_distance(a.position, self.position)
            frequency, signal = a.get_signal(distance)

            if not frequency in perceived:
                perceived[frequency] = signal
            else:
                for i in range(len(signal)):
                    perceived[frequency][i] = perceived[frequency][i] + signal[i]
            
        for p in perceived.values():
            self.__overlapping += sum(p) if sum(p) > 1 else 0
        
        if self.__verbose:
            print(perceived, self.__overlapping)
    
    def get_overlapping(self):
        return self.__overlapping

    def clear_signals(self):
        self.perceived_signals.clear()

    def reset(self, initial_position=None):
        self.position = { 'x': 0, 'y': 0 }
        self.change_direction()
        self.clear_signals()

    def __get_random_direction(self):
        return rd.randint(0, 360)

    def __in_bounds__(self, position):
        return (position['x'] >= self.__bounds[0][0] and
            position['x'] < self.__bounds[1][0] and
            position['y'] >= self.__bounds[0][1] and
            position['y'] < self.__bounds[2][1])
    
    def __adjust_to_bounds__(self, position):

        if position['x'] >= self.__bounds[0][0]:
            position['x'] = self.__bounds[0][0]
        elif position['x'] < self.__bounds[1][0]:
            position['x'] = self.__bounds[1][0]
        elif position['y'] >= self.__bounds[0][1]:
            position['y'] = self.__bounds[0][1]
        elif position['y'] < self.__bounds[2][1]:
            position['y'] = self.__bounds[2][1]

        return position