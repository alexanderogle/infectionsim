import pandas as pd
import numpy as np
import time
import sys
import resource
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import pickle as pkl
import logging
import subprocess
import argparse
from connection_engine import ConnectionEngine
sys.setrecursionlimit(10**6)


class MemoryMonitor:
    def __init__(self):
        self.keep_measuring = True

    def measure_usage(self):
        max_usage = 0
        usage = []
        while self.keep_measuring:
            max_usage = max(
                max_usage,
                resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            )

            time.sleep(0.1)

        return max_usage


class ExperimentLogger:
    def __init__(self):
        pass

    def init(self):
        # Create logger ---
        logger = logging.getLogger('connection-engine')
        logger.setLevel(logging.DEBUG)
        # Create file handler
        os.makedirs('log/', exist_ok=True)
        log_path = 'log/experiment.log'
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # Create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # Add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        self.log = logger

        return logger


# class ConnectionEngine():
    #    def __init__(self, num_people=None, num_connections=None):
    #        self.num_people = num_people
    #        self.num_connections = num_connections
    #
    #    def _build_connection_list(self, agent, population, num_connections, cnt=None):
    #
    #        # Return IDs of people with connections less than num_connections
    #        available_to_connect = (
    #            lambda agent, population: population.drop(agent).query('num_connections < {}'
    #                                                                   .format(num_connections)
    #                                                                   ).index
    #        )
    #
    #        # Get other agents available to connect
    #        runtime = {}
    #        _start = time.time()
    #        available = available_to_connect(agent, population)
    #        runtime_available = time.time() - _start
    #        # Randomly choose connection
    #        _start = time.time()
    #        if len(available) > 0:
    #            connection = np.random.choice(available)
    #            # Make connection
    #            population.iloc[connection].connections.append(agent)
    #            population.iloc[agent].connections.append(connection)
    #
    #            # Update number of connections
    #            population.iloc[[agent, connection], 2] += 1
    #
    #            # If more connections are needed, iterate
    #            if cnt is None:
    #                cnt = 0
    #            # and (cnt < len(population)):
    #            while cnt < len(population) and population.num_connections[agent] < num_connections:
    #                cnt += 1
    #                self._build_connection_list(agent,
    #                                            population,
    #                                            num_connections,
    #                                            cnt=cnt)
    #        runtime_choose = time.time() - _start
    #        return population, runtime_available, runtime_choose
    #
    #    def create_connections(self, verbose=False):
    #        num_connections = self.num_connections
    #        num_people = self.num_people
    #        population = pd.DataFrame(
    #            {
    #                'index': [i for i in range(num_people)],
    #                'connections': [[] for i in range(num_people)],
    #                'num_connections': [0 for i in range(num_people)]
    #            }
    #        )
    #
    #        _update = num_people*0.1
    #        runtime = {
    #            'available': [],
    #            'choose': []
    #        }
    #        for _per in population.index:
    #            if verbose:
    #                if _per % _update == 0:
    #                    print('{:.0f}% complete'.format(_per/num_people*100))
    #            population, runtime_available, runtime_choose = self._build_connection_list(
    #                _per,
    #                population,
    #                num_connections)
    #            runtime['available'].append(runtime_available)
    #            runtime['choose'].append(runtime_choose)
    #
    #        self.population = population
    #        return population, runtime


