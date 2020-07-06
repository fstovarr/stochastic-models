import pandas as pd
from numpy import random as rd
from igraph import Graph, plot
from enum import Enum
from spectrum_analyzer import SpectrumAnalyzer
from antenna import Antenna
from util.propagation_model import PropagationModel
from scipy.optimize import fsolve

class System():
    """System that will be contain the agents and handle the interactions
    """
    def __init__(self, antennas=10, bounds=((0, 0), (1, 0), (1, 1), (0, 1)), seed=0, verbose=False):
        rd.seed(seed)
        tx_power = 50
        freq = 9e8

        self.__antennas = [Antenna(i, rd.rand(), rd.rand(), antennas, self.__calc_radio__(tx_power, freq), tx_power=tx_power, freq=freq) for i in range(antennas)]
        self.__analyzer = SpectrumAnalyzer(bounds, verbose=True)

    def __calc_radio__(self, tx_power, freq):
        initial_point = 0.5
        return fsolve(PropagationModel.log, initial_point, args=(tx_power, freq))
    
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