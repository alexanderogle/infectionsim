#!/usr/local/bin/python3
import random as r
# Data structs for use in modeling infections

class Person():

    def __init__(self, id, state):
        self.id = id
        self.state = state
        self.infection_date = "NaN"
        self.death_date = "NaN"

    def update_state(self, new_state):
        self.state = new_state

    def get_id(self):
        return self.id

    def get_state(self):
        return self.state

    def infect(self, day):
        self.update_state("infected")
        self.infection_date= day

    def is_infected(self, day):
        self.infection_date = day

    def is_dead(self, day):
        self.death_date = day

    def get_infection_date(self):
        return self.infection_date

    def __str__(self):
        return "Person object id: \"" + str(self.id) + "\" and state: \"" + str(self.state) + "\""


class Population():

    def __init__(self, id, people={}):
        self.people = people
        self.id = id

    def add_people(self, person):
        self.people[person.get_id()] = person

    def update_person_state(self, id, state):
        for person_id in self.people:
            if person_id == id:
                self.people[person_id].update_state(state)

    def infect_person(self, id, day):
        for person_id in self.people:
            if person_id == id:
                self.people[person_id].infect(day)

    def get_population_size(self):
        return len(self.people)

    def get_population(self):
        """ Returns the people dict of this population object.
        The people dict should have the following format:

            people = {person_id_int_1: Person_object_1,
                      .
                      .
                      .
                      person_id_int_n: Person_object_n
                      }
        """
        return self.people

    def count_infected(self):
        infected = 0
        for person_id in self.people:
            if self.people[person_id].get_state() == "infected":
                infected += 1
        return infected

    def count_states(self, states):
        count = 0
        for person_id in self.people:
            for state in states:
                if self.people[person_id].get_state() == state:
                    count += 1
        return count

    def __str__(self):
        string = str(self.people)
        return string


class Network():

    def __init__(self, population):
        self.population = population

    def init_random_network(self, connection_min, connection_max, seed_num):
        r.seed(seed_num)
        pop = self.population.get_population()
        pop_size =len(pop)
        self.network = {}

        completion_percent = 0
        for person_id in pop:
            num_connections = r.random() * connection_max
            connections_list = []
            for i in range(connection_min, connection_max):
                # Get a random person_id
                connection_id = r.randint(0, pop_size-1)
                # Ensure it isn't in the connections_list
                while(connection_id in connections_list):
                    connection_id = r.randint(0, pop_size-1)
                # Add the random person_id to the connections_list
                connections_list.append(connection_id)
                completion_percent = (person_id / pop_size) * 100
                print("Generating random network: " + str(completion_percent) + "%")
            # Add the connections list to the network dict
            self.network[person_id] = connections_list

    def get_network(self):
        return self.network

    def get_population(self):
        return self.population

    def __str__(self):
        string = str(self.network)
        return string


class Simulation():

    def __init__(self, population):
        self.population = population

    def seed_simulation(self, initial_infected, infection_probability,
                        recovery_period, death_probability, seed_num):
        r.seed(seed_num)
        self.infection_probability = infection_probability
        self.recovery_period = recovery_period
        self.death_probability = death_probability
        infected = 0
        pop = self.population.get_population()
        for person in pop:
            if infected < initial_infected:
                self.population.infect_person(person, 0)
                infected += 1

    def update(self, day):
        people = self.population.people
        for person_id in people:
            person = people[person_id]
            # Simulates probability of getting infection
            if r.random() < self.infection_probability and person.get_state() == "not infected":
                person.update_state("infected")
                person.is_infected(day)
            # Simulates probability of dying
            if r.random() < self.death_probability and person.get_state() == "infected":
                person.update_state("dead")
                person.is_dead(day)
            # Simulates period it takes to recover
            if person.get_state() == "infected" and day - person.get_infection_date() > self.recovery_period:
                person.update_state("recovered")


    def get_snapshot(self):
        return self.population

    def simulate(self, max_days):
        timeline = {0: self.get_snapshot()}
        infection_timeline = {0: self.population.count_infected()}
        not_infected_states = ["not infected", "recovered"]
        not_infected_timeline = {0: self.population.count_states(not_infected_states)}
        alive_states = ["not infected", "infected", "recovered"]
        alive_timeline = {0: self.population.count_states(alive_states)}

        completion_percent = 0
        for day in range(1, max_days):
            self.update(day)
            timeline[day] = self.get_snapshot()
            infection_timeline[day] = self.population.count_infected()
            not_infected_timeline[day] = self.population.count_states(not_infected_states)
            alive_timeline[day] = self.population.count_states(alive_states)

            completion_percent = (day/max_days)*100
            print("Percent Simulation Complete: " + str(completion_percent) + "%")
        return timeline, infection_timeline, not_infected_timeline, alive_timeline

    def __str__(self):
        string = str(self.population)
        return string

class NetworkSimulation(Simulation):
    """ Simulates propogation of an infection through a static network in a population.
    """
    def __init__(self, network):
        self.population = network.get_population()
        self.network = network

    def get_snapshot(self):
        return self.population, self.network

    def update(self, day):
        people = self.population.people
        for person_id in people:
            person = people[person_id]
            # Only use infected individuals' connections for updating infection status
            # Simulates probability of individuals connected to infected individual
            # getting infected.
            network = self.network.get_network()
            connections_list = network[person_id]
            if person.get_state() == "infected":
                for connection in connections_list:
                    connected_person = people[connection]
                    if r.random() < self.infection_probability and connected_person.get_state() == "not infected":
                        connected_person.update_state("infected")
                        connected_person.is_infected(day)
            # Simulates probability of dying
            if r.random() < self.death_probability and person.get_state() == "infected":
                person.update_state("dead")
                person.is_dead(day)
            # Simulates period it takes to recover
            if person.get_state() == "infected" and day - person.get_infection_date() > self.recovery_period:
                person.update_state("recovered")

    def simulate(self, max_days):
        initial_population, initial_network = self.get_snapshot()
        timeline = {0: {"population": initial_population, "network": initial_network}}
        infection_timeline = {0: self.population.count_infected()}
        not_infected_states = ["not infected", "recovered"]
        not_infected_timeline = {0: self.population.count_states(not_infected_states)}
        alive_states = ["not infected", "infected", "recovered"]
        alive_timeline = {0: self.population.count_states(alive_states)}

        completion_percent = 0
        for day in range(1, max_days):
            self.update(day)
            population, network = self.get_snapshot()
            timeline[day] = {"population": population, "network": network}
            infection_timeline[day] = population.count_infected()
            not_infected_timeline[day] = population.count_states(not_infected_states)
            alive_timeline[day] = population.count_states(alive_states)

            completion_percent = (day/max_days)*100
            print("Percent Simulation Complete: " + str(completion_percent) + "%")
        return timeline, infection_timeline, not_infected_timeline, alive_timeline
