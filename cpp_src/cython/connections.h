#ifndef CONNECTIONS_H
#define CONNECTIONS_H

#include <vector>

class Connections {
    private:
    int size;
    public:
    Connections();
    Connections(int newSize);
    int getSize();
    void setSize(int newSize);
    std::vector<int> getAvailable(int personID, int connectionMax, std::vector<std::vector<int> > connections);
    std::vector<std::vector<int> > genRandomNetwork(int connectionMax, bool verbose=false);
};

#endif