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

    def get_available(self, int personID, int connectionMax, vector[vector[int]] connections):
        return self.c_connections.getAvailable(personID, connectionMax, connections)

    def gen_random_network(self, int connectionMax, bool verbose=False):
        return self.c_connections.genRandomNetwork(connectionMax, verbose)

    