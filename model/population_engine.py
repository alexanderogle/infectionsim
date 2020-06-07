import pandas as pd
import numpy as np
from settings import SimfectionSettings


class PopulationEngine:
    def __init__(self, settings: SimfectionSettings, _df: pd.DataFrame = None) -> None:
        if _df is not None:
            self._df = _df
        else:
            self.num_people = settings.get_setting('num_people')
            self.initial_states = settings.get_setting('initial_states')
            self._df = pd.DataFrame()
            self.verbose = settings.get_setting('verbose')

    def _synthesize_states(self):
        initial_states = self.initial_states
        num_people = self.num_people

        # Get total weight
        total_weights = sum([v for k, v in initial_states.items()])
        # Validate given weights
        if total_weights < 1:
            initial_states['sus'] = 1 - total_weights
        elif total_weights > 1:
            raise ValueError(
                '''
                Total weights for initial state cannot exceed 1.
                Total Weight: {}
                Weights: {}
                '''.format(total_weights, initial_states)
            )
        # Synthesize states
        states = np.random.choice(
            [k for k in initial_states.keys()],
            size=num_people,
            p=[v for v in initial_states.values()]
        )

        return states

    def synthesize_population(self):
        print('+ Synthesizing population.')
        num_people = self.num_people
        initial_states = self.initial_states

        population = pd.DataFrame(
            {
                'agent': range(num_people),
                'state': ['sus']*num_people,
                'infected_by': [None]*num_people,
                'days_infected': [0]*num_people,
                'immunity': [0]*num_people
            }
        )

        inf = population.sample(
            n=int(num_people*initial_states['inf'])
        ).agent
        population.loc[inf, 'state'] = 'inf'

        self._df = population

    def make_dummy(self):
        verbose = self.verbose

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
