// Main script for running simulation
#include <iostream>
#include <vector>
#include <string>

// User defined libraries
#include "time.h"
#include "person.h"
#include "population.h"
#include "network.h"


int main(int argc, const char* argv[]){

    // Get start time
    time_t start, end;
    time(&start);
    // Create a new Network object
    Network network(0, 0, 10);
    network.genRandomNetwork(10, true);
    time(&end);
    int runtime = end - start;
    network.printNetwork();
    std::cout << "Finished in " << runtime << " seconds.\n";
    return 0;
}