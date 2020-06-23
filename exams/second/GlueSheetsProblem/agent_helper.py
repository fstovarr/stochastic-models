from agent import Agent
from random_generator import RandomGenerator

class AgentHelper():
    @staticmethod
    def create_agents(num_agents, album_sheets=700):
        agents = [Agent(album_sheets=album_sheets, idx=i) for i in range(num_agents)]
        rd = RandomGenerator()
        if num_agents > 1:        
            for agent in agents:
                friends = rd.get_int(0, album_sheets - 1)
                for i in range(friends):
                    friend = agents[rd.get_int(0, album_sheets - 1)]
                    while friend != agent and friend.idx != agent.idx:
                        friend = agents[rd.get_int(0, album_sheets - 1)]
                    agent.add_friend(friend)
                    friend.add_friend(agent)
        return agents

        