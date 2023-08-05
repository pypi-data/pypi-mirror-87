#!/usr/bin/env python
from setuptools import setup, Extension

modules = ["grammar", "parsing", "special", "tokens"]

try:
    from Cython.Build import cythonize
except ImportError:
    ext_modules = [
        Extension(f"codewhisper.{module}", [f"src/codewhisper/{module}.c"])
        for module in modules
    ]
else:
    ext_modules = cythonize([
        Extension(f"codewhisper.{module}", [f"src/codewhisper/{module}.pyx"])
        for module in modules
    ], compiler_directives={"language_level": 3})

setup(ext_modules=ext_modules)
