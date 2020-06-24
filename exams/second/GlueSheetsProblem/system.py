from agent import AgentState
from datetime import datetime
from pathlib import Path
from enum import Enum

class SystemState(Enum):
    COMPLETED = 1
    RUNNING = 0

class System():
    def __init__(self, env, agents, verbose=False):
        self.__env = env
        self.__agents = agents
        self.__full_agents = []
        self.__state = SystemState.RUNNING
        self.__verbose = verbose
    
    def step(self):
        full_agents = []
        agents = self.__buy_stage()
        if len(agents) > 0:
            full_agents.extend(agents)
        
        agents_2 = self.__exchange_stage()
        if len(agents_2) > 0:
            full_agents.extend(agents_2)
        
        if self.__verbose:
            print(' '.join(str(a[0]) for a in full_agents))
            print("Total: {}\tCompleted: {}".format(len(self.__agents), len(self.__full_agents)))
            print("-------------------------\n")
            
        self.__full_agents.extend(full_agents)
        return full_agents

    def get_state(self):
        return self.__state

    def __buy_stage(self):
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

    def __exchange_stage(self):
        full_agents = []
        flags = [False, False]
        
        for agent in self.__agents:
            if agent.has_surplus():
                flags[0] = agent.get_state() == AgentState.LOOKING_FOR_SHEETS
                possible_exchange = agent.look_for_exchange()

                if possible_exchange != None:
                    (friend_list, own_list, friend) = possible_exchange
                    flags[1] = friend.get_state() == AgentState.LOOKING_FOR_SHEETS
                    agent.do_exchange(friend_list, own_list, friend)

                    if flags[0] and agent.get_state() == AgentState.COMPLETED:
                        full_agents.append([agent, "exchange"])
                    
                    if flags[1] and friend.get_state() == AgentState.COMPLETED:
                        full_agents.append([friend, "exchange"])
        return full_agents
