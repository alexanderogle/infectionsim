#ifndef POPULATION_H
#define POPULATION_H

#include "person.h"

class Population {
    private: 
        int id;
        std::vector<Person> people;
    public:
        Population(int ID);
        void setID(int newId);
        std::vector<Person> getPeople();
        void addPerson(Person newPerson);
        void genPopulation(int size);
};
#endif