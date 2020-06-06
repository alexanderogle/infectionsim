#include "person.h"

Person::Person(int id, State state){
    setID(id);
    setState(state);
}

void Person::setID(int newID){
    id = newID;
}

int Person::getID(){
    return id;
}

void Person::setState(State newState){
    state = newState;
}

State Person::getState(){
    return state;
}
