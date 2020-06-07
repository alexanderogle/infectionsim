from libcpp.vector cimport vector

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
        vector[int] getAvailable(int, int, vector[vector[int]])
        vector[vector[int]] genRandomNetwork(int, bool)