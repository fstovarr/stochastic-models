import numpy as np
from enum import Enum
from graph_helper import GraphHelper
from igraph import Graph, plot

class AgentState(Enum):
    """Enum that represents the possible states of the agent
    """
    COMPLETED = 1

class NaiveAgent():
    """Model of the agent who wants to fill its album through simulation
    """

    def __init__(self, nodes, radio):
        """Class constructor

        Args:
            album_sheets (int, optional): Album total sheets. Defaults to 700.
            idx (int, optional): Agent Identifier. Defaults to 0.
        """
        self.__radio = radio
        self.__g = Graph()
        self.__data = nodes
        self.__distances = np.zeros((len(nodes), len(nodes)))
        self.__build_graph(nodes)
    
    def __build_graph(self, data):
        for (i, row) in enumerate(self.__data):
            self.__g.add_vertex(x=row[0], y=row[1], name="Tower {}".format(i), label="T{}".format(i))

        for (i, row) in enumerate(self.__g.vs):
            for j in range(i):
                self.__distances[i][j] = self.__distances[j][i] = GraphHelper.calc_distance(row, self.__g.vs[j])
                if self.__distances[i][j] <= self.__radio:
                    self.__g.add_edge(self.__g.vs[i], self.__g.vs[j])
    
    def distances(self):
        return self.__distances

    def solve(self):
        colors = self.__colouring_graph__(self.__g)
        gen_colors = GraphHelper.get_colors(colors)
        for (i, v) in enumerate(self.__g.vs):
            v['color'] = gen_colors[v['color']]
        
        return colors
    
    def __colouring_graph__(self, G):
        adj = list(G.get_adjacency())
        available_colors = [True] * (len(G.vs))
        colors = [None] * (len(G.vs))
        max_color = 0

        for vertex in G.vs:
            indexes = []
            for neighbor in vertex.neighbors():
                if colors[neighbor.index] != None:
                    available_colors[colors[neighbor.index]] = False
                    indexes.append(colors[neighbor.index])
            color = next(i for (i, value) in enumerate(available_colors) if value)
            colors[vertex.index] = color
            vertex["color"] = color
            max_color = max(max_color, color)

            for i in indexes:
                available_colors[i] = True
        return max_color + 1

    def get_graph(self):
        return self.__g