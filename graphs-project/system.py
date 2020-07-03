import pandas as pd
from numpy import random as rd
from igraph import Graph, plot
from enum import Enum

class SystemState(Enum):
    """Enum that represents the state of the system
    """
    COMPLETED = 1
    RUNNING = 0

class System():
    """System that will be contain the agents and handle the interactions
    """
    def __init__(self, verbose=False):
        self.__state = SystemState.RUNNING
        self.__verbose = verbose
        self.__data = [[rd.rand(), rd.rand()] for i in range(100)]
    
    def step(self):
        """Perform the actions that should be executed in each step of time

        Returns:
            list: Completed agents in this time step
        """
        pass

    def getTowers(self):
        return self.__data

    def plot(self):
        plot(self.__g)