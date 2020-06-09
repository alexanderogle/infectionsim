import sys
sys.path.append('../')
sys.path.append('../model')

from model.connection_engine_timing_test import ConnectionEngine
from model.population_engine import PopulationEngine
from model.settings import SimfectionSettings
import pandas as pd

class TimingTest:
    def __init__(self, runs=10, pop_size=1000, cpp=False):
        self.runs = runs
        self.pop_size = pop_size
        # Use default settings
        self.settings = SimfectionSettings(None)
        # Use cpp optimization
        self.settings.set_setting('cpp', cpp)

    def _gen_sizes(self):
        sizes = []
        for i in range(1, self.runs + 1):
            num = self.pop_size * i
            sizes.append(num)
        return sizes

    def _experiment(self):
        runtimes = []
        sizes = self._gen_sizes()
        for num in sizes:
        # Set the population heres
            self.settings.set_setting('num_people', num)
            popengine = PopulationEngine(self.settings)
            popengine.make_dummy()
            population = popengine._df
            connectengine = ConnectionEngine(population, self.settings)
            runtime = connectengine.create_connections(self.settings.get_setting('cpp'))
            runtimes.append(runtime)
        return runtimes

    def run_test(self):
        self._experiment()

