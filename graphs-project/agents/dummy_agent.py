import sys
sys.path.append('..')

from .graph_agent import GraphAgent
from igraph import Graph
from util.graph_helper import GraphHelper

class DummyAgent(GraphAgent):
    def _build_graph_(self, data):
        for (i, antenna) in enumerate(self._data):
            self._g.add_vertex(x=antenna.position['x'], y=antenna.position['y'], name=antenna.name, label=antenna.shortname, antenna=antenna)

    def solve(self):
        for d in self._data:
            d.set_frequency(0)
        self._frequencies = 1