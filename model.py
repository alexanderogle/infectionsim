#!/usr/local/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# User defined
import data_structs as data

# Model initial parameters
population = 100000
recovery_period = 14
death_rate = 0.05
initial_infected = 1
seed_num = 1459
states = ["not infected", "infected", "recovered", "dead"]
P = 0.01
t = 60

# Setup the population
pop = data.Population()
for i in range(0, population):
    pop.add_people(data.Person(i, states[0]))

# Setup and run the simulation
sim = data.Simulation(pop)
sim.seed_simulation(initial_infected, P, recovery_period, death_rate, seed_num)
timeline, infection_timeline, not_infected_timeline, alive_timeline = sim.simulate(t)


infected = pd.DataFrame.from_dict(infection_timeline, orient="index", columns=["number infected"])
not_infected = pd.DataFrame.from_dict(not_infected_timeline, orient="index", columns=["number not infected"])
alive = pd.DataFrame.from_dict(alive_timeline, orient="index", columns=["number alive"])
plt.plot(infected)
plt.plot(not_infected)
plt.plot(alive)
plt.legend(["infected", "not infected", "alive"])
plt.show()
