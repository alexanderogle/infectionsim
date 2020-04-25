import pandas as pd
import numpy as np
import time
import sys
import resource
import matplotlib.pyplot as plt
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
sys.setrecursionlimit(10**6)

def mean(x):
    return sum(x)/len(x)

class ConnectionEngine():
    def __init__(self,num_people=None,num_connections=None):
        self.num_people = num_people
        self.num_connections = num_connections

    def _build_connection_list(self,agent,population,num_connections):
        # Break ounter
        #if _cnt == 0:
        #    _cnt += 1
        # Return IDs of people with connections less than num_connections
        available_to_connect = (
            lambda agent,population: population.drop(agent).query('num_connections < {}'
                                                                     .format(num_connections)
                                                                    ).index
        )

        ## Update number of connections
        #population['num_connections'] = population.connections.apply(len)
        # Get other agents available to connect
        available_to_connect_times = []
        start_time = time.time()
        available = available_to_connect(agent,population)
        end_time = time.time()
        available_to_connect_runtime = end_time - start_time

        # Randomly choose connection
        start_time = time.time()
        if len(available) > 0:
            connection = np.random.choice(available)
            # Make connection
            population.iloc[connection].connections.append(agent)
            population.iloc[agent].connections.append(connection)

            # Update number of connections
            population.iloc[[agent,connection],2] += 1
            #if _cnt < 10:
            while population.num_connections[agent] < num_connections:
                self._build_connection_list(agent,
                                       population,
                                       num_connections)
        end_time = time.time()
        randomly_chosen_runtime = end_time - start_time


        return population, available_to_connect_runtime, randomly_chosen_runtime

    def create_connections(self,verbose=False):
        num_connections = self.num_connections
        num_people = self.num_people
        population = pd.DataFrame(
            {
                'index': [i for i in range(num_people)],
                'connections': [[] for i in range(num_people)],
                'num_connections': [0 for i in range(num_people)]
            }
        )

        _update = num_people*0.1
        available_to_connect_runtimes = []
        randomly_chosen_runtimes = []
        for _per in population.index:
            if verbose:
                if _per % _update == 0:
                    print('{:.0f}% complete'.format(_per/num_people*100))
            population, available_to_connect_runtime, randomly_chosen_runtime = self._build_connection_list(_per,population,num_connections)
            available_to_connect_runtimes.append(available_to_connect_runtime)
            randomly_chosen_runtimes.append(randomly_chosen_runtime)

        self.population = population
        if verbose:
            mean_available_to_connect = mean(available_to_connect_runtimes)
            mean_randomly_chosen = mean(randomly_chosen_runtimes)
            iterations = population.index.size
            time = range(0, iterations)
            overall_runtime_available_to_connect = iterations * mean_available_to_connect
            overall_runtime_randomly_chosen = iterations * mean_randomly_chosen
            plt.scatter(time, available_to_connect_runtimes)
            plt.scatter(time, randomly_chosen_runtimes)
            plt.xlabel("iterations")
            plt.ylabel("execution time (s)")
            plt.legend(["available_to_connect", "randomly_chosen_connection"])
            plt.title(f'available_to_connect overall runtime: {overall_runtime_available_to_connect}\nrandomly_chosen overall runtime: {overall_runtime_randomly_chosen}')
            plt.show()

        return population

engine = ConnectionEngine(10000, 10)
engine.create_connections(verbose=True)
