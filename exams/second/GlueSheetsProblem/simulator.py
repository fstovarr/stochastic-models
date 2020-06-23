from agent import AgentState

class Simulator():
    def __init__(self, env, agents, time=400):
        self.__time = 0
        self.__env = env
        self.__agents = agents
        self.__limit_time = time

    def reset(self):
        self.__time = 0
    
    def start(self):
        while self.__limit_time > self.__time:
            self.buy_stage()
            self.exchange_stage()
            
            print(''.join(str(a) for a in self.__agents))
            print ("-------------------------\n")
            
            self.__time += 1

    def buy_stage(self):
        for agent in self.__agents:
            if agent.get_state() == AgentState.LOOKING_FOR_SHEETS:
                sheet = self.__env.get_sheet()
                print ("Sheet {}".format(sheet))
                agent.save_sheet(sheet)

    def exchange_stage(self):
        print("EXCHANGING")
        for agent in self.__agents:
            if agent.has_surplus():
                agent.try_exchanging()