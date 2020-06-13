from functools import reduce
import numpy as np

class BinaryAgent:
    def __init__(self, top):
        self.original_top = top
        self.top = top
        self.bottom = 0
    
    def get_action(self, reward, action):
        if self.top > self.bottom:
            if reward == 1:
                self.top = action
            else:
                self.bottom = action + 1
        return self.bottom + (self.top - self.bottom) // 2

    def reset(self):
        self.top = self.original_top
        self.bottom = 0