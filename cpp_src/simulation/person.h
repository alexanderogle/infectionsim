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
        int id;
        State state;

    public:
        Person(int id, State state=State::susceptible);
        int getID();
        void setID(int newID);
        State getState();
        void setState(State newState);
};

#endif