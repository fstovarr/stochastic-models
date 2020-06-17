from functools import reduce
import numpy as np
from agent import Agent

class BinaryAgent(Agent):
    """Agent that adjust their value through a binary search
    """
    def __init__(self, top):
        """Class constructor

        Arguments:
            top {integer} -- Maximum possible action
        """
        self.original_top = top
        self.top = top
        self.bottom = 0
    
    def get_action(self, reward, action):
        """Function that according to a reward and its action, calculate the next action

        Arguments:
            reward {integer} -- 1 or 0
            action {integer} -- The action to get that reward

        Returns:
            integer -- Next action
        """
        if self.top > self.bottom:
            if reward == 1:
                self.top = action
            else:
                self.bottom = action + 1
        return self.bottom + (self.top - self.bottom) // 2

    def reset(self):
        """Reset the agent of its original values
        """
        self.top = self.original_top
        self.bottom = 0