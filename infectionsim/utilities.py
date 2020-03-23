#!/usr/local/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import sys
import time
from infectionsim.protobuf import simulation_pb2

# File that holds utility functions to be used in the code base

def plot_timeline(timeline):
    infection_timeline = {}
    susceptible_timeline = {}
    recovered_timeline = {}
    dead_timeline = {}
    for day in timeline:
        infection_timeline[day] = timeline[day]["population"].count_infected()
        susceptible_timeline[day] = timeline[day]["population"].count_states(["susceptible"])
        recovered_timeline[day] = timeline[day]["population"].count_states(["recovered"])
        dead_timeline[day] = timeline[day]["population"].count_states(["dead"])

    infected = pd.DataFrame.from_dict(infection_timeline, orient="index", columns=["number infected"])
    susceptible = pd.DataFrame.from_dict(susceptible_timeline, orient="index", columns=["number susceptible"])
    recovered = pd.DataFrame.from_dict(recovered_timeline, orient="index", columns=["number alive"])
    dead = pd.DataFrame.from_dict(dead_timeline, orient="index", columns=["number dead"])

    plt.plot(infected)
    plt.plot(susceptible)
    plt.plot(recovered)
    plt.plot(dead)
    plt.xlabel("timeline (days from t = 0)")
    plt.ylabel("person count")
    plt.legend(["infected", "susceptible", "recovered", "dead"])
    plt.show()

def write_out_person(person_proto, id, state, infection_date, death_date):
    person_proto.id = str(id)
    person_proto.state = str(state)
    person_proto.infection_date = str(infection_date)
    person_proto.death_date = str(death_date)

def write_out_population(simulation_proto, id, population):
    population_proto = simulation_proto.population.add()
    population_proto.id = id
    for person_id in population:
        person_proto = population_proto.people.add()
        person = population[person_id]
        id = person.get_id()
        state = person.get_state()
        infection_date = person.get_infection_date()
        death_date = person.get_death_date()
        write_out_person(person_proto, id, state, infection_date, death_date)

def write_out_connection_list(connection_list_proto, id, connections):
    connection_list_proto.id = id
    for connection in connections:
        connections_proto = connection_list_proto.connection.add()
        connections_proto = connection

def save_simulation_to_file(filepath, timeline):
    print("Writing out to filepath: " + filepath)

    population = timeline[0]["population"]
    network = timeline[0]["network"]

    simulation_proto = simulation_pb2.SimulationTimeline()
    simulation_proto.id = str(time.time())

    # Write out the populations
    pop_id = "cityville"
    for day in timeline:
        population = timeline[day]["population"].get_population()
        write_out_population(simulation_proto, pop_id, population)

    # Write the new person out to disk
    f = open(filepath, "wb")
    f.write(simulation_proto.SerializeToString())
    f.close
