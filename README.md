# infection_simulation

Have a lot of time to play around with Python? I do. I'm trying to play around
by building some infection simulations that I can eventually fit to actual data.

## Data Structures
The six main data structures are as follows:
- Person
- Population
- Network
  - TODO(alexanderogle): fix import issues (NaNs values, etc.)
- TemporalNetwork
  - TODO(alexanderogle): add CSV import/export capabilities
- Policy
- Simulation
  - Simulation(): base class for simulations
  - NetworkSimulation(): inherits Simulation, simulates static networks
  - TemporalNetworkSimulation(): inherits NetworkSimulation, simulates temporally
  variant networks

A Person instance has a unique identifier (currently just an int) and a state.
A Person can have a state of "susceptible", "infected", "recovered", or "dead".

A Population object consists of a collection of Person objects. The Population
object has built in functions/methods for keeping track of and managing the
state of its Person objects.

A Network object generates a connections list for a population and allows networks
to be exported and imported as CSVs. You can thus generate a large and densely
connected network once and then use it repeatedly for future simulations.

A TemporalNetwork object is a collection of Network objects. TemporalNetwork
manages state and generation of these Network objects.

A Policy is a dictionary which keeps track of how parameters change over time.
This can be used to simulate a change in the max/min of the connections in a network,
or even to change the death rate or infection probability. A policy represents
changes implemented by governments or from viral adaptions or the presence of a
vaccine that affects the mechanics of the simulation.

A Simulation object manages the set up and tracks the evolution of state for a
Population object over a specified time.

A NetworkSimulation object manages the setup and tracks the evolution of state for
a Population object that is structured by a Network object.

A TemporalNetworkSimulation object manages the setup and tracks the evolution of state
for a Population object that is structured by a TemporalNetwork object. Ideally,
the TemporalNetwork would be defined in such a way as to simulate events where
policies such as social distancing are implemented (the max connections between
people decreases to some minimum over a small time period, and is maintained for
some period of time).

## Simulation Process Abstractly:
The process for running the simulation (done in a model.py file) currently goes like this:
1. Create a Population object.
2. Generate a Network or TemporalNetwork object depending on the type of simulation
desired (the base Simulation class does not use Network objects). If a TemporalNetwork
is being generated, the user can define a Policy object that will determine the temporal
evolution of the network (essentially how the minimum and maximum number of randomly
chosen connections between Person objects change over time).
3. Setup the Simulation with user defined initial conditions and run it.
Define what kind of simulation to run here (can be the base Simulation, NetworkSimulation
or TemporalNetworkSimulation). For each day, the simulation will randomly select
the change of state for Person objects depending on their network connections,
the infection, recovery, and death probabilities, and the recovery period for that day.
Policy objects can change how these parameters vary for each day. The essential
day-to-day mechanics for Person objects can be found in the update() function of
each Simulation object.
4. Plot and examine the results.

## To Run a Simulation:
1. Edit either 'model_static_network.py' or 'model_temporal_network.py' as desired
or create your own model_.py file
2. Run $ python3 model.py

Required dependencies:
- pandas (install with 'pip3 pandas' on Mac OSX)
- numpy
- matplotlib
- random

## Comparing to Naturalistic Data:
For a comparison to your simulation, run data_fitting.py, which pulls the latest
COVID-19 full dataset from https://ourworldindata.org/coronavirus-source-data and plots it.

## Example Output
Here's an example which had people with connections ranging from 1 - 50 other people.
Notice the narrow bell shape of the infection line.

![SRI Model with moderately dense network (max connections of 50)](example1_max_connections_50.png)

And here is the output when social distancing is implemented (connections were more limited
ranging from 1 - 8 other people). This is "flattening the curve".

![SRI model with light network (max connections of 8)](example2_max_connections_8.png)

## Future Directions
There are many ways to model the dynamics of a system's change of state, and
hopefully in the future, we will bring in differential equations and some Monte
Carlo simulation.

Articles for further consideration:

  Monte Carlo Simulation - https://towardsdatascience.com/infection-modeling-part-1-87e74645568a

  Mathematical models to characterize early epidemic growth: A Review - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5348083/

  A Network-Based Compartmental Model For The Spread Of Whooping Cough In Nebraska - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6568137/

  Impact of non-pharmaceutical interventions (NPIs) to reduce COVID19 mortality and healthcare demand: https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf?fbclid=IwAR13T_bDz3d0Vr4UCZAmVIN5gU8O2VG-OCKn8fpeJc51W7YysL_S85RAi6M

  Strategies for mitigating an influenza pandemic: https://www.nature.com/articles/nature04795

  Modeling targeted layered containment of an influenza pandemic in the United States: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2290797/
