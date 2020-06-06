import pandas as pd
from connection_engine import ConnectionEngine
from simfection_settings import SimFectionSettings
import numpy as np


class InteractionEngine():
    def __init__(self,
                 connections: pd.DataFrame = None,
                 population: pd.DataFrame = None,
                 settings: SimFectionSettings = None) -> None:
        self.connections = connections
        self.population = population
        self.pathogen = {
            key: settings.get_setting(key) for key in settings.get_setting('pathogen_keys')
        }

    def _make_interaction_pair(self, row):
        agent_a = row['agent_a']
        agent_b = row['agent_b']

        if agent_a < agent_b:
            return (row['agent_a'], row['agent_b'])
        else:
            return (row['agent_b'], row['agent_a'])

    def _get_unique_connections(self):
        connections = self.connections

        # Explode on connections
        # Drop num_connections column
        # Rename columns
        connections = (connections.query('num_connections > 0')
                       .explode(column='connections')
                       .drop(columns=['num_connections'])
                       .rename(columns={
                           'agent': 'agent_a',
                           'connections': 'agent_b'
                       })
                       )

        # Combine into interaction pair
        connections['interaction'] = (connections
                                      .apply(self._make_interaction_pair, axis=1)
                                      )

        # Drop unneeded columns
        # Drop duplicates
        connections = (connections
                       .filter(['interaction'])
                       .drop_duplicates()
                       )

        self.connections = connections

    def _get_agents(self, a, b):
        population = self.population

        records = population.query('agent in {}'.format([a, b])).to_dict()
        agent_a = {
            'agent': records['agent'][a],
            'state': records['state'][a]
        }
        agent_b = {
            'agent': records['agent'][b],
            'state': records['state'][b]
        }

        return agent_a, agent_b

    def _qualify_interaction(self, agent_a, agent_b):

        # Determine if agents have different states
        different_states = agent_a['state'] != agent_b['state']

        if different_states:

            # Determine if someone is infected
            someone_infected = agent_a['state'] == 'inf' or agent_b['state'] == 'inf'

            # Determine if someone is susceptible
            someone_susceptible = agent_a['state'] == 'sus' or agent_b['state'] == 'sus'

            if someone_infected and someone_susceptible:

                # Determine who is infected and who is susceptible
                if agent_a['state'] == 'inf':
                    infected = agent_a
                    susceptible = agent_b
                else:
                    infected = agent_b
                    susceptible = agent_a

                # Determine if infected is contagious
                days_infected = (
                    self.population
                    .query('agent == {}'.format(infected['agent']))
                    .days_infected
                    .values[0]
                )
                infected_is_contagious = days_infected < pathogen['contagious_period']

                if infected_is_contagious:

                    # Determine if susecptible is immune
                    immunity = (
                        self.population
                        .query('agent == {}'.format(susceptible['agent']))
                        .immunity
                        .values[0]
                    )
                    susecptible_is_immune = immunity > 0

                    if not susecptible_is_immune:
                        # Interaction qualified
                        return True, infected, susceptible
                    else:
                        # Interaction disqualified
                        return False, None, None
                else:
                    # Interaction disqualified
                    return False, None, None
            else:
                # Interaction disqualified
                return False, None, None
        else:
            # Interaction disqualified
            return False, None, None

    def _interact(self, a, b):
        pathogen = self.pathogen

        # Get agents
        agent_a, agent_b = self._get_agents(a, b)

        # Qualify interaction
        interact, infected, susceptible = self._qualify_interaction(agent_a, agent_b)

        # Interact
        draw = np.random.rand()  # Determines if pathogen spreads
        infect = draw < pathogen['infection_rate']
        if interact and infect:
            self.population.loc[susceptible['agent'], 'state'] = 'inf'
            self.population.loc[susceptible['agent'], 'infected_by'] = (
                int(infected['agent'])
            )

    def interact_all(self, verbose=False):
        self._get_unique_connections()
        connections = self.connections
        for a, b in connections.interaction.values:
            self._interact(a, b)

        if verbose:
            print(self.population.state.value_counts())


pathogen = {
    'infection_rate': 0.4,
    'recovery_rate': 0.1,
    'death_rate': 0.02,
    'spontaneous_rate': 0.0,
    'testing_accuracy': None,
    'immunity_period': 14,
    'contagious_period': 10,
    'incubation_period': 1,
}

if __name__ == '__main__':
    print("Hi, I'm the Interaction Engine. I'm not meant to be run directly.")
    print('To use me, please import InteractionEngine in your script.')
