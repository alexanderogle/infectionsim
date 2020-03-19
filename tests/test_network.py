import unittest as test
from infectionsim import data_structs as data

class TestNetworkMethods(test.TestCase):

    def setup(self):
        self.pop_id = "city"
        self.population_size = 1000
        self.pop = data.Population(self.pop_id, self.population_size)
        self.network = data.Network(self.pop)
        self.seed = 1
        self.connection_min = 1
        self.connection_max = 5


    # def test_init_random_network(self):
    #     self.setup()
    #     self.network.init_random_network(self.connection_min,
    #                                      self.connection_max, self.seed)
    #     # TODO(alexanderogle): Once import functionality is available, have a
    #     # test file be imported here as the answer, then assertEqual()
    #     self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
