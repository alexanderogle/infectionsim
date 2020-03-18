# infection_simulation

Have a lot of time to play around with Python? I do. I'm trying to play around
by building some infection simulations that I can eventually fit to actual data.

## Data Structures
The three main data structures are as follows:
- Person
- Population
- Simulation

A Person instance has a unique identifier (currently just an int) and a state.
A Person can have a state of "not infected", "infected", "recovered", or "dead".

A Population object consists of a collection of Person objects. The Population
object has built in functions/methods for keeping track of and managing the
state of its Person objects.

A Simulation object manages the set up and tracks the evolution of state for a
Population object over a specified time.

The process for running the simulation currently goes like this:
1. Create a Population object with a set of Person objects that are not infected.
2. Setup the Simulation and run it.
3. Plot and examine the results.

There are many ways to model the dynamics of a system's change of state, and
hopefully in the future, we will bring in differential equations and some Monte
Carlo simulation.

Articles for further consideration:

  Monte Carlo Simulation: https://towardsdatascience.com/infection-modeling-part-1-87e74645568a

  Mathematical models to characterize early epidemic growth: A Review: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5348083/
