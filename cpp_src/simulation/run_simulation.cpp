// Main script for running simulation
#include <iostream>
#include <vector>
#include <string>

// User defined libraries
#include "time.h"
#include "person.h"
#include "population.h"
#include "network.h"


int main(){

    // Get start time
    time_t start, end;
    time(&start);
    // Instantiate a population
    Population population;
    population.setID(0);
    population.genPopulation(100);

    // std::vector<Person> people = population.getPeople();
    // for (Person person : people){
    //     if (person.getState() == State::susceptible){
    //         std::cout << "Person object at " << &person << " is susceptible." << std::endl;
    //     }
    //     else if (person.getState() == State::infected){
    //         std::cout << "Person object at " << &person << " is infected." << std::endl;
    //     }
    //     else if (person.getState() == State::removed){
    //         std::cout << "Person object at " << &person << " is removed." << std::endl;
    //     }
    // }
    
    // Create a new Network object
    Network network(0, 0, 50000);
    network.genRandomNetwork(10, true);
    time(&end);
    network.printNetwork();
    // network.genTrivialNetwork();
    // network.printNetwork();
    
    std::cout << "Finished in " << end - start << " seconds.\n";
    return 0;
}