class ConnectionsExperiment():
    def __init__(self,
                 num_people=None,
                 mean_connections=None,
                 connection_engine=None,
                 std=10,
                 size=100000,
                 num_runs=1):
        self.num_people = num_people
        self.mean_connections = mean_connections
        self.std = std
        self.size = size
        self.connection_engine = connection_engine
        self.num_runs = num_runs
        self.data = []
        self.logger = ExperimentLogger()
        self.logger.init()

    def single_experiment(self,
                          mean_connections=None,
                          num_people=None,
                          std=None,
                          size=None):

        if mean_connections is None:
            mean_connections = self.mean_connections
        if num_people is None:
            num_people = self.num_people
        if size is None:
            size = self.size
        if std is None:
            std = self.std

        _start = time.time()
        xns = self.connection_engine(
            num_people=num_people,
            mean_connections=mean_connections,
            experiment=True
        )
        population, runtime = xns.create_connections(
            std=std,
            size=size
        )
        output = {
            'num_people': num_people,
            'mean_connections': mean_connections,
            'max_size': sys.getsizeof(xns.population),
            'runtime': runtime
        }
        del xns
        output['runtime']['total'] = time.time() - _start
        self.data.append(output)

    def run(self):
        logger = self.logger
        # Set variables
        num_people = self.num_people
        mean_connections = self.mean_connections
        std = self.std
        size = self.size
        num_runs = self.num_runs

        # Allows handling of single values
        if isinstance(num_people, int):
            num_people = [num_people]
        if isinstance(mean_connections, int):
            mean_connections = [mean_connections]

        # Main
        logger.log.info('+ Starting Engine')
        for run in range(num_runs):
            for _np in num_people:
                for _nc in mean_connections:
                    logger.log.info(
                        'People: {} Mean Connections: {} STD: {} Size {}'
                        .format(_np, _nc, std, size))
                    try:
                        # TODO: Abstract out the Thread Pool Memory Monitor
                        with ThreadPoolExecutor() as executor:
                            monitor = MemoryMonitor()
                            mem_thread = executor.submit(monitor.measure_usage)
                            try:
                                fn_thread = executor.submit(
                                    self.single_experiment(
                                        num_people=_np,
                                        mean_connections=_nc,
                                        size=size,
                                        std=std)
                                )
                            finally:
                                monitor.keep_measuring = False
                                max_usage = mem_thread.result()

                            # Log Max Memory Usage
                            self.data[-1]['max_memory'] = max_usage

                    except:
                        # Bad run
                        output = {
                            'num_people': num_people,
                            'mean_connections': mean_connections,
                            'size': None,
                            'max_memory': None
                        }
                        self.data.append(output)
        logger.log.info('+ Stopping Engine')
        logger.log.info('+ Saving results.')
        self.save_results()
        logger.log.info('+ Closing Logger')

    def save_results(self):
        now = int(time.time())

        # Save results
        os.makedirs('results', exist_ok=True)
        with open('results/results_{}.pkl'.format(now), 'wb') as file_:
            pkl.dump(self.data, file_)

        # Push results to cloud
        cmd = (
            'aws s3 sync results  s3://infectionsim-experiment-data/connections/ --profile is --exact-timestamps'
        )
        _ = subprocess.run(cmd.split())

        # Rename log
        cmd = (
            'mv log/experiment.log log/experiment_{}.log'.format(now)
        )
        _ = subprocess.run(cmd.split())

        # Push log to cloud
        cmd = (
            'aws s3 sync log  s3://infectionsim-experiment-log/connections/ --profile is --exact-timestamps'
        )
        _ = subprocess.run(cmd.split())


if __name__ == '__main__':
    # Commandline arguments ---
    parser = argparse.ArgumentParser()
    parser.add_argument('-np', '--num_people', nargs='+', type=int,
                        help='single value or list for number of people',
                        default='100')
    parser.add_argument('-mc', '--mean_connections', nargs='+', type=int,
                        help='single value or list for nmean umber of connections',
                        default='10')
    parser.add_argument('-sd', '--std', type=int,
                        help='standard deviation for connection distribution',
                        default='10')
    parser.add_argument('-s', '--size', type=int,
                        help='sample size for connection distribution',
                        default='1000000')
    parser.add_argument('-nr', '--num_runs', type=int,
                        help=(
                            'number of times to iterate over (num_people,num_connections) pairs'
                        ),
                        default=3)
    args = parser.parse_args()

    num_people = args.num_people
    mean_connections = args.mean_connections
    num_runs = args.num_runs
    std = args.std
    size = args.size

    experiment = ConnectionsExperiment(
        num_people=num_people,
        mean_connections=mean_connections,
        connection_engine=ConnectionEngine,
        num_runs=num_runs,
        std=std,
        size=size)

    experiment.run()
