import numpy as np
from functools import reduce
from math import sqrt

class NodesHelper:
    def get_centroid(self, positions):
        return np.average(positions, axis=0)

    def get_radio(self, positions_list):
        positions = np.array(positions_list)

        # Calculate centroid
        centroid = self.get_centroid(positions)

        # Calculate max radius
        max_radio = 0
        for pos in positions:
            max_radio = max(max_radio, self.calc_distance(centroid, pos))
        return max_radio

    def calc_distance(self, v1, v2):
        return sqrt((v2[0] - v1[0]) ** 2 + (v2[1] - v1[1]) ** 2)