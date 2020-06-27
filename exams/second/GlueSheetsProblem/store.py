from random_generator import RandomGenerator

class Store():
    def __init__(self, distribution, sheets, seed=1):
        self.distribution = distribution
        self.__rg = RandomGenerator(distribution, 0, int(sheets - 1), seed=seed)
    
    def get_sheet(self):
        return self.__rg.get_int()