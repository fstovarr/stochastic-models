import numpy.random as rd
import numpy as np
from scipy.optimize import fsolve
from scipy.stats import truncexpon

class RandomGenerator():
    def __init__(self, distribution, lower_bound, upper_bound, seed=0):
        """Class constructor

        Args:
            distribution (string): Distribution of random generator
            args (exponential): lower bound, upper bound
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
