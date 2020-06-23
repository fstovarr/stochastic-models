from agent import AgentState
from datetime import datetime
from pathlib import Path

class Simulator():
    def __init__(self, env, agents, time=400, verbose=False):
        self.__time = 0
        self.__env = env
        self.__agents = agents
        self.__limit_time = time
        self.__full_agents = []
        self.__general_filename = "data/data.csv"
        self.__specific_filename = "data/{}_.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))
        self.__verbose = verbose
        
        self.__init_file()

    def reset(self):
        self.__time = 0
    
    def start(self):
        full_agents = []
        while (self.__limit_time != None and self.__limit_time > self.__time) or self.__limit_time == None:
            agents = self.buy_stage()
            if len(agents) > 0:
                full_agents.extend(agents)
            
            agents_2 = self.exchange_stage()
            if len(agents_2) > 0:
                full_agents.extend(agents_2)
            
            if self.__verbose:
                print(' '.join(str(a[0]) for a in full_agents))
                print(str(self.__agents[7]))
                print("Total: {}\tCompleted: {}".format(len(self.__agents), len(self.__full_agents)))
                print("-------------------------\n")
            
            self.__full_agents.extend(full_agents)
            self.__collect_metrics(full_agents)

            if self.__limit_time == None and len(self.__full_agents) == len(self.__agents):
                break
            self.__time += 1
            full_agents = []
        print("Simulation ended")

    def buy_stage(self):
        full_agents = []

        for agent in self.__agents:
            if agent.get_state() == AgentState.LOOKING_FOR_SHEETS:
                sheet = self.__env.get_sheet()
                if self.__verbose:
                    print("Sheet {}".format(sheet))
                agent.save_sheet(sheet)
                if agent.get_state() == AgentState.COMPLETED:
                    full_agents.append([agent, "buy"])
        return full_agents

    def exchange_stage(self):
        full_agents = []
        flags = [False, False]
        
        for agent in self.__agents:
            if agent.has_surplus():
                flags[0] = agent.get_state() == AgentState.LOOKING_FOR_SHEETS
                (friend_list, own_list, friend) = agent.look_for_exchange()
                
                flags[1] = friend.get_state() == AgentState.LOOKING_FOR_SHEETS
                agent.do_exchange(friend_list, own_list, friend)

                if flags[0] and agent.get_state() == AgentState.COMPLETED:
                    full_agents.append([agent, "exchange"])
                if flags[1] and friend.get_state() == AgentState.COMPLETED:
                    full_agents.append([friend, "exchange"])
        return full_agents

    ### Private functions
    def __init_file(self):
        # TODO time,sheets,id,friends,surplus,agents,full_agents,stage
        Path(self.__general_filename).touch()
        Path(self.__specific_filename).touch()

    def __collect_metrics(self, agents):
        metrics = ""
        for (agent, stage) in agents:
            metrics = "{},{},{},{},{},{}\n".format(self.__time, self.__env.get_sheets_count(), agent.get_metrics(), len(self.__agents), len(self.__full_agents), stage)
        if metrics != "":
            f = open(self.__general_filename, "a+")
            f2 = open(self.__specific_filename, "a+")
            f.write(metrics)
            f2.write(metrics)
            f.close()
            f2.close()