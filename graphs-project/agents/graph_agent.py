import sys
sys.path.append('..')

from .agent import Agent
from igraph import Graph
from util.graph_helper import GraphHelper

class GraphAgent(Agent):
    def __init__(self, nodes):
        """Agente abstracto que permite resolver el problema mediante manipulación de grafos

        Args:
            nodes (list): Lista de antenas para armar el grafo
        """
        super().__init__()

        self._data = nodes
        self._radio = nodes[0].get_radio() * 2
        self._g = Graph()
        self._build_graph_(nodes)

    def get_graph(self):
        return self._g

    def get_data(self):
        return self._data

    def _build_graph_(self, data):
        pass