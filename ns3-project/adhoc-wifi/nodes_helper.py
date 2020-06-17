import numpy as np
from functools import reduce
from math import sqrt

class NodesHelper:
    def get_centroid(self, positions):
        """Function to calculate the centroid of an array of coordinates

        Arguments:
            positions {array} -- Array of cardinal coordinates

        Returns:
            array -- Centroid of the array [x, y]
        """
        return np.average(positions, axis=0)

    def get_radio(self, positions_list):
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

    def calc_distance(self, v1, v2):
        """Function to calculate the distance between two points 

        Arguments:
            v1 {array} -- 2D Vector
            v2 {array} -- 2D Vector

        Returns:
            float -- Distance between vectors
        """
        return sqrt((v2[0] - v1[0]) ** 2 + (v2[1] - v1[1]) ** 2)