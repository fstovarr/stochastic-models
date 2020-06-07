#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from ns3gym import ns3env
from functools import reduce
import numpy as np
from math import sqrt
import tensorflow as tf
import tensorflow.contrib.slim as slim

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
simTime = 50            # seconds
stepTime = 1          # seconds
seed = 1
simArgs = { "--simTime": simTime,
            "--nNodes": 5 }
debug = False

env = ns3env.Ns3Env(port=port, stepTime=stepTime, startSim=startSim, simSeed=seed, simArgs=simArgs, debug=debug)
# simpler:
#env = ns3env.Ns3Env()
env.reset()

ob_space = env.observation_space
ac_space = env.action_space
print("Observation space: ", ob_space, ob_space.shape, ob_space.dtype)
print("Action space: ", ac_space, ac_space.shape, ac_space.dtype)

# a_size = ac_space.n
# model = tf.keras.Sequential()
# model.add(tf.keras.layers.Dense(s_size, input_shape=(s_size,), activation='relu'))
# model.add(tf.keras.layers.Dense(a_size, activation='softmax'))
# model.compile(optimizer=tf.train.AdamOptimizer(0.001),
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])

total_episodes = 200
max_env_steps = 100
env._max_episode_steps = max_env_steps

epsilon = 1.0               # exploration rate
epsilon_min = 0.01
epsilon_decay = 0.999

time_history = []
rew_history = []

stepIdx = 0
currIt = 0

def calc_action(reward, action, top, bottom):
    if top >= bottom:
        if reward == 1:
            top = action
        else:
            bottom = action
    return (bottom + (top - bottom) // 2, top, bottom)

def calc_distance(v1, v2):
    return sqrt((v2[0] - v1[0]) ** 2 + (v2[1] - v1[1]) ** 2)

def calc_radius(positions_list):
    positions = np.array(positions_list)

    # Calculate centroid
    centroid = np.average(positions, axis=0)

    # Calculate max radius
    max_radius = 0
    for pos in positions:
        max_radius = max(max_radius, calc_distance(centroid, pos))
    return max_radius

# try:
#     while True:
#         print("Start iteration: ", currIt)
#         obs = env.reset()
#         print("Step: ", stepIdx)
#         # print("---obs:", obs)

#         bottom = 0
#         top = env.action_space.n
#         action = env.action_space.sample()

#         while True:
#             stepIdx += 1

#             obs, reward, done, info = env.step(action)
#             radius = calc_radius(obs[2])

#             action, top, bottom = calculate_action(reward, action, top, bottom)
#             print("--- action {} top {} bottom {} ".format(action, top, bottom))
        
#             if done:
#                 stepIdx = 0
#                 if currIt + 1 < iterationNum:
#                     env.reset()
#                 break

#         currIt += 1
#         if currIt == iterationNum:
#             break

# except KeyboardInterrupt:
#     print("Ctrl-C -> Exit")
# finally:
#     env.close()
#     print("Done")