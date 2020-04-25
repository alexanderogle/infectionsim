import pandas as pd
import numpy as np
import typing
import time
import sys
sys.setrecursionlimit(10**6)


class ConnectionEngine():
    def __init__(self, num_people=None, mean_connections=None, population=None):
        self.num_people = num_people
        self.mean_connections = mean_connections
        self.population = population

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
        available = self._available_to_connect(agent, population)

        # Randomly choose connection
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

        return population

    def create_connections(self, std=10, size=100000, verbose=False):
        num_people = self.num_people
        if self.population is None:
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
            self.population = population
        else:
            raise TypeError('Bad population given. Pass nothing for now. DEBUG THIS')

        _update = num_people*0.1
        for _per in population.index:
            if verbose:
                if _per % _update == 0:
                    print('{:.0f}% complete'.format(_per/num_people*100))

            self._build_connection_list(_per, population)
        self.connections = population

    def make_dummy(self, verbose=False):

        states = ['sus', 'inf', 'rec', 'imm', 'dead']

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
        population['infected_by'] = None
        population['days_infected'] = [np.random.randint(14) for i in range(len(population))]

        if verbose:
            print(population.state.value_counts())

        return population


if __name__ == '__main__':
    print("Hi, I'm the Connection Engine. I'm not meant to be run directly.")
    print('To use me, please import ConnectionEngine in your script.')
