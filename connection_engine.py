import pandas as pd
import numpy as np
import typing
import time
import sys
sys.setrecursionlimit(10**6)


class ConnectionEngine():
    def __init__(self, num_people=None, num_connections=None):
        self.num_people = num_people
        self.num_connections = num_connections

    def _build_connection_list(self, agent, population, num_connections):
        # Break counter
        # if _cnt == 0:
        #    _cnt += 1
        # Return IDs of people with connections less than num_connections
        available_to_connect = (
            lambda agent, population: population.drop(agent).query('num_connections < {}'
                                                                   .format(num_connections)
                                                                   ).index
        )

        # Update number of connections
        #population['num_connections'] = population.connections.apply(len)
        # Get other agents available to connect
        available = available_to_connect(agent, population)
        # Randomly choose connection
        if len(available) > 0:
            connection = np.random.choice(available)
            # Make connection
            population.iloc[connection].connections.append(agent)
            population.iloc[agent].connections.append(connection)

            # Update number of connections
            population.iloc[[agent, connection], 2] += 1
            # if _cnt < 10:
            while population.num_connections[agent] < num_connections:
                self._build_connection_list(agent,
                                            population,
                                            num_connections)

        return population

    def create_connections(self, verbose=False):
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
        for _per in population.index:
            if verbose:
                if _per % _update == 0:
                    print('{:.0f}% complete'.format(_per/num_people*100))
            self._build_connection_list(_per, population, num_connections)

        self.population = population

        return population


if __name__ == '__main__':
    print("Hi")
