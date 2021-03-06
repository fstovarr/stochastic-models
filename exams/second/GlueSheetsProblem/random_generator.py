import numpy.random as rd
import numpy as np
from scipy.optimize import fsolve
from scipy.stats import truncexpon
import pandas as pd

class RandomGenerator():
    def __init__(self, distribution, lower_bound, upper_bound, seed=0):
        """Class constructor

        Args:
            distribution (string): Distribution of random generator ('exponential' or 'uniform')
            lower_bound (int): Lower bound of numbers generated
            upper_bound (int): Upper bound of numbers generated
            seed (int, optional): Random generator seed. Defaults to 0.
        """
        rd.seed(seed)
        self.distribution = distribution
        self.__random_args = [lower_bound, upper_bound]
        self.__set_random(distribution)

    def get_int(self):
        return int(np.round(self.__rg(*self.__random_args)))

    def __set_random(self, distribution):
        if distribution == 'uniform':
            self.__rg = rd.randint
            self.__random_args[1] += 1
        elif distribution == 'exponential':
            def func(scale, desired_mean, x1, x2):
                return truncexpon.mean((x2 - x1)/scale, loc=x1, scale=scale) - desired_mean
            x1 = self.__random_args[0]
            x2 = self.__random_args[1]
            desired_mean = np.round((x2 - x1) * 0.35)
            scale_guess = 4.0
            scale = fsolve(func, scale_guess, args=(desired_mean, x1, x2))[0]
            shape = (x2 - x1)/scale
            self.__random_args = [shape, x1, scale]
            self.__rg = truncexpon.rvs
        elif distribution == 'binomial':
            self.rg = rd.binomial
            self.__random_args = [self.__random_args[1], 0.5]
        elif distribution == 'custom':
            data = self.__load_file('data/custom_distribution.csv')

    def __load_file(self, filename):
        data = pd.read_csv(filename)
        data.loc[-1] = (-1, 0)
        data = data.sort_values('sheet').reset_index()
        data.drop('index', axis=1, inplace=True)
        data['sheet'] = list(data.index)
        data['distribution'] = data['distribution'].cumsum()

        if (1 - data["distribution"].iloc[-1]) > 1e-6:
            raise Exception("The sum of probabilities must be 1")
        self.__random_args = [data]
        self.__rg = self.__custom_random

    def __custom_random(self, data):
        n = np.random.uniform()
        low = 0
        top = len(data) - 1
        while top - low > 1:
            middle = low + (top - low) // 2
            if n > data.loc[middle]['distribution']:
                low = middle
            elif n < data.loc[middle]['distribution']:
                top = middle
        return data.loc[low + (top - low) // 2]["sheet"]