import os
import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt
from infectionsim import data_structs as data


class InfectionRun():
    '''An instance of a model run.'''

    def __init__(self, path_inputs='.pipeline_data/inputs.pkl'):
        with open(path_inputs, 'rb') as _file:
            self.inputs = pkl.load(_file)

        os.makedirs('data', exist_ok=True)

    def setup_population(self):
        self.pop = data.Population(
            self.inputs['population_name'],
            self.inputs['population']
        )

    def setup_network(self):
        if not self.inputs['read_in_data']:
            print('Initializing new network.')
            self.network = data.Network(self.pop)
            self.network.init_random_network(connection_min=self.inputs['connection_min'],
                                             connection_max=self.inputs['connection_max'],
                                             seed_num=self.inputs['seed_num'])
        if self.inputs['read_in_data']:
            self.network = data.Network(self.pop)
            self.network.from_csv(self.inputs['path_in'])
            print("Network created from data located at: " + self.inputs['path_in'])

        if self.inputs['write_out_data']:
            self.network.to_csv(self.inputs['path_out'])
            print('Network written to: {}'.format(self.inputs['path_out']))

    def run_model(self):
        self.initial_infected = int(self.inputs['population'] * 0.005)
        if self.initial_infected < 1:
            self.initial_infected = 1
        states = ["susceptible", "infected", "recovered", "dead"]
        self.sim = data.NetworkSimulation(self.network)
        print("Seeding simulation...")
        self.sim.seed_simulation(
            self.initial_infected,
            self.inputs['infection_probability'],
            self.inputs['recovery_period'],
            self.inputs['recovery_probability'],
            self.inputs['death_probability'],
            self.inputs['seed_num'])
        print("Beginning simulation...")
        self.timeline, self.infection_timeline, self.susceptible_timeline, self.recovered_timeline, self.dead_timeline = self.sim.simulate(
            self.inputs['max_days'])

        if self.inputs['plot_results']:
            self.infected = pd.DataFrame.from_dict(
                self.infection_timeline,
                orient="index",
                columns=["number infected"])
            self.susceptible = pd.DataFrame.from_dict(
                self.susceptible_timeline,
                orient="index",
                columns=["number susceptible"])
            self.recovered = pd.DataFrame.from_dict(
                self.recovered_timeline,
                orient="index",
                columns=["number alive"])
            self.dead = pd.DataFrame.from_dict(
                self.dead_timeline,
                orient="index",
                columns=["number dead"])

            plt.plot(self.infected)
            plt.plot(self.susceptible)
            plt.plot(self.recovered)
            plt.plot(self.dead)
            plt.xlabel("timeline (days from t = 0)")
            plt.ylabel("person count")
            plt.legend(["infected", "susceptible", "recovered", "dead"])
            plt.show()


if __name__ == '__main__':
    run = InfectionRun()
    run.setup_population()
    run.setup_network()
    run.run_model()
    with open('.pipeline_data/done.pkl', 'wb') as file_:
        pkl.dump('Done.', file_)
