import network

# Create a C++ Connections object with a population size of 1000
# Note that in Python, the actual object is a PyConnections object
x = network.PyConnections(1000)

# Get a randomly generated network in the form of a 2d list using the following: 
connection_max = 10
random_network = x.gen_random_network(connection_max)

# Print the random network so you can see what it looks like
print(random_network)