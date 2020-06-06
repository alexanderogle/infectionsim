"""Creates a network of hand-shake connections as part of model run.

The ConnectionEngine takes a Population object and an average number of connections
and randomly creates a hand-shake network of interactions within the population.

  Typical usage example:

  from population_engine import PopulationEngine
  from connection_engine import ConnectionEngine

  # Set params
  initial_states = {'inf':0.2}
  num_people = 100
  mean_connections = 10

  # Synthesize population
  population = PopulationEngine(
    num_people=num_people,
    initial_states=initial_states
  )
  population.synthesize_population()

  # Create connections
  connection_engine = ConnectionEngine(
    population=population._df,
    mean_connections=mean_connections
  )
  connection_engine.create_connections()
"""
import typing
import time
import sys
import pandas as pd
import numpy as np

sys.setrecursionlimit(10**6)


class ConnectionEngine():
    """Creates a connections list for each agent in a population following
    the hand-shake protocol.

    Longer class information....
    Longer class information....

    Attributes:
        population: A PopulationEngine instance.
        mean_connections: An integer average number of connections for each
            agent.
        experiment: A boolean indicating whether or not this instance is being
            used for a timing experiment.
        verbose: A boolean indicating whether or not print debugging
            information to the console.
        std: An integer standard deviation for the distribution from which
            each agent draws to determine the maximum number of connections
            they will have.
        size: An interger number of samples to take from the normal distribution
            from which each agent draws to determine the maximum number of
            connections.
        connections: Initialized as a Nonetype. This will be set in the
            create_connections method.
    """

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
        self.connections = None

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

    @staticmethod
    def _available_to_connect(agent, connections):
        # Return IDs of people with connections less than num_connections
        # Only drop agent if it returns from query
        try:
            return connections[
                connections.num_connections < connections.max_connections
            ].drop(agent).index
        except KeyError:
            return connections[
                connections.num_connections < connections.max_connections
            ].index

    def _build_connection_list(self, agent, connections):

        # Get other agents available to connect
        if self.experiment:
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
        return connections

    def create_connections(self):
        """Creates connection list for each agent.

        A connections DataFrame is created and returned using the agents in the
        PopulationEngine instance self attribute. This method and return object
        spec are required inputs for the next step,which is the interaction
        engine.

        Args:
            ALEX: I don't know if I should put arguments here, because the
            method uses self attributes. Thoughts?

        Returns:
            A pandas DataFrame representing the interaction network for a
            simulation day. Each row is a record that is indexed to an agent in
            the  PopulationEngine instance. A description of the columns
            folowed by an example record are given below.

            DataFrame Columns:
                'agent': unqiue agent ID indexed to the PopulationEngine
                'connections': list of agent IDs with whom the agent had
                    an interaction
                'num_connections': length of list in connections columns
                'max_connections': maximum number of connections the agent can
                    have as randomly drawn

            Example:
                agent connections  num_connections  max_connections
                0         [1]                1                1
                1      [0, 3]                2                1
                2         [5]                1                1
                3      [1, 4]                2                1
                4      [3, 8]                2                1


        Raises:
            #TODO
        """
        std = self.std
        size = self.size
        verbose = self.verbose

        not_dead = self.population.query('state != "dead"').index
        connections = pd.DataFrame(
            {
                'agent': list(range(len(not_dead))),
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
                    connections
                )
                runtime['available'].append(runtime_available)
                runtime['choose'].append(runtime_choose)
            else:
                self._build_connection_list(_per, connections)
        self.connections = connections

        if self.experiment:
            return connections, runtime
        return None


if __name__ == '__main__':
    print("Hi, I'm the Connection Engine. I'm not meant to be run directly.")
    print('To use me, please import ConnectionEngine in your script.')
