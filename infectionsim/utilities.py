#!/usr/local/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import sys
import time
from infectionsim.protobuf import simulation_pb2
from infectionsim import data_structs as data

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

def write_out_population(population_proto, id, population):
    population_proto.id = id
    for person_id in population:
        person_proto = population_proto.people.add()
        person = population[person_id]
        id = person.get_id()
        state = person.get_state()
        infection_date = person.get_infection_date()
        death_date = person.get_death_date()
        write_out_person(person_proto, id, state, infection_date, death_date)

def write_out_connection_list(connection_list_proto, person_id, connections):
    connection_list_proto.person_id = str(person_id)
    connections = [str(connection) for connection in connections]
    connection_list_proto.connection.extend(connections)

def write_out_network(network_proto, network):
    for person_id in network:
        connection_list_proto = network_proto.connections.add()
        connections = network[person_id]
        write_out_connection_list(connection_list_proto, person_id, connections)

def write_out_temporal_network(simulation_proto, id, timeline, verbose=False):
    temporal_network_proto = simulation_proto.temporal_network.add()
    completion_percent = 0
    for timestep in timeline:
        if verbose:
            completion_percent = (timestep / len(timeline)) * 100
            print("File generation completion: " + str(completion_percent) + "%")
        network_proto = temporal_network_proto.network.add()
        population_proto = temporal_network_proto.population.add()
        network_proto.timestep = str(timestep)
        population_proto.timestep = str(timestep)
        network = timeline[timestep]["network"].get_network()
        population = timeline[timestep]["population"].get_population()
        write_out_network(network_proto, network)
        write_out_population(population_proto, id, population)

def save_simulation_to_file(filepath, timeline, verbose=False):
    print("Writing out to filepath: " + filepath)

    # population = timeline[0]["population"]
    # network = timeline[0]["network"]

    simulation_proto = simulation_pb2.SimulationTimeline()
    simulation_proto.id = str(time.time())

    # Write out the populations
    pop_id = "cityville"
    write_out_temporal_network(simulation_proto, pop_id, timeline, verbose)

    # Write the new person out to disk
    print("Writing out file...")
    f = open(filepath, "wb")
    f.write(simulation_proto.SerializeToString())
    f.close
    print("File written!")

def read_in_people(pop_id, people):
    people_dict = {}
    for person in people:
        id = int(person.id)
        state = person.state

        if person.infection_date:
            infection_date = int(person.infection_date)
        else:
            infection_date = ""

        if person.death_date:
            death_date = int(person.death_date)
        else:
            death_date = ""
        person = data.Person(id, state)
        person.is_infected(infection_date)
        person.is_dead(death_date)
        people_dict[id] = person
    population = data.Population(pop_id, 0)
    population.init_with_dict(people_dict)
    return population


def read_in_population(simulation_proto):
    for field in simulation_proto.temporal_network:
        population = field.population
        population_dict = {}
        for field in population:
            people = field.people
            timestep = int(field.timestep)
            id = field.id
            population = read_in_people(id, people)
            population_dict[timestep] = population
        return population_dict

def read_in_network(simulation_proto):
    for field in simulation_proto.temporal_network:
        network = field.network
        network_dict = {}
        for field in network:
            timestep = int(field.timestep)
            connections = field.connections
            connections_dict = {}
            for field in connections:
                person_id = field.person_id
                connection_repeated_list = field.connection
                connection_list = []
                for connection_id in connection_repeated_list:
                    connection_list.append(int(connection_id))
                connections_dict[person_id] = connection_list
            network_obj = data.Network()
            network_obj.init_from_connections_dict(connections_dict)
            network_dict[timestep] = network_obj.get_network()
        return network_dict

def read_simulation_to_timeline(filepath):
    simulation_proto = simulation_pb2.SimulationTimeline()

    f = open(filepath, "rb")
    print("Reading in data from file...")
    simulation_proto.ParseFromString(f.read())
    f.close()

    print("Extracting population data...")
    population = read_in_population(simulation_proto)
    print("Extracting network data...")
    network = read_in_network(simulation_proto)
    if(len(population) == len(network)):
        # Zip the two dictionaries into a timeline-like dictionary
        timeline = {}
        completion_percent = 0
        for timestep in range(0, len(population)):
            print("Zipping timeline: " + str(completion_percent) + "%")
            completion_percent = (timestep / len(population)) * 100
            timeline[timestep] = {"population": population[timestep], "network": network[timestep]}

        return timeline
