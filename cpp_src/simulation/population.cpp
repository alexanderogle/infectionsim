#include <string>
#include <vector>

// User defined libraries
#include "population.h"

Population::Population(){
}

void Population::setID(int newID){
    id = newID;
}

std::vector<Person> Population::getPeople(){
    return people;
}

void Population::addPerson(Person newPerson){
    people.push_back(newPerson);
}

void Population::genPopulation(int size){
    // Reset the people vector
    people = {};
    for (int i = 0; i < size; i++){
        Person newPerson(i);
        people.push_back(newPerson);
    }
}

int Population::size(){
    return people.size();
}