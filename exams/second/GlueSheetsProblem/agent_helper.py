from agent import Agent
from random_generator import RandomGenerator

class AgentHelper():
    """Helper to create easier the agents and its relationships

    Returns:
        list: List of friends
    """
    @staticmethod
    def create_agents(num_agents, album_sheets=700):
        agents = [Agent(album_sheets=album_sheets, idx=i) for i in range(num_agents)]
        rd = RandomGenerator('uniform', 0, num_agents - 1)
        if num_agents > 1:        
            for agent in agents:
                max_recursions = 10
                friends = rd.get_int()
                for i in range(friends):
                    m = rd.get_int()
                    friend = agents[m]
                    while friend != agent and friend.idx != agent.idx and max_recursions > 0:
                        friend = agents[rd.get_int()]
                        max_recursions -= 1
                    agent.add_friend(friend)
                    friend.add_friend(agent)
        return agents
