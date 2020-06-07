from population_engine import PopulationEngine
from simulation_day import SimulationDay
from settings import SimfectionSettings
from logger import SimfectionLogger

simfection_logger = SimfectionLogger()
logger = simfection_logger.get_logger()


class SimulationRun():
    def __init__(self, settings: dict = None) -> None:
        logger.info('+ Initializing Simfection Run.')
        # Set settings)
        self.settings = SimfectionSettings(settings)

        if self.settings.get_setting('previous_run') is None:
            self.population = PopulationEngine(self.settings)
            self.population.synthesize_population()
            self.days = None
        else:
            logger.info('+ Restarting from previous run.')
            self.days = self.settings.get_setting('previous_run').days
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
                    population=population,
                    day_number=day_number,
                    settings=self.settings
                )
            else:
                yesterday = self.days[-1]
                day = SimulationDay(
                    population=yesterday.population,
                    day_number=day_number,
                    settings=self.settings
                )

            day.run()
            self.days.append(day)
        logger.info('- All days ran successfully.')
