import numpy.random as rd

class RandomGenerator():
    def __init__(self, seed=0):
        rd.seed(seed)
        self.__rg = rd
        self.idx = -1
        self.tmp = [3, 1, 2, 3, 1, 2, 3, 1, 2]

    def get_value(self, low, high):
        #return self.__rg.randint(low, high)
        self.idx += 1
        return self.tmp[self.idx]
