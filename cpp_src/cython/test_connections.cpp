#include <iostream>
#include <vector>

#include "connections.h"

int main(){
    int size = 100;
    int min = 8;
    int max = 10;
    Connections a(size);
    size = a.getSize();
    std::vector<int> connectionsMax;
    connectionsMax = a.genConnectionsMaxVector(min, max, size);
    a.genRandomNetwork(connectionsMax);
    std::cout << size << std::endl;
}