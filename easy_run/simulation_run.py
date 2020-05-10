from population_engine import PopulationEngine
from simulation_day import SimulationDay


class SimulationRun():
    def __init__(
        self,
        num_people=None,
        mean_connections=None,
        num_days=None,
        initial_states=None,
        pathogen=None,
        previous_run=None,
        verbose=False,
        connections_std=10,
        connections_size=10**5
    ):
        assert num_people is not None or previous_run is not None, (
            'Either num_people or previous_run must be provided.'
        )
        if previous_run is None:
            assert initial_states is not None, (
                'To synthesize new population, initial_states must be passed.'
            )
            self.num_people = num_people
            self.initial_states = initial_states
            self.population = PopulationEngine(
                num_people=num_people,
                initial_states=initial_states,
                verbose=verbose
            )
            self.population.synthesize_population()
            self.days = None
            self.connections_std = connections_std
            self.connections_size = connections_size
        else:
            print('+ Restarting from previous run.')
            self.days = previous_run.days
            self.population = self.days[-1].population

        assert mean_connections is not None, (
            'You must prvide a value for mean_connects.'
        )

        self.mean_connections = mean_connections
        self.num_days = num_days
        self.pathogen = pathogen
        self.verbose = verbose

    def run(self):
        num_days = self.num_days
        population = self.population
        mean_connections = self.mean_connections
        pathogen = self.pathogen
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
                    mean_connections=mean_connections,
                    pathogen=pathogen,
                    day_number=day_number,
                    verbose=self.verbose,
                    connections_size=self.connections_size,
                    connections_std=self.connections_std
                )
            else:
                yesterday = self.days[-1]
                day = SimulationDay(
                    population=yesterday.population,
                    pathogen=pathogen,
                    mean_connections=mean_connections,
                    day_number=day_number,
                    verbose=self.verbose
                )

            day.run()
            self.days.append(day)
