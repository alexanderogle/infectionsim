#include <iostream>
#include <vector>
#include <ctime> 

#include "connections.h"

int main(){
    time_t start, end;
    time(&start);
    int size = 10000;
    int min = 9;
    int max = 11;
    Connections a(size);
    size = a.getSize();
    std::vector<int> connectionsMax;
    connectionsMax = a.genConnectionsMaxVector(min, max, size);
    a.genRandomNetwork(connectionsMax);
    time(&end);
    std::cout << "Time to completion: " << end - start << std::endl;
    std::cout << size << std::endl;
}