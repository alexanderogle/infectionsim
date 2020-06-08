import network
import time
import pandas as pd

sizes = []
sizes.append(10)
sizes.append(100)
for i in range(1, 100 + 1):
    num = 1000 * i
    sizes.append(num)
runtimes = []
def experiment(size):
    for num in sizes:
        print(f'Running size {num}.')
        # Create a C++ Connections object with a population size of num
        # Note that in Python, the actual object is a PyConnections object
        start = time.time()
        x = network.PyConnections(num)
        # Get a randomly generated network in the form of a 2d list using the following: 
        connections_max = x.gen_connections_max_vector(10, 11, num)
        random_network = x.gen_random_network(connections_max)
        end = time.time()
        runtime = end - start
        runtimes.append(runtime)

experiment(sizes)

for i in range(len(sizes)):
    size = sizes[i]
    runtime = runtimes[i]
    print(f'Runtime for population {size} = {runtime}')
    
data = {'sizes': sizes, 'runtimes': runtimes}
df = pd.DataFrame(data)
df.to_csv('./test_network_results.csv')