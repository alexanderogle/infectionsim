#ifndef NETWORK_H
#define NETWORK_H

#include <vector> 

// User defined libraries
#include "population.h"

class Network{
    private:
        int id;
        int popID;
        int size;
        Population population;
        // { Person { other person ids Person is connected to } }
        std::vector<std::vector<int>> connections;
        bool available_to_connect(int id);

    public: 
        Network(int id, int popID, int newSize);
        int getID();
        void setID(int newID);
        int getSize();
        void setSize(int newSize);
        void setupConnections(int size);
        void genRandomNetwork(int connection_max, bool verbose);
        void genTrivialNetwork();
        void printNetwork();
        bool existsInVector(int num, std::vector<int> v);
        bool availableToConnect(int personID, int connectionMax);

        std::vector<int> getAvailable(int personID, int connectionMax);
};

#endif