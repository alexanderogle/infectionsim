from libcpp.vector cimport vector
from libcpp cimport bool

# Declare the class with cdef
cdef extern from "connections.h":
    cdef cppclass Connections:
        # private:
        int size 
        # public: 
        Connections() except +
        Connections(int) except +
        int getSize()
        void setSize(int)
        bool existsInVector(int, vector[int])
        vector[int] genConnectionsMaxVector(int, int, int)
        vector[int] getAvailable(int, vector[int], vector[vector[int]])
        vector[vector[int]] genRandomNetwork(vector[int], bool, bool)