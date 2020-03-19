#!/usr/local/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# User defined
import data_structs as data

################################################################################
# Data input/output parameters
# TODO(aogle): Fix read_in_data functionality, currently graph is outputting a
# flattened curve, might have to do with presence of NaNs in data?
read_in_data = False
write_out_data = not read_in_data
write_out_path = './large_network_pop_100000_conmin_1_conmax_50'
read_in_path = './large_network_pop_100000_conmin_1_conmax_50'

# Model initial parameters
## Population and Network parameters
population = 100000
population_name = "cityville"
connection_min = 1
connection_max = 8

# Infection propogation parameters
recovery_period = 14
recovery_probability = 0.3
death_probability = 0.01
initial_infected = int(population * 0.005)
seed_num = 1459
states = ["susceptible", "infected", "recovered", "dead"]
infection_probability = 0.03
t = 120

################################################################################

# Setup the population
pop = data.Population("cityville", population)

if not read_in_data:
    # Setup the Network
    network = data.Network(pop)
    network.init_random_network(connection_min=connection_min, connection_max=connection_max, seed_num=seed_num)

if write_out_data:
    network.to_csv(write_out_path)

if read_in_data:
    network = data.Network(pop)
    network.from_csv(read_in_path)
    print("Network created from data located at: " + read_in_path)

# Setup and run the network simulation
sim = data.NetworkSimulation(network)
print("Seeding simulation...")
sim.seed_simulation(initial_infected, infection_probability, recovery_period,
                    recovery_probability, death_probability, seed_num)
print("Beginning simulation...")
timeline, infection_timeline, susceptible_timeline, recovered_timeline, dead_timeline = sim.simulate(t)

# Plot results
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
