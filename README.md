# PetroBuffer
A python package for performing geochemical redox calculations and buffer conversions.

[![Documentation Status](https://readthedocs.org/projects/petrobuffer/badge/?version=latest)](https://petrobuffer.readthedocs.io/en/latest/?badge=latest)

The current implementation has been developed in Python 3 and tested on Windows.

PetroBuffer currently only supports a small number of functions. The aim is to expand this package over time.

## Documentation

PetroBuffer's documentation is hosted on [Read the Docs](https://petrobuffer.readthedocs.io/en/latest/).

## Installation/Usage:
[![PyPI](https://img.shields.io/pypi/v/petrobuffer.svg?style=flat)](https://pypi.python.org/pypi/petrobuffer)
[![Compatible Python Versions](https://img.shields.io/pypi/pyversions/petrobuffer.svg?style=flat)](https://pypi.python.org/pypi/petrobuffer/)

```
pip install petrobuffer
```

Alternatively, to access the most up-to-date `development` version, you can clone this repository into the same root directory as your project files where you wish to use `PetroBuffer`.

The package can then be pip installed by running
```
pip install PetroBuffer/
```
from your project root, and imported in your files in the same way as other packages, using 
```
import petrobuffer
```

Check out the documentation for usage [examples](https://petrobuffer.readthedocs.io/en/latest/examples.html).

## Acknowledgements

The testing of this package made heavy use of the excellent Excel tools from Kayla Iacovino: an [fO2 buffer calculator](https://doi.org/10.5281/zenodo.5907867)  and a [Ferric/Ferrous converter](https://doi.org/10.5281/zenodo.5907844).
