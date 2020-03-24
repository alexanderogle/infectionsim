#!/usr/local/bin/python3
from infectionsim import utilities as util
import time

start_time = time.time()

################################################################################
# Adjust filepath to be the name of the simulation file you want to read in.   #
################################################################################
filepath = "./test.simulation"

# Read in simulation data
timeline = util.read_simulation_to_timeline(filepath)

execution_time = time.time() - start_time
print("Read file in " + str(execution_time) + " seconds.")
# Graph the read-in simulation file:
print("Graphing timeline...")
util.plot_timeline(timeline)
