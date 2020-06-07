import pandas as pd 
import network 

columns = ["agent", "connections", "num_connections", "max_connections"]
agents = [0, 1, 2, 3, 4, 5]
connections = [[], [], [], [], [], []]
num_connections = [0, 0, 0, 0, 0, 0]
max_connections = [1, 2, 2, 3, 1, 1]
data = {
        columns[0]: agents, 
        columns[1]: connections,
        columns[2]: num_connections,
        columns[3]: max_connections,
        }
x = pd.DataFrame(data=data)

max_connections_list = x['max_connections']
net = network.PyConnections(x['agent'].size)
random_network = net.gen_random_network(max_connections_list)

# Update the x DataFrame to have the generated connections lists
new_connections = pd.DataFrame({'connections': random_network})
x.update(new_connections)
x.loc[:, 'num_connections'] = 9
x.loc[:, 'num_connections'] = 7

print(x['connections'].size)
for i in range(0, x['connections'].size):
        x.iloc[i, 2] = len(x.iloc[i,1])

print(x)