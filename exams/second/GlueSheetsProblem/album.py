from enum import Enum

class Album:
    def __init__(self, size=700):
        self.size = 700
        self.__state = [False] * size
        self.__state_count = 0
        self.__surplus = [0] * size
        self.__surplus_count = 0
    
    def add_sheet(self, sheet):
        if self.is_completed():
            raise Exception("The album is already full")

        if self.__state[sheet] == False:
            self.__state[sheet] = True
            self.__state_count += 1
        else:
            self.__surplus[sheet] += 1
            self.__surplus_count += 1
    
    def get_surplus(self, sheet):
        if self.__surplus[sheet] > 0:
            self.__surplus_count -= 1
            return self.__surplus[sheet]
        else
            return None
    
    def get_missing(self):
        return filter(lambda i, x: not x, enumerate(self.__state))

    def is_full(self):
        return self.__state_count == self.__size

    def has_surplus(self):
        return self.__surplus_count > 0

    def get_surplus(self):
        return filter(lambda i, x: x > 0, enumerate(self.__surplus))

    def remove_surplus(self, sheet):
        self.__surplus[sheet] -= 1