from population_engine import PopulationEngine
from simulation_day import SimulationDay
from settings import SimfectionSettings
from logger import SimfectionLogger
from path import SimfectionPath
import time

simfection_logger = SimfectionLogger()
logger = simfection_logger.get_logger()


class SimulationRun():
    def __init__(self, settings: dict = None) -> None:
        logger.info('+ Initializing Simfection Run.')
        # Set settings)
        self.settings = SimfectionSettings(settings)
        self.path = SimfectionPath(base_path=self.settings.get_setting('base_path'))

        logger.info('+ Building directory structure at {}.'.format(self.path.base()))
        self.path.build_directory_structure()

        if self.settings.get_setting('previous_run') is None:
            self.population = PopulationEngine(self.settings)
            self.population.synthesize_population()
            self.days = None
            self.run_id = 'simfection_{}'.format(int(time.time()))
        else:  # Restarting
            logger.info('+ Restarting from previous run.')
            self.days = self.settings.get_setting('previous_run').days
            self.run_id = self.settings.get_setting('previous_run').run_id
            logger.info('- Loading population.')
            self.population = self.days[-1].population

    def run(self):
        num_days = self.settings.get_setting('num_days')
        population = self.population
        if self.days is None:
            self.days = []
        logger.info('+ Running {} days.'.format(num_days))
        for today in range(num_days):
            # Get day number
            if len(self.days) == 0:
                day_number = today
            else:
                day_number = self.days[-1].day_number + 1
            if today == 0:
                day = SimulationDay(
                    self.run_id,
                    population=population,
                    day_number=day_number,
                    settings=self.settings
                )
            else:
                yesterday = self.days[-1]
                day = SimulationDay(
                    self.run_id,
                    population=yesterday.population,
                    day_number=day_number,
                    settings=self.settings
                )

            day.run()
            self.days.append(day)
            self.path.save_day(day)
        logger.info('- All days ran successfully.')
        logger.info('+ Saving run.')
        self.path.save_run(self)


if __name__ == '__main__':
    sim = SimulationRun()
    sim.run()
