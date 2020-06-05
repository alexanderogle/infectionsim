// Main script for running simulation
#include <iostream>
#include <vector>
#include <string>

// User defined libraries
#include "person.h"
#include "population.h"


int main(){
    // Instantiate a population
    Population population(0);
    population.genPopulation(100);

    std::vector<Person> people = population.getPeople();
    for (Person person : people){
        if (person.getState() == State::susceptible){
            std::cout << "Person object at " << &person << " is susceptible." << std::endl;
        }
        else if (person.getState() == State::infected){
            std::cout << "Person object at " << &person << " is infected." << std::endl;
        }
        else if (person.getState() == State::removed){
            std::cout << "Person object at " << &person << " is removed." << std::endl;
        }
    }
    std::string name = "Alex";
    Person alex(name);
    std::cout << alex.getName() << std::endl;
    return 0;
}