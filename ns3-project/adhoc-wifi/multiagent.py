#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2020 Fabio Steven Tovar Ramos <fabiostovarr@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse                                         # Load variables from command line
from ns3gym import ns3env                               # NS3 environment library
import pandas as pd                                     # Pandas to manage data
import matplotlib.pyplot as plt                         # Matplotlib to plot simulation data and training performance
from datetime import datetime                           # Datetime to get the current datetime

from agents.binary_agent import BinaryAgent                    # Agent 1
from agents.cognitive_agent import CognitiveAgent              # Agent 2
from nodes_helper import NodesHelper                    # Helper to make calculations over nodes
from simulators.binary_simulator import BinarySimulator            # Simulator for binary agent
from simulators.cognitive_simulator import CognitiveSimulator      # Simulator for binary agent
from math import ceil, log2

__author__ = "Fabio Steven Tovar Ramos"
__version__ = "1.0"
__email__ = "fstovarr@unal.edu.co"

parser = argparse.ArgumentParser(description='Start simulation script on/off')
parser.add_argument('--port',
                    type=int,
                    default=5555,
                    help='Start ns-3 simulation script on a specified port, Default: 1')
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
port = int(args.port)
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
agent2 = CognitiveAgent(3)
helper = NodesHelper()

binarySim = BinarySimulator(env, agent1, verbose=verbose)
cognitiveSim = CognitiveSimulator(env, agent2, verbose=verbose)

try:
    # Training
    if training:
        print("Training started")
        epTmp = episodes
        X = []
        Y = []
        
        while epTmp != 0:            
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
            df.to_csv("data/{}_{}_{}.csv".format(currentTime, episodes, stepsByEpisode), mode='a', header=False)
            df.to_csv("data/data.csv", mode='a', header=False)

    if training:    
        df = df[df['reward']==1].reset_index()          # Select valid data
        df.drop('index', axis=1, inplace=True)          # Delete index column

        X = df[['time', 'distance', 'radio']].to_numpy()            # Select training data for cognitive agent
        y = df['power'].to_numpy()                                  # Select goal
        
        # Model training
        history = agent2.learn(X, y, epochs=50, validation_data=(X_test, y_test), verbose=verbose)
        agent2.save_state()

        print("Learning finished")
    else:
        df = pd.read_csv("data/data.csv", index_col=0)            # Load data from file
        agent2.load_state()

    print("Start of environment execution")

    cognitive_results = []
    binary_results = []

    for i in range(41, stepsByEpisode + 1):
        # Choose a random initial action
        initial_action = env.get_random_action()

        seed += 1
        
        # Reset environment to real execution with the COGNITIVE AGENT
        cognitiveSim.reset(seed)
        X, Y = cognitiveSim.start(initial_action, i)
        if verbose:
            print(X)
            print(Y)
        totalPackages, ratePackages, totalPower = cognitiveSim.get_metrics()
        cognitive_results += [[i, totalPackages, ratePackages, totalPower]]
        print("COGNITIVE: Packages: {} | Rate: {}% | Accumulated power: {}".format(totalPackages, ratePackages * 100, totalPower))

        # Reset environment to real execution with the BINARY AGENT
        binarySim.reset(seed)
        binarySim.start(initial_action, i)
        if verbose:
            print(X)
            print(Y)
        totalPackages, ratePackages, totalPower = binarySim.get_metrics()
        binary_results += [[i, totalPackages, ratePackages, totalPower]]
        print("BINARY: Packages: {} | Rate: {}% | Accumulated power: {}".format(totalPackages, ratePackages * 100, totalPower))
    
    print("SAVING DATA")

    print(cognitive_results)
    print(binary_results)

    df_c = pd.DataFrame(cognitive_results, columns=['c_episode', 'c_packages', 'c_rate', 'c_power'])
    df_b = pd.DataFrame(binary_results, columns=['b_episode', 'b_packages', 'b_rate', 'b_power'])
    print(df_c)
    print(df_b)

    df = pd.concat([df_c, df_b], axis=1)
    print(df)
    df.to_csv("data/real_{}_{}_{}.csv".format(currentTime, episodes, stepsByEpisode), mode='a', header=False)
    df.to_csv("data/real_data.csv", mode='a', header=False)
except KeyboardInterrupt:
    print("Ctrl-C -> Exit")
finally:
    env.close()
    print("Done")
# ./multiagent.py --stepsByEpisode=25 --port=5558 --verbose=True