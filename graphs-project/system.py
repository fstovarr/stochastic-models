import pandas as pd
from numpy import random as rd
from igraph import Graph, plot
from enum import Enum
from spectrum_analyzer import SpectrumAnalyzer
from antenna import Antenna
from util.propagation_model import PropagationModel
from scipy.optimize import fsolve

class System():
    def __init__(self, bounds=((0, 0), (1, 0), (1, 1), (0, 1)), antennas=10, csv_file=None, seed=0, verbose=False):
        """System that contains the antennas and the analyzer

        Args:
            bounds (tuple): Tuple with coordinates of the spacial system bounds. It starts from top-left and continues clockwise.
            antennas (int, optional): Number of randomly generated antennas. Defaults to 10.
            csv_file ([type], optional): Path of CSV to load custom antennas, if it is different to None, the previous argument 
            is ignored. Defaults to None.
            verbose (bool, optional): Verbose mode. Defaults to False.
            seed (int, optional): Seed of random generator. Defaults to 0.
        """
        rd.seed(seed)
        tx_power = 50
        freq = 9e8
        
        if csv_file == None:
            radio = self.__calc_radio__(tx_power, freq)
            self.__antennas = [Antenna(i, rd.rand(), rd.rand(), antennas, radio, tx_power=tx_power, freq=freq) for i in range(antennas)]
        else:
            self.__antennas = self.__read_file__(csv_file, tx_power=tx_power, freq=freq)
        self.__analyzer = SpectrumAnalyzer(bounds, verbose=True)

    def __read_file__(self, filename, tx_power=None, freq=None):
        data = pd.read_csv(filename).to_records()
        radio = self.__calc_radio__(tx_power, freq)
        return [Antenna(d[0], d[1], d[2], len(data), radio, tx_power=tx_power, freq=freq) for d in data]

    def __calc_radio__(self, tx_power, freq):
        initial_point = 0.5
        return fsolve(PropagationModel.log, initial_point, args=(tx_power, freq))
    
    def step(self):
        """Perform the actions that should be executed in each step of time
        """
        self.__analyzer.move()
        self.__analyzer.record_signals(self.__antennas)

    def get_antennas(self):
        return self.__antennas

    def get_analyzer(self):
        return self.__analyzer

    def set_frequencies(self, frequencies):
        pass