#!/usr/local/bin/python3
import matplotlib.pyplot as plt
import pandas as pd

# File that holds utility functions to be used in the code base
def save_simulation_to_file(filepath, timeline):
    print("Writing out to filepath: " + filepath)

    population = timeline[0]["population"]
    network = timeline[0]["network"]

    # for dict_id in timeline:
    #     print(timeline[dict_id]['population'])
    # for person_id in population_dict:
    #     print(population_dict[person_id])

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
