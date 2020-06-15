#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse                                         # Load variables from command line
from ns3gym import ns3env                               # NS3 environment library
import pandas as pd                                     # Pandas to manage data
import matplotlib.pyplot as plt                         # Matplotlib to plot simulation data and training performance
from sklearn.model_selection import train_test_split    # SKLearn to divide the data between training and test
from datetime import datetime                           # Datetime to get the current datetime

from agents.binary_agent import BinaryAgent                    # Agent 1
from agents.cognitive_agent import CognitiveAgent              # Agent 2
from nodes_helper import NodesHelper                    # Helper to make calculations over nodes
from simulators.binary_simulator import BinarySimulator            # Simulator for binary agent
from simulators.cognitive_simulator import CognitiveSimulator      # Simulator for binary agent

__author__ = "Fabio Steven Tovar Ramos"
__version__ = "1.0"
__email__ = "fstovarr@unal.edu.co"

parser = argparse.ArgumentParser(description='Start simulation script on/off')
parser.add_argument('--start',
                    type=int,
                    default=1,
                    help='Start ns-3 simulation script automatically 0/1, Default: 1')
parser.add_argument('--simTime',
                    type=int,
                    default=4000,
                    help='Simulation time (s), Default: 4000')
parser.add_argument('--stepTime',
                    type=int,
                    default=5,
                    help='Time of each step (s), Default: 5')
parser.add_argument('--training',
                    type=bool,
                    default=False,
                    help='Training mode, Default: false')
parser.add_argument('--verbose',
                    type=bool,
                    default=False,
                    help='Verbose mode, Default: false')
parser.add_argument('--episodes',
                    type=int,
                    default=10,
                    help='Training Episodes, Default: 10')
parser.add_argument('--stepsByEpisode',
                    type=int,
                    default=30,
                    help='Steps by episode in trainig, Default: 30')

args = parser.parse_args()

now = datetime.now()
currentTime = now.strftime("%d%m%Y%H%M%S")

# Simulation variables
startSim = bool(args.start)
simTime = int(args.simTime)
stepTime = int(args.stepTime)
verbose = bool(args.verbose)
port = 5555
seed = 1
simArgs = { "--simTime": simTime, '--stepTime': stepTime }
debug = False

# Training variables
training = bool(args.training)
episodes = int(args.episodes)
stepsByEpisode = int(args.stepsByEpisode)

# NS3 Environment creation
env = ns3env.Ns3Env(port=port, stepTime=stepTime, startSim=startSim, simSeed=seed, simArgs=simArgs, debug=debug)
env.reset()

total_actions = env.action_space.n
action = 0
last_radio = -1
radio = -1

# Agents instantiation
agent1 = BinaryAgent(total_actions)
agent2 = CognitiveAgent(3, total_actions)
helper = NodesHelper()

binarySim = BinarySimulator(env, agent1, verbose=verbose)
cognitiveSim = CognitiveSimulator(env, agent2, verbose=verbose)

try:
    # Training
    if training:
        epTmp = episodes
        while epTmp != 0:
            X = []
            Y = []
            
            seed += 1                                               # Change the simulation seed for each episode
            initial_action = env.get_random_action()                # Choose a random initial action
            binarySim.reset(seed)                                   # Reset simulation and set the new seed
            X, Y = binarySim.start(initial_action, stepsByEpisode)  # Start simulation and get data

            epTmp -= 1                                              # Update episodes counter
            
            if verbose:
                print("------------- SAVE FILE --------------------")

            # Save data in a csv file after each episode 
            df_x = pd.DataFrame(X, columns=['time', 'radio', 'reward', 'distance'])
            df_y = pd.DataFrame({'power': Y})
            df = pd.concat([df_x, df_y], axis=1)
            df.to_csv("{}_{}_{}.csv".format(currentTime, episodes, stepsByEpisode), mode='a', header=False)
            df.to_csv("data.csv", mode='a', header=False)

    if not training:
        df = pd.read_csv("14062020222635_10_30.csv", index_col=0, )            # Load data from file
    
    df = df[df['reward']==1].reset_index()          # Select valid data
    df.drop('index', axis=1, inplace=True)          # Delete index column

    X = df[['time', 'distance', 'radio']].to_numpy()            # Select training data for cognitive agent
    Y = df['power'].to_numpy()                      # Select goal

    # Divide data in training and test
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        Y,
                                                        test_size=0.2,
                                                        random_state=2)

    # Model training
    history = agent2.learn(X_train, y_train, epochs=50, validation_data=(X_test, y_test), verbose=verbose)

    print("Learning finished\nStart of environment execution")

    # Choose a random initial action
    initial_action = env.get_random_action()
    
    # Reset environment to real execution with the COGNITIVE AGENT
    cognitiveSim.reset()
    cognitiveSim.start(initial_action, 20)
    totalPackages, ratePackages, totalPower = cognitiveSim.get_metrics()
    print("COGNITIVE: Packages: {} | Rate: {}% | Accumulated power: {}".format(totalPackages, ratePackages * 100, totalPower))

    # Reset environment to real execution with the BINARY AGENT
    binarySim.reset()
    binarySim.start(initial_action, 20)
    totalPackages, ratePackages, totalPower = binarySim.get_metrics()
    print("BINARY: Packages: {} | Rate: {}% | Accumulated power: {}".format(totalPackages, ratePackages * 100, totalPower))
except KeyboardInterrupt:
    print("Ctrl-C -> Exit")
finally:
    env.close()
    print("Done")
