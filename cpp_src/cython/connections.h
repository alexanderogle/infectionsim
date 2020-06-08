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
    bool existsInVector(int num, std::vector<int> &v);
    std::vector<int> genConnectionsMaxVector(int minConnections, int maxConnections, int size);
    std::vector<int> getAvailable(int personID, std::vector<int> &connectionsMax, std::vector<std::vector<int> > &connections);
    std::vector<std::vector<int> > genRandomNetwork(std::vector<int> &connectionsMax, bool verbose=false, bool testing=false);
};

#endif