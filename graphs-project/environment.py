from system import System
from observer import Observer
from agents.greedy import NaiveAgent, DSaturAgent
from agents.dummy_agent import DummyAgent

class Environment():
    def __init__(self, system, agent, limit_time=40000, verbose=False):
        """Environment constructor

        Args:
            system (System): Systems that will be perform in the environment
            agent (Agent): Agent which will solve the problem
            limit_time (int, optional): Simulation limit time. Defaults to 40000.
            verbose (bool, optional): Verbose mode. Defaults to False.
        """
        self.__time = 0
        self.__limit_time = limit_time
        self.__system = system
        self.__agent = agent
        self.__observer = Observer()

    @classmethod
    def create(cls, agent, antennas=10, limit_time=40000, seed=0, verbose=False):
        """Función para crear un ambiente completo

        Args:
            agent (string | Agent): Simulation agent
            antennas (int, optional): Number of antennas. Defaults to 10.
            limit_time (int, optional): Simulation limit time. Defaults to 40000.
            seed (int, optional): Seed of random generator. Defaults to 0.
            verbose (bool, optional): Verbose mode. Defaults to False.

        Returns:
            Environment
        """
        sys = System(antennas=antennas, seed=seed)
        if isinstance(agent, str):
            if agent == 'dsatur':
                _agent = DSaturAgent(sys.get_antennas())
            elif agent == 'naive':
                _agent = NaiveAgent(sys.get_antennas())
            elif agent == 'dummy':
                _agent = DummyAgent(sys.get_antennas())
        else:
            _agent = agent(sys.get_antennas())
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