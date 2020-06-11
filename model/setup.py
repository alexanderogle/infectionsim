from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

# This file will only work when the Cython compile code is run from the /model/ directory. 

### Example from https://stackoverflow.com/questions/49353463/cython-compiled-ok-but-symbol-not-found-znss4-rep20-s-empty-rep-storagee-whe
ext_modules=[
    Extension(
        "network",
        sources=["./cpp_src/network.pyx"],
        language="c++",
        extra_compile_args=['-std=c++11', '-O3'],
    )
]
setup(
    name = "network",
    ext_modules = cythonize(ext_modules)
)



