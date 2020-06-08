// Function for generating a connections list
#include <iostream>
#include <vector>
#include <algorithm>

// User defined libraries
#include "connections.h"

Connections::Connections(){
    // Do nothing
}

Connections::Connections(int newSize){
    setSize(newSize);
}

int Connections::getSize(){
    return size;
}

void Connections::setSize(int newSize){
    size = newSize;
}

bool Connections::existsInVector(int num, std::vector<int> &v){
    for(int i : v){
        if(num == i){
            return true;
        }
    }
    return false;
}

std::vector<int> Connections::genConnectionsMaxVector(int minConnections, int maxConnections, int size){
    std::vector<int> connectionsMax;
    for(int i = 0; i < size; i++){
        int connectionRange = maxConnections - minConnections;
        int randomConnectionSize = std::rand() % connectionRange + minConnections;
        connectionsMax.push_back(randomConnectionSize);
    }
    return connectionsMax;
}

std::vector<int> Connections::getAvailable(int personID, std::vector<int> &connectionsMax, std::vector<std::vector<int> > &connections){
    // Finds all the connections avialable for a given perosn, excluding themselves. 
    std::vector<int> available;

    for (int i = 0; i < connections.size(); i++){
        if (i != personID && !existsInVector(personID, connections[i]) && connections[i].size() < connectionsMax[i]){
            available.push_back(i);
        }
    }
    return available;
}

std::vector<std::vector<int> > Connections::genRandomNetwork(std::vector<int> &connectionsMax, bool verbose, bool testing){
    // Instantiate a 2d vector container for the connections list
    std::vector<std::vector<int> > connections;
    for(int i = 0; i < size; i++){
        std::vector<int> v;
        connections.push_back(v);
    }
    // If testing, Generate a random connectionsMax vector
    if(testing){
        int connectMin = 8;
        int connectMax = 10;
        std::vector<int> connectionsMax = genConnectionsMaxVector(connectMin, connectMax, size);
    }
    // Loop through the connections, and for each, allocate a random connection that is available to connect
    float percent_complete = 0;
    if (verbose){
        std::cout << "Starting to generate random network." << std::endl;
        std::cout << "Percent Complete: " << percent_complete << std::endl;
    }
    for (int i = 0; i < size; i++){
        if (verbose && i % 1000 == 0 ){
            percent_complete = (float)i / (float)size * 100;
            std::cout << "Percent Complete: " << percent_complete << std::endl;
        }
        
        while(connections[i].size() < connectionsMax[i]){
            // Get the available people we can connect with
            std::vector<int> available = getAvailable(i, connectionsMax, connections);
            if(available.size() == 0){
                // No one available to connect with
                break;
            }
            // Pick someone from among those we can connect with
            int randomConnection = std::rand() % available.size();

            // Make sure they aren't already in the person's conenction list
            for (int j = 0; j < connections[i].size(); j++){
                if(randomConnection == connections[i][j]){
                    // This person is already in the connections list, so continue
                    continue;
                }
            }

            connections[i].push_back(available[randomConnection]);
            connections[available[randomConnection]].push_back(i);
        }
    }

    return connections;
}