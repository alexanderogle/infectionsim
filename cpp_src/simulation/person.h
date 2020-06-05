#ifndef PERSON_H
#define PERSON_H
// Header file for defining simulation data structures. 
#include <string> 

// User defined libraries


enum class State {
    infected,
    susceptible,
    removed
};

class Person {
    private: 
        std::string name;
        State state;

    public:
        Person(std::string name, State state=State::susceptible);
        std::string getName();
        void setName(std::string name);
        State getState();
        void setState(State newState);
};

#endif