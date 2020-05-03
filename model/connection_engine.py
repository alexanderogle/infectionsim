import pandas as pd
import numpy as np
import typing
import time
import sys
sys.setrecursionlimit(10**6)


class ConnectionEngine():
    def __init__(self,
                 num_people=None,
                 mean_connections=None,
                 population=None,
                 experiment=False):
        self.num_people = num_people
        self.mean_connections = mean_connections
        self.population = population
        self.experiment = experiment

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

    def _available_to_connect(self, agent, population):
        # Return IDs of people with connections less than num_connections
        # Only drop agent if it returns from query
        try:
            return population[
                population.num_connections < population.max_connections
            ].drop(agent).index
        except:
            return population[
                population.num_connections < population.max_connections
            ].index

    def _build_connection_list(self, agent, population):

        # Get other agents available to connect
        if self.experiment:
            runtime = {}
            _start = time.time()
        available = self._available_to_connect(agent, population)
        if self.experiment:
            runtime_available = time.time() - _start

        # Randomly choose connection
        if self.experiment:
            _start = time.time()
        if len(available) > 0:
            connection = np.random.choice(available)
            # Make connection
            population.iloc[connection].connections.append(agent)
            population.iloc[agent].connections.append(connection)

            # Update number of connections
            population.iloc[[agent, connection], 2] += 1

            # Iterate if necessary
            cont = (
                population.num_connections[agent] < population.max_connections[agent]
            )
            if cont:
                self._build_connection_list(agent, population)
        if self.experiment:
            runtime_choose = time.time() - _start
            return population, runtime_available, runtime_choose
        else:
            return population

    def create_connections(self, std=10, size=100000, verbose=False):
        num_people = self.num_people
        population = pd.DataFrame(
            {
                'agent': [i for i in range(num_people)],
                'connections': [[] for i in range(num_people)],
                'num_connections': [0 for i in range(num_people)],
                'max_connections': [
                    self._max_connections(std=std, size=size)
                    for i in range(num_people)
                ]
            }
        )

        _update = num_people*0.1
        if self.experiment:
            runtime = {
                'available': [],
                'choose': []
            }
        for _per in population.index:
            if verbose:
                if _per % _update == 0:
                    print('{:.0f}% complete'.format(_per/num_people*100))

            if self.experiment:
                population, runtime_available, runtime_choose = self._build_connection_list(
                    _per,
                    population,
                    num_connections)
                runtime['available'].append(runtime_available)
                runtime['choose'].append(runtime_choose)
            else:
                self._build_connection_list(_per, population)
        self.connections = population

        if self.experiment:
            return population, runtime

    def make_dummy(self, verbose=False):

        states = ['sus', 'inf', 'dead']

        try:
            population = pd.DataFrame(
                self.connections
                .agent
                .copy()
            )
        except:
            self.create_connections()
            population = pd.DataFrame(
                self.connections
                .agent
                .copy()
            )
        population['state'] = [np.random.choice(states) for i in range(len(population))]
        population['infected_by'] = [[] for i in range(len(population))]
        population['days_infected'] = [np.random.randint(14) for i in range(len(population))]
        population['immunity'] = 0

        susceptible = population.query('state == "sus"').index
        population.loc[susceptible, 'immunity'] = [
            np.random.randint(0, high=10)
            for i in range(len(susceptible))
        ]

        if verbose:
            print(population.state.value_counts())

        return population


if __name__ == '__main__':
    print("Hi, I'm the Connection Engine. I'm not meant to be run directly.")
    print('To use me, please import ConnectionEngine in your script.')
