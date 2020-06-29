from agent import AgentState
from datetime import datetime
from pathlib import Path
from enum import Enum

class SystemState(Enum):
    """Enum that represents the state of the system
    """
    COMPLETED = 1
    RUNNING = 0

class System():
    """System that will be contain the agents and handle the interactions
    """
    def __init__(self, store, agents, verbose=False):
        self.__store = store
        self.__agents = agents
        self.__full_agents = []
        self.__state = SystemState.RUNNING
        self.__verbose = verbose
    
    def step(self):
        """Perform the actions that should be executed in each step of time

        Returns:
            list: Completed agents in this time step
        """
        full_agents = []
        agents = self.__buy_stage()
        if len(agents) > 0:
            full_agents.extend(agents)
        
        agents_2 = self.__exchange_stage()
        if len(agents_2) > 0:
            full_agents.extend(agents_2)
        
        if self.__verbose:
            print(' '.join(str(a) for a in self.__agents))
            print("Total: {}\tCompleted: {}".format(len(self.__agents), len(self.__full_agents)))
            print("-------------------------\n")

        if len(self.__full_agents) == len(self.__agents):
            self.__state = SystemState.COMPLETED

        self.__full_agents.extend(full_agents)
        return full_agents

    def get_agents_count(self):
        return len(self.__agents)

    def get_full_agents_count(self):
        return len(self.__full_agents)

    def get_state(self):
        return self.__state

    def __buy_stage(self):
        """Stage where agents buy new sheets

        Returns:
            list: Completed agents in this step
        """
        full_agents = []

        for agent in self.__agents:
            if agent.get_state() == AgentState.LOOKING_FOR_SHEETS:
                sheet = self.__store.get_sheet()
                if self.__verbose:
                    print("Sheet {}".format(sheet))
                agent.save_sheet(sheet)
                if agent.get_state() == AgentState.COMPLETED:
                    full_agents.append([agent, "buy"])
        return full_agents

    def __exchange_stage(self):
        """Stage where the agents do some exchanges based on their necessity

        Returns:
            list: Completed agents in this stage
        """
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
