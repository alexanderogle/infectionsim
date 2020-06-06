#ifndef POPULATION_H
#define POPULATION_H

#include "person.h"

class Population {
    private: 
        int id;
        std::vector<Person> people;
    public:
        Population();
        void setID(int newId);
        std::vector<Person> getPeople();
        void addPerson(Person newPerson);
        void genPopulation(int size);
        int size();
};
#endif