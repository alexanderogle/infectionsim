#!/usr/local/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# User defined
from infectionsim import data_structs as data
from infectionsim import utilities as util

start_time = time.time()
################################################################################
# Simulation write out options
save_simulation = False
plot_simulation = True

# Model initial parameters
## Population and Network parameters
population = 1000
population_name = "cityville"
connection_min_start = 1
connection_max_start = 10
connection_min_end = 1
connection_max_end = 10

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
print("Generating population...")
pop = data.Population("cityville", population)

# Create a temporal network policy (defines how the network should change over time)
policy = data.Policy("linearly increase isolation")
print("Generating policy...")
policy.linearly_interpolated_network_policy(max_days, connection_min_start,
                                    connection_max_start, connection_min_end,
                                    connection_max_end)

# Edit the policy so it has an opening from day 20 to day 21, where people no
# longer have to isolate, letting their connections range from 30-50. 
days = [20,21]
connections_start = [30, 50]
connections_end = [30, 50]
policy.edit_policy(days, connections_start, connections_end)

temporal_network = data.TemporalNetwork(pop, max_days)
print("Generating temporal network...")
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
timeline = sim.simulate(max_days, verbose=verbose)

execution_time = time.time() - start_time
print("Simulation completed in " + str(execution_time) + " seconds.")

# Write out the simulation to file
if save_simulation:
    filepath = "./" + "sim_" + str(int(time.time())) + ".infectionsim"
    util.save_simulation_to_file(filepath, timeline, verbose=False)

    execution_time = time.time() - start_time
    print("Simulation and file output in: " + str(execution_time) + " seconds.")

# Plot the simulation
if plot_simulation:
    util.plot_timeline(timeline)
