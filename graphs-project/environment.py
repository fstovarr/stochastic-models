from system import System
from observer import Observer
from agents.greedy import NaiveAgent, DSaturAgent
from agents.dummy_agent import DummyAgent

class Environment():
    """Representation of the environment in which the system and the observer will perform
    """
    def __init__(self, system, agent, limit_time=40000, verbose=False):
        self.__time = 0
        self.__limit_time = limit_time
        self.__system = system
        self.__agent = agent
        self.__observer = Observer()

    @classmethod
    def create(cls, agent, antennas=10, limit_time=40000, seed=0, verbose=False):
        sys = System(antennas=antennas, seed=seed)
        if agent == 'dsatur':
            _agent = DSaturAgent(sys.get_antennas())
        elif agent == 'naive':
            _agent = NaiveAgent(sys.get_antennas())
        elif agent == 'dummy':
            _agent = DummyAgent(sys.get_antennas())
        return cls(sys, _agent, limit_time=limit_time, verbose=verbose)

    def start(self):
        self.__agent.solve()

        while self.__limit_time > self.__time:
            self.__system.step()
            self.__observer.collect_metrics(self.__time, self.__agent, self.__system.get_analyzer())
            self.__time += 1
        
        if self.__limit_time == self.__time:
            print("LIMIT REACHED")
        print("Simulation ended")

    def get_agent(self):
        return self.__agent