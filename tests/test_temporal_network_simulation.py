import unittest as test
from infectionsim import data_structs as data

class TestTemporalSimulation(test.TestCase):

    def setup(self):
        # Setup a population of 10 people
        population_size = 10
        self.pop = data.Population("city", 10)

        self.max_days = 10
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
        self.timeline, self.infection_timeline, self.susceptible_timeline, self.recovered_timeline, self.dead_timeline = self.sim.simulate(self.max_days, verbose=False)

    def test_initial_timeline_population_correct(self):
        # Only the first person in the population should be infected
        self.setup()
        population = self.timeline[0]['population']
        for person_id in population:
            print("Person ID: " + str(person_id) + " : " + population[person_id].get_state())
            if person_id == 0:
                self.assertEquals(population[person_id].get_state(), "infected")
            else:
                self.assertEquals(population[person_id].get_state(), "susceptible")


if __name__ == '__main__':
    unittest.main()
