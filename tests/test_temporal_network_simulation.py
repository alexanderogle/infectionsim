import unittest as test
import time
from infectionsim import data_structs as data
from infectionsim import utilities as util

class TestTemporalSimulation(test.TestCase):

    def setup(self):
        # Setup a population of 10 people
        population_size = 10
        self.pop = data.Population("city", 10)

        self.max_days = 100
        self.temporal_network = data.TemporalNetwork(self.pop, self.max_days)
        conmin = 1
        conmax = 5
        seed_num = 1
        initial_infected = 1
        infection_probability = 0.03
        recovery_period = 14
        recovery_probability = 0.3
        death_probability = 0.01
        self.temporal_network.init_random_network(conmin, conmax, seed_num)
        self.sim = data.TemporalNetworkSimulation(self.temporal_network)
        self.sim.seed_simulation(initial_infected, infection_probability,
                            recovery_period, recovery_probability, death_probability, seed_num)
        self.timeline = self.sim.simulate(self.max_days, verbose=False)

    def test_initial_timeline_population_correct(self):
        # Only the first person in the population should be infected
        self.setup()
        population = self.timeline[0]["population"].get_population()
        for person_id in population:
            if person_id == 0:
                self.assertEqual(population[person_id].get_state(), "infected")
            else:
                self.assertEqual(population[person_id].get_state(), "susceptible")

    def test_simulation_write_out_read_in(self):
        self.setup()
        filepath = "./tests/test_simulation_write_out_read_in.simulation"
        # Write out the test simulation to a test file
        util.save_simulation_to_file(filepath, self.timeline)
        # Read in that test file
        timeline = util.read_simulation_to_timeline(filepath)

        # Need a better method of checking whether these timelines are the same
        # Currently will just check whether they have the same dimension.
        self.assertEqual(len(timeline), len(self.timeline))

    def test_time_simulation(self):
        start_time = time.time()
        self.setup()
        end_time = time.time()
        runtime = end_time - start_time
        print(runtime)
        self.assertGreater(5, runtime)


if __name__ == '__main__':
    unittest.main()
