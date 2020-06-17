import sys
sys.path.append("..")
from nodes_helper import NodesHelper
from simulator import Simulator

class CognitiveSimulator(Simulator):
    """This class allows to the cognitive agent performing in an easy and reusable way
    """

    def start(self, initial_action, steps):
        """Start the simulation

        Arguments:
            initial_action {integer} -- Initial action of the agent
            steps {integer} -- Number of nodes position variations

        Returns:
            tuple -- Data collected by the simulator, i.e. time, radio, reward and distance in the first position, and the corresponding power in the second
        """
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
            
            action = self.agent.get_action([self.time + 1, distance, radio])      # Calculate the next action according to the reward and action
            
            lastRadio = radio                                       # Update last radio
            lastReward = reward                                     # Update last reward
            lastDistance = distance                                 # Update last distance
        
        self.receivedPackets = obs[1][0]
        return (X, Y)