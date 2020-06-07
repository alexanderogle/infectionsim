from population_engine import PopulationEngine
from simulation_day import SimulationDay
from settings import SimfectionSettings


class SimulationRun():
    def __init__(self, settings: dict = None) -> None:

        # Set settings
        self.settings = SimfectionSettings(settings)

        if self.settings.get_setting('previous_run') is None:
            self.population = PopulationEngine(self.settings)
            self.population.synthesize_population()
            self.days = None
        else:
            print('+ Restarting from previous run.')
            self.days = self.settings.get_setting('previous_run').days
            self.population = self.days[-1].population

    def run(self):
        num_days = self.settings.get_setting('num_days')
        population = self.population
        if self.days is None:
            self.days = []

        for today in range(num_days):
            # Get day number
            if len(self.days) == 0:
                day_number = today
            else:
                day_number = self.days[-1].day_number + 1
            print('\n+ Day {}'.format(day_number))
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
