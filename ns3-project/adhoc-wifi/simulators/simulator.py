import sys
sys.path.append("..")

from nodes_helper import NodesHelper

class Simulator:
    """This class allows to different agents perform in an enviroment in an easy and reusable way
    """
    def __init__(self, env, agent, verbose=False):
        """Class constructor

        Arguments:
            env {Ns3Env} -- NS3 environment
            agent {Agent} -- Agent

        Keyword Arguments:
            verbose {bool} -- Verbose mode (default: {False})
        """
        self.env = env
        self.agent = agent
        self.helper = NodesHelper()
        self.verbose = verbose
        self.totalPower = 0
        self.receivedPackages = 0
        self.time = 0
        self.steps = 0
    
    def reset(self, seed=1):
          """Reset the simulator state and the enviroment

        Keyword Arguments:
            seed {int} -- NS3 environment seed (default: {1})
        """
        self.env.set_seed(seed)
        self.env.reset()
        self.agent.reset()
        self.time = 0
        self.totalPower = 0
        self.receivedPackages = 0
        self.steps = 0
    
    def get_metrics(self):
        """Get metrics of the simulator

        Returns:
            tuple -- (Received packets, Received packets rate, Total power)
        """
        return (self.receivedPackets, self.receivedPackets / (self.steps), self.totalPower)

    def start(self):
        """Override this function to give the necessary behavior to your agent
        """
        pass