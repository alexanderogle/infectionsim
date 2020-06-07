import network

# Create a C++ Connections object with a population size of 1000
# Note that in Python, the actual object is a PyConnections object
size = 1000
x = network.PyConnections(size)

# Get a randomly generated network in the form of a 2d list using the following: 
connections_max = x.gen_connections_max_vector(8, 9, size)
random_network = x.gen_random_network(connections_max)

# Print the random network so you can see what it looks like
print(random_network)