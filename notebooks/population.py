import pandas as pd
import numpy as np


class Population:
    def __init__(self, num_people=None, _df=None):
        if num_people is not None:
            self.num_people = num_people
            self.make_dummy()
        else:
            self._df = _df

    def make_dummy(self, verbose=False):
        states = ['sus', 'inf', 'dead']

        population = pd.DataFrame(
            {
                'agent': [i for i in range(self.num_people)]
            }
        )
        # Give initial values
        population['state'] = [np.random.choice(states) for i in range(len(population))]
        population['infected_by'] = [[] for i in range(len(population))]
        population['days_infected'] = 0
        population['immunity'] = 0

        # Give susceptible people random immunity
        susceptible = population.query('state == "sus"').index
        population.loc[susceptible, 'immunity'] = [
            np.random.randint(0, high=10)
            for i in range(len(susceptible))
        ]

        # Give infected people random infected_by and days_infected
        infected = population.query('state == "inf"').index
        population.loc[infected, 'days_infected'] = [
            np.random.randint(1, high=10)
            for i in range(len(infected))
        ]
        population.loc[infected, 'infected_by'].apply(
            lambda x: x.append(
                np.random.choice(infected)
            )
        )

        # Give dead people random days_infected and infected_by
        infected = population.query('state == "dead"').index
        population.loc[infected, 'days_infected'] = [
            np.random.randint(0, high=10)
            for i in range(len(infected))
        ]
        population.loc[infected, 'infected_by'].apply(
            lambda x: x.append(
                np.random.choice(infected)
            )
        )

        if verbose:
            print(population.state.value_counts())

        self._df = population
