# Wrapping the connections list code 
# distutils: sources = connections.cpp
# distutils: language = c++

from libcpp.vector cimport vector
from libcpp cimport bool

from connections cimport Connections

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef class PyConnections:
    cdef Connections c_connections  # Hold a C++ instance which we're wrapping

    def __cinit__(self, int size):
        self.c_connections = Connections(size)

    def get_size(self):
        return self.c_connections.getSize()

    def set_size(self, int size):
        self.c_connections.setSize(size)

    def gen_connections_max_vector(self, int minConnections, int maxConnections, int size):
        return self.c_connections.genConnectionsMaxVector(minConnections, maxConnections, size)

    def get_available(self, int personID, vector[int] connectionsMax, vector[vector[int]] connections):
        return self.c_connections.getAvailable(personID, connectionsMax, connections)

    def gen_random_network(self, vector[int] connectionsMax, bool verbose=False, bool testing=False):
        return self.c_connections.genRandomNetwork(connectionsMax, verbose, testing)

    