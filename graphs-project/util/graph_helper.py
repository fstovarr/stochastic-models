import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from .graph_artist import GraphArtist

from functools import reduce
from math import sqrt

class GraphHelper:
    @staticmethod
    def get_colors(n):
        colors = []
        for i in range(0, 360, 360 // n):
            colors.append('hsl(%d, %d%%, %d%%)' % (i, 90 + np.random.rand() * 10, 50 + np.random.rand() * 10))
        return colors
    
    @staticmethod
    def get_centroid(positions):
        """Function to calculate the centroid of an array of coordinates

        Arguments:
            positions {array} -- Array of cardinal coordinates

        Returns:
            array -- Centroid of the array [x, y]
        """
        return np.average(positions, axis=0)

    @staticmethod
    def get_radio(positions_list):
        """Function to calculate the radio of an array of cardinal coordinates

        Arguments:
            positions_list {array} -- Array of cardinal coordinates

        Returns:
            float -- Radio of the array
        """
        positions = np.array(positions_list)

        # Calculate centroid
        centroid = self.get_centroid(positions)

        # Calculate max radius
        max_radio = 0
        for pos in positions:
            max_radio = max(max_radio, self.calc_distance(centroid, pos))
        return max_radio
    
    @staticmethod
    def calc_distance(v1, v2):
        """Function to calculate the distance between two points 

        Arguments:
            v1 {array} -- 2D Vector
            v2 {array} -- 2D Vector

        Returns:
            float -- Distance between vectors
        """
        return sqrt((v2['x'] - v1['x']) ** 2 + (v2['y'] - v1['y']) ** 2)
    
    @staticmethod
    def plot(graph, figsize=(10, 10), fig=None, ax=None):
        matplotlib.use("cairo")        
        if ax == None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width, height = bbox.width, bbox.height

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        graph_artist = GraphArtist(graph, bbox, fig.dpi)
        ax.artists.append(graph_artist)
        
        if fig != None:
            return fig, ax
        return ax