from enum import Enum

class Album():
    def __init__(self, size=700):
        self.size = size
        self.__state = [False] * size
        self.__state_count = 0
        self.__surplus = [0] * size
        self.__surplus_count = 0
    
    def add_sheet(self, sheet):
        if self.is_full():
            raise Exception("The album is already full")

        if self.__state[sheet] == False:
            self.__state[sheet] = True
            self.__state_count += 1
        else:
            self.__surplus[sheet] += 1
            self.__surplus_count += 1
    
    def get_missing(self):
        return list(filter(lambda x: not x[1], enumerate(self.__state)))

    def is_full(self):
        return self.__state_count == self.size

    def has_surplus(self):
        return self.__surplus_count > 0

    def get_surplus_count(self):
        return self.__surplus_count

    def get_surplus(self):
        return list(filter(lambda x: x[1] > 0, enumerate(self.__surplus)))

    def remove_surplus(self, sheet):
        if self.__surplus[sheet] == 0:
            raise Exception("This sheet doesn't exist")
        else:
            self.__surplus[sheet] -= 1

    def __str__(self):
        return '\t|\t'.join(str(i) + ' x' if s else str(i) + ' -' for (i, s) in enumerate(self.__state)) + '\n' + '\t|\t'.join("{} {}".format(i, s) for (i, s) in enumerate(self.__surplus))