import pandas as pd
from numpy import random as rd
from igraph import Graph, plot
from enum import Enum
from spectrum_analyzer import SpectrumAnalyzer
from antenna import Antenna

class System():
    """System that will be contain the agents and handle the interactions
    """
    def __init__(self, antennas=10, bounds=((0, 0), (1, 0), (1, 1), (0, 1)), seed=0, verbose=False):
        rd.seed(seed)

        self.__antennas = [Antenna(i, rd.rand(), rd.rand(), antennas, .05) for i in range(antennas)]
        self.__analyzer = SpectrumAnalyzer(bounds, verbose=True)
    
    def step(self):
        """Perform the actions that should be executed in each step of time

        Returns:
            list: Completed agents in this time step
        """
        self.__analyzer.move()
        self.__analyzer.record_signals(self.__antennas)

    def get_antennas(self):
        return self.__antennas

    def set_frequencies(self, frequencies):
        pass