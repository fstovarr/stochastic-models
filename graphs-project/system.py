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
        """Sistema contenedor de las antenas y el analizador, junto con su interacción

        Args:
            bounds (tuple, optional): Tupla de tuplas, que contiene las coordenadas de los límites del espacio de movimiento
                iniciando desde la esquina superior izquierda y siguiendo en sentido horario. Defaults to ((0, 0), (1, 0), (1, 1), (0, 1)).
            antennas (int, optional): Cantidad de antenas a generar aleatoriamente. Defaults to 10.
            csv_file ([type], optional): Ruta relativa del archivo CSV que permite cargar antenas personalizadas, si es diferente de None, 
                el anterior argumento es ignorado. Defaults to None.
            seed (int, optional): Semilla para generar números aleatorios. Defaults to 0.
            verbose (bool, optional): Modo verboso. Defaults to False.
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