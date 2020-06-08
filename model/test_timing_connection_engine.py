from connection_engine_timing_test import ConnectionEngine
from population_engine import PopulationEngine
from settings import SimfectionSettings
import pandas as pd

# Use default settings
settings = SimfectionSettings(None)
# Use cpp optimization
settings.set_setting('cpp', True)

sizes = []
sizes.append(10)
sizes.append(100)
for i in range(1, 100 + 1):
    num = 1000 * i
    sizes.append(num)

runtimes = []
def experiment(size):
    for num in sizes:
       # Set the population here
        settings.set_setting('num_people', num)
        popengine = PopulationEngine(settings)
        popengine.make_dummy()
        population = popengine._df
        connectengine = ConnectionEngine(population, settings)
        runtime = connectengine.create_connections(settings.get_setting('cpp'))
        runtimes.append(runtime)

# Run the experiment:
experiment(sizes)

# Print out the results
for i in range(len(sizes)):
    size = sizes[i]
    runtime = runtimes[i]
    print(f'Runtime for population {size} = {runtime}')

# Save the data to a csv
data = {'sizes': sizes, 'runtimes': runtimes}
df = pd.DataFrame(data)
df.to_csv('./test_timing_connection_engine_results.csv')

