from system import System, SystemState
from observer import Observer

class Environment():
    """Representation of the environment in which the system and the observer will perform
    """
    def __init__(self, system, store, limit_time=40000, verbose=False):
        self.__time = 0
        self.__limit_time = limit_time

        self.__system = system
        self.__store = store
        self.__observer = Observer()

    @classmethod
    def create(cls, system, store, limit_time=40000):
        return cls(system, store, limit_time=limit_time)

    def start(self):
        while self.__limit_time > self.__time and self.__system.get_state() != SystemState.COMPLETED:
            full_agents = self.__system.step()
            if len(full_agents) > 0:
                self.__observer.collect_metrics(self.__time, full_agents, self.__store.distribution, self.__system.get_agents_count(), self.__system.get_full_agents_count())
            self.__time += 1
        
        if self.__limit_time == self.__time:
            print("LIMIT REACHED in case {} {}".format(self.__system.get_agents_count(), 2))
        print("Simulation ended")