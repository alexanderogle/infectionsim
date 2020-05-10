from connection_engine import ConnectionEngine
from interaction_engine import InteractionEngine, pathogen
from population_engine import PopulationEngine
from update_engine import UpdateEngine

import pandas as pd
import numpy as np
import sys


class SimulationDay():
    def __init__(
            self,
            day_number=None,
            population=None,
            num_people=None,
            mean_connections=None,
            pathogen=None,
            verbose=False,
            connections_std=10,
            connections_size=10**5):
        assert population is not None or num_people is not None, (
            'Both population and num_people are NoneType. At least one must be passed.'
        )
        self.day_number = day_number
        self.mean_connections = mean_connections
        self.pathogen = pathogen
        self.verbose = verbose
        self.connections_std = connections_std
        self.connections_size = connections_size
        if population is None:
            print('+ Dummy population generated.')
            self.population = PopulationEngine(num_people=num_people)
        else:
            print('+ Population loaded.')
            self.population = population

        self.starting_population = self.population._df.copy()

    def run(self):
        verbose = self.verbose
        if verbose:
            print('\n+ Starting PopulationEngine:')
            print(self.population._df.state.value_counts())
        if verbose:
            print('\n+ Running Connection Engine.')
        self.connection_engine = ConnectionEngine(
            population=self.population._df,
            mean_connections=self.mean_connections,
            std=self.connections_std,
            size=self.connections_size
        )
        self.connection_engine.create_connections()

        if verbose:
            print('\n+ Running Interaction Engine.')
        self.interaction_engine = InteractionEngine(
            connections=self.connection_engine.connections,
            pathogen=self.pathogen,
            population=self.connection_engine.population
        )
        self.interaction_engine.interact_all(verbose=verbose)

        if verbose:
            print('\n+ Running Update Engine.')
        self.update_engine = UpdateEngine(
            population=self.interaction_engine.population,
            pathogen=self.pathogen
        )
        self.update_engine.update_all(
            verbose=verbose
        )

        if verbose:
            print('\n+ Updating PopulationEngine.')
        self.population._df = self.update_engine.population
