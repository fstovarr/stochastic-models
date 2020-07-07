from system import System
from observer import Observer
from agents.greedy import NaiveAgent, DSaturAgent
from agents.dummy_agent import DummyAgent

class Environment():
    def __init__(self, system, agent, limit_time=40000, verbose=False):
        """Ambiente de ejecución

        Args:
            system (System): Sistema que actuará sobre el ambiente
            agent (Agent): Agente que resolverá el problema
            limit_time (int, optional): Tiempo límite de la simulación. Defaults to 40000.
            verbose (bool, optional): Modo verboso. Defaults to False.
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
            agent (string | Agent): Agente de la simulación
            antennas (int, optional): Número de antenas. Defaults to 10.
            limit_time (int, optional): Tiempo límite de simulación. Defaults to 40000.
            seed (int, optional): Seed del generador de números aleatorios. Defaults to 0.
            verbose (bool, optional): Modo verboso. Defaults to False.

        Returns:
            Environment: Ambiente creado de acuerdo a las características solicitadas
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