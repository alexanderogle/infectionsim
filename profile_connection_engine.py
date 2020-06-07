import pandas as pd
import numpy as np
import time
import sys
import resource
import matplotlib.pyplot as plt
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tests import anchor
sys.setrecursionlimit(10**6)


class ConnectionEngine():
    def __init__(self,num_people=None,num_connections=None):
        self.num_people = num_people
        self.num_connections = num_connections

    def _build_connection_list(self,agent,population,num_connections, recursion_num):
        recursion_num = recursion_num + 1
        # Return IDs of people with connections less than num_connections
        available_to_connect = (
            lambda agent,population: population.drop(agent).query('num_connections < {}'
                                                                     .format(num_connections)
                                                                    ).index
        )

        ## Update number of connections
        # Get other agents available to connect
        available = available_to_connect(agent,population)


        # Randomly choose connection
        if len(available) > 0:

            connection = np.random.choice(available)

            # Make connection
            population.iloc[connection].connections.append(agent)
            population.iloc[agent].connections.append(connection)


            # Update number of connections
            population.iloc[[agent,connection],2] += 1
            anchor = 'connection_' + str(recursion_num)
            anchor_tracker.create_anchor(anchor)
            while population.num_connections[agent] < num_connections:
                self.return_data = self._build_connection_list(agent,
                                       population,
                                       num_connections,
                                       recursion_num)
            anchor_tracker.end_anchor(anchor)

        if recursion_num == 1:
            return population
        else:
            return population, recursion_num

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
        times = []
        for count, _per in enumerate(population.index):
            if verbose:
                if _per % _update == 0:
                    print('{:.0f}% complete'.format(_per/num_people*100))
            population = self._build_connection_list(_per,population,num_connections,0)

        self.population = population

        return population

def run_experiment(connections):
    engine = ConnectionEngine(1000, connections)
    engine.create_connections(verbose=True)

    anchor_list = anchor_tracker.get_anchors()
    times = []
    for a in anchor_list:
        t = a.timing()
        times.append(t)
    df = pd.DataFrame(times)
    filename = './test_output_' + str(connections) + '.csv'
    df.to_csv(filename)
    # Explicitly delete the DataFrame
    del df

# MAIN FUNCTION
# Run a series of experiments
experiments = [10]

for experiment in experiments:
    anchor_tracker = anchor.AnchorTracker()
    print("Running experiment: " + str(experiment))
    run_experiment(experiment)
    print("Experiment " + str(experiment) + " concluded.")
