#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from ns3gym import ns3env
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from binary_agent import BinaryAgent
from cognitive_agent import CognitiveAgent
from nodes_helper import NodesHelper

__author__ = "Fabio Steven Tovar Ramos"
__version__ = "0.1.0"
__email__ = "fstovarr@unal.edu.co"

parser = argparse.ArgumentParser(description='Start simulation script on/off')
parser.add_argument('--start',
                    type=int,
                    default=1,
                    help='Start ns-3 simulation script 0/1, Default: 1')
parser.add_argument('--iterations',
                    type=int,
                    default=1,
                    help='Number of iterations, Default: 1')
args = parser.parse_args()
startSim = bool(args.start)
iterationNum = int(args.iterations)

port = 5555
simTime = 20
stepTime = 5
seed = 0
simArgs = {"--simTime": simTime}
debug = False

env = ns3env.Ns3Env(port=port, stepTime=stepTime, startSim=1, simSeed=seed, simArgs=simArgs, debug=debug)
env.reset()

total_actions = env.action_space.n

action = 0
last_radio = -1
radio = -1
episodes = 1
stepsByEpisode = 3
verbose = True
training = True

agent1 = BinaryAgent(total_actions)
agent2 = CognitiveAgent(2, total_actions)
helper = NodesHelper()

X = []
Y = []

try:
    if training:
        epTmp = episodes
        while epTmp != 0:
            env.reset()
            agent1.reset()
            sbeTmp = stepsByEpisode
            action = 0
            last_radio = -1
            while sbeTmp != 0:
                obs, reward, done, info = env.step(action)
                radio = helper.get_radio(obs[2])
                
                if verbose:
                    print("Step: {}\tAction: {}\tReward: {}\tRadio: {}".format(stepsByEpisode - sbeTmp, action, reward, radio))
                
                if last_radio != radio and last_radio != -1:
                    X.append([stepsByEpisode - sbeTmp, last_radio])
                    Y.append(action)
                    action = 0
                    sbeTmp -= 1
                    agent1.reset()
                else:
                    action = agent1.get_action(reward, action)
                last_radio = radio
            epTmp -= 1

    if not training:
        df = pd.read_csv("data.csv", index_col=0)
    else:
        df_x = pd.DataFrame(X, columns=['time', 'radio'])
        df_y = pd.DataFrame({'power': Y})
        df = pd.concat([df_x, df_y], axis=1)
        df.to_csv("data2.csv", mode='a', header=False)
    
    # X = df[['radio', 'time']].to_numpy()
    # Y = df['power'].to_numpy()

    # X_train, X_test, y_train, y_test = train_test_split(X,
    #                                                     Y,
    #                                                     test_size=0.2,
    #                                                     random_state=2)

    # print(X_train)
    # # history = agent2.learn(X_train, y_train, epochs=400)

    # # plt.plot(history.history['accuracy'])
    # plt.savefig("learning.png")

    # plot = df.plot()
    # fig = plot.get_figure()
    # fig.savefig("plot.png")

    # radio = helper.get_radio(obs[2])
    # action = agent2.get_action(radio)
    # print("------- radio {} / action {}".format(radio, action))
    # obs, reward, done, info = env.step(action)
except KeyboardInterrupt:
    print("Ctrl-C -> Exit")
finally:
    env.close()
    print("Done")