import sys
sys.path.append('..')

from .agent import Agent
from igraph import Graph
from util.graph_helper import GraphHelper

class GraphAgent(Agent):
    def __init__(self, nodes, radio):
        super().__init__()

        self._data = nodes
        self._radio = radio
        self._g = Graph()
        self._build_graph_(nodes)

    def get_graph(self):
        return self._g

    def get_data(self):
        return self._data

    def _build_graph_(self, data):
        pass