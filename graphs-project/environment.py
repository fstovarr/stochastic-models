from system import System
from observer import Observer
from agents.greedy import NaiveAgent, DSaturAgent

class Environment():
    """Representation of the environment in which the system and the observer will perform
    """
    def __init__(self, system, agent, limit_time=40000, verbose=False):
        self.__time = 0
        self.__limit_time = limit_time
        self.__system = system
        self.__agent = agent
        # self.__observer = Observer()

    @classmethod
    def create(cls, system, agent, radio=0.3, limit_time=40000):
        if agent == 'dsatur':
            agent = DSaturAgent(system.get_antennas(), radio)
        elif agent == 'naive':
            agent = NaiveAgent(system.get_antennas(), radio)
        return cls(system, agent, limit_time=limit_time)

    def start(self):
        self.__agent.solve()

        while self.__limit_time > self.__time:
            self.__system.step()
            self.__time += 1
        
        if self.__limit_time == self.__time:
            print("LIMIT REACHED")
        print("Simulation ended")