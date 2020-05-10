import pandas as pd
import numpy as np
import typing
import time
import sys
sys.setrecursionlimit(10**6)


class ConnectionEngine():
    def __init__(self,
                 population=None,
                 mean_connections=None,
                 experiment=False,
                 verbose=False,
                 std=10,
                 size=10**5):

        self.population = population
        self.mean_connections = mean_connections
        self.experiment = experiment
        self.verbose = verbose
        self.std = std
        self.size = size

    def _max_connections(self, std=None, size=None):
        distribution = np.round(
            np.random.normal(
                loc=self.mean_connections,  # Mean
                scale=std,  # Standard Deviation
                size=size  # sample size
            )
        )

        choice = int(np.random.choice(distribution))
        while choice < 0:
            choice = int(np.random.choice(distribution))

        return choice

    def _available_to_connect(self, agent, connections):
        # Return IDs of people with connections less than num_connections
        # Only drop agent if it returns from query
        try:
            return connections[
                connections.num_connections < connections.max_connections
            ].drop(agent).index
        except:
            return connections[
                connections.num_connections < connections.max_connections
            ].index

    def _build_connection_list(self, agent, connections):

        # Get other agents available to connect
        if self.experiment:
            runtime = {}
            _start = time.time()
        available = self._available_to_connect(agent, connections)
        if self.experiment:
            runtime_available = time.time() - _start

        # Randomly choose connection
        if self.experiment:
            _start = time.time()
        if len(available) > 0:
            connection = np.random.choice(available)
            # Make connection
            connections.iloc[connection].connections.append(agent)
            connections.iloc[agent].connections.append(connection)

            # Update number of connections
            connections.iloc[[agent, connection], 2] += 1

            # Iterate if necessary
            cont = (
                connections.num_connections[agent] < connections.max_connections[agent]
            )
            if cont:
                self._build_connection_list(agent, connections)
        if self.experiment:
            runtime_choose = time.time() - _start
            return connections, runtime_available, runtime_choose
        else:
            return connections

    def create_connections(self):
        std = self.std
        size = self.size
        verbose = self.verbose

        not_dead = self.population.query('state != "dead"').index
        connections = pd.DataFrame(
            {
                'agent': [i for i in not_dead],
                'connections': [[] for i in not_dead],
                'num_connections': [0 for i in not_dead],
                'max_connections': [
                    self._max_connections(std=std, size=size)
                    for i in not_dead
                ]
            }
        )

        _update = len(not_dead)*0.1
        if self.experiment:
            runtime = {
                'available': [],
                'choose': []
            }
        for _per in connections.index:
            if verbose:
                if _per % _update == 0:
                    print('{:.0f}% complete'.format(_per/len(not_dead)*100))

            if self.experiment:
                connections, runtime_available, runtime_choose = self._build_connection_list(
                    _per,
                    connections,
                    num_connections)
                runtime['available'].append(runtime_available)
                runtime['choose'].append(runtime_choose)
            else:
                self._build_connection_list(_per, connections)
        self.connections = connections

        if self.experiment:
            return connections, runtime


if __name__ == '__main__':
    print("Hi, I'm the Connection Engine. I'm not meant to be run directly.")
    print('To use me, please import ConnectionEngine in your script.')
