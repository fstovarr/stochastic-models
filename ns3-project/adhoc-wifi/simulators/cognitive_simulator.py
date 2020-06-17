import sys
sys.path.append("..")
from nodes_helper import NodesHelper

class CognitiveSimulator:
    def __init__(self, env, agent, verbose=False):
        self.env = env
        self.agent = agent
        self.helper = NodesHelper()
        self.verbose = verbose
        self.totalPower = 0
        self.receivedPackages = 0
        self.time = 0
        self.steps = 0
    
    def reset(self, seed=1):
        self.env.reset()
        self.time = 0
        self.totalPower = 0
        self.receivedPackages = 0
        self.steps = 0

    def get_metrics(self):
        return (self.receivedPackages, self.receivedPackages / (self.steps), self.totalPower)

    def start(self, initial_action, steps):
        X = []
        Y = []

        radio = -1
        action = initial_action
        lastReward = 0
        lastRadio = -1
        lastDistance = 0

        while steps > 0:
            self.totalPower += action
            self.steps += 1
            obs, reward, done, info = self.env.step(action)             # Execute action and move in time
            
            radio = self.helper.get_radio(obs[2])                            # Nodes distribution radio
            distance = self.helper.calc_distance(obs[2][0], obs[2][-1])      # Distance between source and receiver nodes
            
            if self.verbose:
                print("Step: {}\tAction: {}\tReward: {}\tRadio: {}".format(self.time, action, reward, radio))
            
            # If the agents change their position, save the optimal action found
            if lastRadio != radio and lastRadio != -1:
                X.append([self.time, lastRadio, lastReward, lastDistance])   # Save time, radio, reward, and distance between source and receiver
                Y.append(action)                                    # Save the found action
                steps -= 1
                self.time += 1                                      # Update steps counter
            
            action = self.agent.get_action(self.time + 1, distance, radio)      # Calculate the next action according to the reward and action
            
            lastRadio = radio                                       # Update last radio
            lastReward = reward                                     # Update last reward
            lastDistance = distance                                 # Update last distance
        
        self.receivedPackages = obs[1][0]
        return (X, Y)