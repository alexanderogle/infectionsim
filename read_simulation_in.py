#!/usr/local/bin/python3
from infectionsim import utilities as util

filepath = "./test.file"
timeline = util.read_simulation_to_timeline(filepath)

# Graph the read-in simulation file:
util.plot_timeline(timeline)
