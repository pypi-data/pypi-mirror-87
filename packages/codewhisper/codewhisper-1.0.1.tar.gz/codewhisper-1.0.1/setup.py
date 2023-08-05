#!/usr/bin/env python
from setuptools import setup, Extension

modules = ["grammar", "parsing", "special", "tokens"]

try:
    from Cython.Build import cythonize
    from pathlib import Path
    compiled = all(Path(f"src/codewhisper/{module}.pyx").exists() for module in modules)
except ImportError:
    compiled = False

if compiled:
    ext_modules = cythonize([
        Extension(f"codewhisper.{module}", [f"src/codewhisper/{module}.pyx"])
        for module in modules
    ], compiler_directives={"language_level": 3})
else:
    ext_modules = [
        Extension(f"codewhisper.{module}", [f"src/codewhisper/{module}.c"])
        for module in modules
    ]

setup(ext_modules=ext_modules)
