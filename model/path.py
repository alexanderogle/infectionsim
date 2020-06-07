import os
import shutil
import pickle
from simulation_day import SimulationDay
from logger import SimfectionLogger

simfection_logger = SimfectionLogger()
logger = simfection_logger.get_logger()


class SimfectionPath:
    def __init__(self, base_path='simfection'):
        self.base_path = base_path

    # Base directory
    def base(self):
        return self.base_path

    def log(self):
        return os.path.join(self.base(), 'log')

    def output(self):
        return os.path.join(self.base(), 'output')

    def build_directory_structure(self):
        for _dir in [self.base, self.log, self.output]:
            os.makedirs(_dir(), exist_ok=True)

    # Log directory
    def log_file(self, source=False):
        if source:
            return 'simfection.log'
        return os.path.join(self.log(), 'simfection.log')

    def move_log(self):
        source = self.log_file(source=True)
        destination = self.log_file()
        try:
            logger.info('Moving log from {} to {}.'.format(source, destination))
            shutil.move(
                source,
                destination
            )
        except FileNotFoundError:
            logger.exception('+ No log file found at {}.'.format(source))

    def day(self, day):
        try:
            return os.path.join(self.output(), 'day_{}.pickle'.format(day.day_number))
        except AttributeError:  # For loading when passing in an int
            return os.path.join(self.output(), 'day_{}.pickle'.format(day))

    def save_day(self, day: SimulationDay):
        day_number = day.day_number
        destination = self.day(day)
        logger.info('+ Saving day {} to {}.'.format(day_number, destination))
        with open(destination, 'wb') as file_:
            pickle.dump(day, file_)

    def load_day(self, day_number: int):
        source = self.day(day_number)
        try:
            logger.info('+ Loading day {} from {}.'.format(day_number, source))
            with open(self.day(day_number), 'rb') as _file:
                return pickle.load(_file)
        except FileNotFoundError:
            logger.exception('+ Unable to load day {} from {}.'.format(day_number, source))
