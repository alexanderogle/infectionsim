import unittest as test
from infectionsim import data_structs as data

class TestPersonMethods(test.TestCase):

    def setup(self):
        self.id = 1
        self.state = "state"
        self.person = data.Person(self.id, self.state)

    def test_person_creation(self):
        self.setup()
        self.assertEqual(self.person.get_id(), self.id)
        self.assertEqual(self.person.get_state(), self.state)
        self.assertEqual(self.person.get_infection_date(), "")
        self.assertEqual(self.person.get_death_date(), "")

    def test_person_change_state(self):
        self.setup()
        state = "infection"
        self.person.update_state(state)
        self.assertEqual(self.person.get_state(), state)

if __name__ == '__main__':
    unittest.main()
