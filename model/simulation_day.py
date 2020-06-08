from connection_engine import ConnectionEngine
from interaction_engine import InteractionEngine, pathogen
from population_engine import PopulationEngine
from update_engine import UpdateEngine
from settings import SimfectionSettings

import pandas as pd
import numpy as np
import time
import logging
from logger import SimfectionLogger
import anchor

simfection_logger = SimfectionLogger(name=__name__)
logger = simfection_logger.get_logger()
anchor_tracker = anchor.AnchorTracker()

class SimulationDay():
    def __init__(
            self,
            run_id,
            day_number: int = None,
            population: PopulationEngine = None,
            settings: SimfectionSettings = None) -> None:
        assert population is not None or settings is not None, (
            'Both population and settings are NoneType. At least one must be passed.'
        )
        logger.info('+ Simulating day {}.'.format(day_number))
        self.day_number = day_number
        self.settings = settings
        self.run_id = run_id
        if population is None:
            logger.info('+ Dummy population generated.')
            self.population = PopulationEngine(settings)
            self.population.make_dummy()

        else:
            logger.debug('+ Population loaded.')
            self.population = population

        logger.debug('+ Saving starting population.')
        self.starting_population = self.population._df.copy()

    def run(self):
        anchor_tracker.create_anchor('run')
        verbose = self.settings.get_setting('verbose')
        self.connection_engine = ConnectionEngine(
            population=self.population._df,
            settings=self.settings
        )
        anchor_tracker.create_anchor('connection')
        cpp = self.settings.get_setting('cpp')
        self.connection_engine.create_connections(cpp)
        anchor_tracker.end_anchor('connection')
        connection_runtime = anchor_tracker.timing('connection')
        logging.debug(f'- Connections made in {connection_runtime} seconds')

        self.interaction_engine = InteractionEngine(
            connections=self.connection_engine.connections,
            settings=self.settings,
            population=self.connection_engine.population
        )
        anchor_tracker.create_anchor('interact')
        self.interaction_engine.interact_all()
        anchor_tracker.end_anchor('interact')
        interact_runtime = anchor_tracker.timing('interact')
        logging.debug(f'- Interactions made in {interact_runtime} seconds.')

        self.update_engine = UpdateEngine(
            population=self.interaction_engine.population,
            settings=self.settings
        )
        anchor_tracker.create_anchor('update')
        self.update_engine.update_all()
        anchor_tracker.end_anchor('update')
        update_runtime = anchor_tracker.timing('update')
        logging.debug(f'- Updates made in {update_runtime} seconds.')

        self.population._df = self.update_engine.population

        anchor_tracker.end_anchor('run')
        run_runtime = anchor_tracker.timing('run')
        logger.debug('- Day ran successfully.')
        logger.debug(f'- Day simulated in {run_runtime} seconds.')
        logger.debug('- Saving final population.')
        self.final_population = self.population._df
