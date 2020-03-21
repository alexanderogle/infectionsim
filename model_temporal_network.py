#!/usr/local/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# User defined
from infectionsim import data_structs as data

################################################################################
# Model initial parameters
## Population and Network parameters
population = 1000000
population_name = "cityville"
connection_min_start = 1
connection_max_start = 1
connection_min_end = 1
connection_max_end = 50

# Control whether simulation completion percentage is output to the console:
verbose = True

# Infection propogation parameters
recovery_period = 14
recovery_probability = 0.3
death_probability = 0.01
# A good number for initial infected is 0.5% of the population
initial_infected = int(population * 0.005)
if initial_infected < 1: initial_infected = 1
seed_num = 1459
states = ["susceptible", "infected", "recovered", "dead"]
infection_probability = 0.03
max_days = 50

################################################################################

# Setup the population
pop = data.Population("cityville", population)

# Create a temporal network policy (defines how the network should change over time)
policy = data.Policy("linearly increase isolation")
policy.linearly_interpolated_network_policy(max_days, connection_min_start,
                                    connection_max_start, connection_min_end,
                                    connection_max_end)

temporal_network = data.TemporalNetwork(pop, max_days)
temporal_network.init_random_network(connection_min=connection_min_start,
                                         connection_max=connection_max_start,
                                         seed_num=seed_num,
                                         policy=policy, verbose=verbose)

# Setup and run the network simulation
sim = data.TemporalNetworkSimulation(temporal_network)
print("Seeding simulation...")
sim.seed_simulation(initial_infected, infection_probability, recovery_period,
                    recovery_probability, death_probability, seed_num)
print("Beginning simulation...")
timeline, infection_timeline, susceptible_timeline, recovered_timeline, dead_timeline = sim.simulate(max_days, verbose=verbose)

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
