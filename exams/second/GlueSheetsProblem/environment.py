from random_generator import RandomGenerator
from system import System, SystemState

class Environment():
    def __init__(self, rg, system, observer, limit_time=40000, album_sheets=700, verbose=False):
        self.__time = 0
        self.__rg = rg
        self.__sheets_count = album_sheets
        self.__system = system
        self.__observer = observer

    def start():
        while self.__limit_time > self.__time and self.__system.get_state() != SystemState.COMPLETED:
            full_agents = self.__system.step()
            if len(full_agents) > 0:
                self.__observer.collect_metrics(full_agents)
            self.__time += 1
        
        if self.__limit_time == self.__time:
            print("LIMIT REACHED in case {} {}".format(self.__env.get_sheets_count(), len(self.__agents)))
        print("Simulation ended")

    def get_sheet(self):
        return self.__rg.get_int()

    def get_sheets_count(self):
        return self.__sheets_count

    def get_distribution(self):
        return self.__rg.distribution