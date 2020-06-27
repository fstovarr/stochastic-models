from random_generator import RandomGenerator
from agent_helper import AgentHelper
from environment import Environment
from system import System
from store import Store

from multiprocessing import Process
from itertools import product
import numpy as np
import argparse
import random

__author__ = "Fabio Steven Tovar Ramos"
__version__ = "1.0"
__email__ = "fstovarr@unal.edu.co"

def start(data, seed):
    for d in data:
        distribution, sheets, agents = d
        try:
            store = Store(distribution, sheets, seed=seed)
            agn = AgentHelper.create_agents(int(agents), album_sheets=int(sheets))
            system = System(store, agn)

            env = Environment.create(system, store, limit_time=1000)
            env.start()
        except Exception as err:
            print("error with {},{} | {}".format(sheets, agents, err))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run simulation')
    parser.add_argument('--procs',
                        type=int,
                        default=4,
                        help='Proccesses to execute in the machine, Default: 4')
    
    parser.add_argument('--seed',
                        type=int,
                        default=0,
                        help='Seed of simulation, Default: 0')

    args = parser.parse_args()
    procs = int(args.procs)
    seed = int(args.seed)
    random.seed(seed)

    print("Running in {} processes".format(procs))

    sheets = [10, 20, 50, 100, 200, 400, 700, 1400]
    agents = [2, 5, 10, 20, 30, 50]

    distributions = [('exponential'), ('uniform')]
    seed = 0

    random.shuffle(sheets)
    random.shuffle(agents)

    cases = list(product(distributions, sheets, agents))
    cases_size = len(agents) * len(sheets) * len(distributions)
    bucket_size = cases_size // procs
    remainder = cases_size - bucket_size * procs
    processes = []

    for i in range(0, procs):
        seed += 1
        final_size = bucket_size
        if remainder > 0:
            remainder -= 1
            final_size += 1
        p = Process(target=start, args=(cases[i * final_size:(i + 1) * final_size], seed))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
