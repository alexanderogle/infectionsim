from connection_engine import ConnectionEngine
from interaction_engine import InteractionEngine, pathogen
from population_engine import PopulationEngine
from update_engine import UpdateEngine
from simfection_settings import SimFectionSettings

import pandas as pd
import numpy as np
import sys


class SimulationDay():
    def __init__(
            self,
            day_number: int = None,
            population: PopulationEngine = None,
            settings: SimFectionSettings = None) -> None:
        assert population is not None or settings is not None, (
            'Both population and settings are NoneType. At least one must be passed.'
        )
        self.day_number = day_number
        self.settings = settings
        if population is None:
            print('+ Dummy population generated.')
            self.population = PopulationEngine(settings)
            self.population.make_dummy()

        else:
            print('+ Population loaded.')
            self.population = population

        self.starting_population = self.population._df.copy()

    def run(self):
        verbose = self.settings.get_setting('verbose')
        if verbose:
            print('\n+ Starting PopulationEngine:')
            print(self.population._df.state.value_counts())
        if verbose:
            print('\n+ Running Connection Engine.')
        self.connection_engine = ConnectionEngine(
            population=self.population._df,
            settings=self.settings
        )
        self.connection_engine.create_connections()

        if verbose:
            print('\n+ Running Interaction Engine.')
        self.interaction_engine = InteractionEngine(
            connections=self.connection_engine.connections,
            settings=self.settings,
            population=self.connection_engine.population
        )
        self.interaction_engine.interact_all(verbose=verbose)

        if verbose:
            print('\n+ Running Update Engine.')
        self.update_engine = UpdateEngine(
            population=self.interaction_engine.population,
            settings=self.settings
        )
        self.update_engine.update_all(
            verbose=verbose
        )

        if verbose:
            print('\n+ Updating PopulationEngine.')
        self.population._df = self.update_engine.population
