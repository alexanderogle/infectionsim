#include <iostream>
#include <vector>

#include "connections.h"

int main(){
    Connections a(100);
    int size = a.getSize();
    std::cout << size << std::endl;
}