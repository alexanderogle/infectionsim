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

    def __init__(self, people={}):
        self.people = people

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
        count = 0
        for person in self.people:
            count += 1
        return count

    def get_population(self):
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

class Simulation():

    def __init__(self, population):
        self.population = population

    def seed_simulation(self, initial_infected, P, recovery_period, death_rate, seed_num):
        r.seed(seed_num)
        self.P = P
        self.recovery_period = recovery_period
        self.death_rate = death_rate
        infected = 0
        pop = self.population.get_population()
        for person in pop:
            if infected < initial_infected:
                self.population.infect_person(person, 0)
                infected += 1

    def update_infection(self, day):
        people = self.population.people
        for person_id in people:
            person = people[person_id]
            # Simulates probability of getting infection
            if r.random() < self.P and person.get_state() == "not infected":
                person.update_state("infected")
                person.is_infected(day)
            # Simulates probability of dying
            if r.random() < self.death_rate and person.get_state() == "infected":
                person.update_state("dead")
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
            self.update_infection(day)
            timeline[day] = self.get_snapshot()
            infection_timeline[day] = self.population.count_infected()
            not_infected_timeline[day] = self.population.count_states(not_infected_states)
            alive_timeline[day] = self.population.count_states(alive_states)

            completion_percent = (day/max_days)*100
            print("Percent Simulation Complete: " + str(completion_percent))
        return timeline, infection_timeline, not_infected_timeline, alive_timeline

    def __str__(self):
        string = str(self.population)
        return string
