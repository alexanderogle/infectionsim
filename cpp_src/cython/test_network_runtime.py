import network
import time


sizes = [10, 100, 1000, 10000, 100000, 1000000]
runtimes = []
def experiment(size):
    for num in size:
        # Create a C++ Connections object with a population size of num
        # Note that in Python, the actual object is a PyConnections object
        start = time.time()
        size = 10000
        x = network.PyConnections(size)

        # Get a randomly generated network in the form of a 2d list using the following: 
        connections_max = x.gen_connections_max_vector(10, 11, size)
        random_network = x.gen_random_network(connections_max)
        end = time.time()
        runtime = end - start
        runtimes.append(runtime)
        print(random_network)

experiment(sizes)

for i in range(len(sizes)):
    size = sizes[i]
    runtime = runtimes[i]
    print(f'Runtime for population {size} = {runtime}')