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


Compiling and Linking Manually (UNVERIFIED -- HAVEN'T GOTTEN TO WORK YET)
Information found from here: https://stackoverflow.com/questions/28366147/how-can-i-manually-compile-cython-code-that-uses-c

If you want to compile the .o files manually (to make sure certain optimizations are being made), do the following:

1. Build the connections.o file using:
$ g++ -std=c++11 -O3 -c connections.cpp

2. Use Cython to generate the network.cpp file
$ cython --cplus network.pyx

3. Run '$ which python3' and take note of the directory used for python3

4. Find and make sure to export the path for your python header file 'Python.h', you can find it first with:
$ sudo find / -iname "Python.h"
and then add the Python.h path you want to your CPLUS_INCLUDE_PATH like this: 
$ export CPLUS_INCLUDE_PATH=/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/include/python3.7m/ 

5. Compile and link connections.o and network.cpp:
$ g++ -std=c++11 -O3 -shared -fPIC -I/usr/local/bin/python3 network.cpp connections.o -lstdc++ -o network.so