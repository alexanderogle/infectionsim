#include "person.h"

Person::Person(std::string name, State state){
    setName(name);
    setState(state);
}

void Person::setName(std::string newName){
    name = newName;
}

std::string Person::getName(){
    return name;
}

void Person::setState(State newState){
    state = newState;
}

State Person::getState(){
    return state;
}
