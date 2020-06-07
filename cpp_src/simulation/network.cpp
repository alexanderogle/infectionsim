#include <iostream>
#include <vector>
#include <algorithm>

#include "network.h"
#include "population.h"

Network::Network(int id, int newPopID, int newSize){
    setID(id);
    popID = newPopID;
    setSize(newSize);
    // Reserve the space needed for the connections vector
    setupConnections(newSize);
    population.setID(newPopID);
    population.genPopulation(newSize);
}

void Network::setID(int newID){
    id = newID;
}

int Network::getID(){
    return id;
}

void Network::setSize(int newSize){
    size = newSize;
}

int Network::getSize(){
    return size;
}

void Network::setupConnections(int size){
    connections.clear();
    for(int i = 0; i < size; i++){
        std::vector<int> v = {};
        connections.push_back(v);
    }
}

bool Network::existsInVector(int num, std::vector<int> v){
    for(int i : v){
        if(num == i){
            return true;
        }
    }
    return false;
}

bool Network::availableToConnect(int personID, int connectionMax){
    // Is there space for the Person of personID to connect? 
    for (int i = 0; i < connections.size(); i++){
        if (i == personID && connections[i].size() < connectionMax){
            return true;
        }
    }
    return false;
}

std::vector<int> Network::getAvailable(int personID, int connectionMax){
    // Finds all the connections avialable for a given perosn, excluding themselves. 
    std::vector<int> available = {};
    for (int i = 0; i < connections.size(); i++){
        if (i != personID && !existsInVector(personID, connections[i]) && connections[i].size() < connectionMax){
            available.push_back(i);
        }
    }
    return available;
}

void Network::genRandomNetwork(int connectionMax, bool verbose=false){
    // Clear the connections before generating a random set of connections
    setupConnections(size);
    // Loop through the connections, and for each, allocate a random connection that is available to connect
    float percent_complete = 0;
    if (verbose){
        std::cout << "Starting to generate random network." << std::endl;
        std::cout << "Percent Complete: " << percent_complete << std::endl;
    }
    for (int i = 0; i < population.size(); i++){
        if (verbose && i % 1000 == 0 ){
            percent_complete = (float)i / (float)population.size() * 100;
            std::cout << "Percent Complete: " << percent_complete << std::endl;
        }
        
        while(connections[i].size() < connectionMax){
            // Get the available people we can connect with
            std::vector<int> available = getAvailable(i, connectionMax);
            if(available.size() == 0){
                // No one available to connect with
                break;
            }
            // Pick someone from among those we can connect with
            int randomConnection = std::rand() % available.size();

            connections[i].push_back(available[randomConnection]);
            connections[available[randomConnection]].push_back(i);
        }
    }
}

void Network::genTrivialNetwork(){
    setupConnections(size);
    // Make everything connected to 1
    for (int i = 0; i < population.size(); i++){
        connections[i].push_back(1);
    }
}

void Network::printNetwork(){
    std::cout << "connections.size() = " << connections.size() << std::endl;
    for (std::vector<int> v : connections){
        for (int i : v){
            std::cout << i << " ";
        }
        std::cout << std::endl;
    }
}

