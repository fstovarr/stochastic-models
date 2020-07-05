from .agent import Agent

class DummyAgent(Agent):
    def __init__(self, nodes, radio):
        self.__data = nodes

    def solve(self):
        for d in self.__data:
            print(d)
            d.set_frequency(0)

        # map(lambda a: a.set_frequency(0), self.__data)
        print("----------")

        for d in self.__data:
            print(d)
