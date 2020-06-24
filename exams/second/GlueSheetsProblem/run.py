from simulator import Simulator
from agent import Agent
from environment import Environment
from agent_helper import AgentHelper
import numpy as np

for sheets in np.linspace(10, 700, 100):
    for agents in np.linspace(1, 30, 10):
        try:
            agn = AgentHelper.create_agents(int(agents), album_sheets=int(sheets))
            env = Environment(album_sheets=int(sheets))
            simulator = Simulator(env, agn)
            simulator.start()
        except:
            print("error with {},{}".format(sheets, agents))

print("Run finished")
