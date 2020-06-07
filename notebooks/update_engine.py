from connection_engine import ConnectionEngine
from interaction_engine import InteractionEngine, pathogen
from population_engine import PopulationEngine
from settings import SimfectionSettings

import pandas as pd
import numpy as np
from logger import SimfectionLogger

simfection_logger = SimfectionLogger()
logger = simfection_logger.get_logger()


class UpdateEngine():
    def __init__(self,
                 population: pd.DataFrame = None,
                 settings: SimfectionSettings = None) -> None:
        logger.debug('+ Initializing update engine.')
        self.population = population
        self.verbose = settings.get_setting('verbose')
        logger.debug('- Reading pathogen.')
        self.pathogen = {
            key: settings.get_setting(key) for key in settings.get_setting('pathogen_keys')
        }

    def _update_state(self, agent):

        # Get probabilities
        rec = self.pathogen['recovery_rate']
        dead = self.pathogen['death_rate']
        inf = 1 - (rec + dead)

        # Choose new state
        new_state = np.random.choice(
            ['rec', 'dead', 'inf'],
            p=[rec, dead, inf]
        )

        return new_state

    def _update_states(self):
        population = self.population.copy()

        infected = population.query('state == "inf"').index
        population.loc[infected, 'state'] = population.loc[infected].apply(
            self._update_state,
            axis=1
        )

        self.population = population

    def _update_recovered(self):
        # Get index of those who just recovered
        recovered = self.population.query('state == "rec"').index

        # Reset their state, days_infected, and immunity
        self.population.loc[recovered, 'state'] = 'sus'
        self.population.loc[recovered, 'days_infected'] = 0
        self.population.loc[recovered, 'infected_by'] = None
        self.population.loc[recovered, 'immunity'] = self.pathogen['immunity_period']

    def _update_infected(self):
        # Index of those infected
        infected = self.population.query('state == "inf"').index
        # Add one day infected
        self.population.loc[infected, 'days_infected'] += 1
        # Clear any residual immunity from dummy populations
        self.population.loc[infected, 'immunity'] = 0

    def _update_immune(self):
        # Index of everyone with immunity, except the people who just recovered
        immune = (self.population
                  .query('days_infected > 1')
                  .query('immunity > 0')
                  .index)
        # Remove one day immunity
        self.population.loc[immune, 'immunity'] -= 1

    def update_all(self):
        verbose = self.verbose

        logger.debug('+ Running update engine.')
        logger.debug('- Updating states.')
        self._update_states()
        logger.debug('- Updating recovered.')
        self._update_recovered()
        logger.debug('- Updating infected.')
        self._update_infected()
        logger.debug('- Updating immnue.')
        self._update_immune()
        logger.debug('- Updates complete.')

        if verbose:
            print(self.population.state.value_counts())


if __name__ == '__main__':
    print("Hi, I'm the Connection Engine. I'm not meant to be run directly.")
    print('To use me, please import ConnectionEngine in your script.')
