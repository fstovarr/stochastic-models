import sys
sys.path.append("..")

from .agent import Agent

import numpy as np

from util.graph_helper import GraphHelper
from igraph import Graph, plot

class GreedyAgent(Agent):
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
        for (i, antenna) in enumerate(self.__data):
            self.__g.add_vertex(x=antenna.position['x'], y=antenna.position['y'], name=antenna.name, label=antenna.shortname, antenna=antenna)

        for (i, row) in enumerate(self.__g.vs):
            for j in range(i):
                self.__distances[i][j] = self.__distances[j][i] = GraphHelper.calc_distance(row, self.__g.vs[j])
                if self.__distances[i][j] <= self.__radio:
                    self.__g.add_edge(self.__g.vs[i], self.__g.vs[j])
    
    def distances(self):
        return self.__distances

    def solve(self):
        colors = self._colouring_graph_(self.__g)
        gen_colors = GraphHelper.get_colors(colors)
        for (i, v) in enumerate(self.__g.vs):
            v['antenna'].set_frequency(v['color'])
            v['color'] = gen_colors[v['color']]
        return colors
    
    def _colouring_graph_(self, G):
        pass

    def get_data(self):
        return self.__data

    def get_graph(self):
        return self.__g

class DSaturAgent(GreedyAgent):
    def _colouring_graph(self):
        degrees = G.degree()
    
        available_colors = [True] * (len(G.vs))
        colors = [None] * (len(G.vs))
        max_color = 0
        
        vertices = dict()
        for v in G.vs:
            vertices[v.index] = (0, v.degree(), v.index)
        
        while len(vertices) > 0:
            index, item = max(enumerate(vertices.values()), key=lambda p: p[1][0])        
            vertex = G.vs[item[2]]
            
            for neighbor in vertex.neighbors():
                if colors[neighbor.index] != None:
                    available_colors[colors[neighbor.index]] = False

            color = next(i for (i, value) in enumerate(available_colors) if value)
            colors[vertex.index] = color
            vertex["color"] = color
            max_color = max(max_color, color)

            for neighbor in vertex.neighbors():
                if colors[neighbor.index] != None:
                    available_colors[colors[neighbor.index]] = True
                if neighbor.index in vertices:
                    vertices[neighbor.index] = (
                        vertices[neighbor.index][0] + 1, 
                        vertices[neighbor.index][1], 
                        vertices[neighbor.index][2]
                    )
            del vertices[vertex.index]
            
        return max_color + 1

class NaiveAgent(GreedyAgent):
    """Model of the agent who wants to fill its album through simulation
    """
    def _colouring_graph_(self, G):
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