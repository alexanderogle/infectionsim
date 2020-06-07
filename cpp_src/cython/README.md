This Cython directory contains the code to build the connections list generator defined in the C++ files: 
connections.cpp
connections.h

The C++ API is exposed in Cython according to the files:
connections.pxd (Cython header-esque file)
network.pyx 
setup.py (File for setting up Cython build)

To build the Python bindings with Cython, use the following in a terminal while in this directory: 
$ python3 setup.py build_ext --inplace

You'll see a good number of warnings which you can ignore for now, and finally you should see the following generated:
network.cpython-37m-darwin.so

This file will be needed to allow importing of the C++ code. 