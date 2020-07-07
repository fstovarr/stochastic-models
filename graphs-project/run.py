from environment import Environment

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
        antennas, agent_type = d

        try:
            env = Environment.create(
                agent_type,
                antennas=antennas,
                limit_time=100,
                seed=1,
                verbose=False
            )
            env.start()
        except Exception as err:
            print("error with {}, {} | {}".format(agent_type, antennas, err))

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

    antennas = [5, 10, 15, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    agents = ['naive', 'dummy', 'dsatur']

    random.shuffle(antennas)
    random.shuffle(agents)

    cases = list(product(antennas, agents))
    cases_size = len(antennas) * len(agents)
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
