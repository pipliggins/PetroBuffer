# PetroBuffer
A python package for performing geochemical redox calculations and buffer conversions.

The current implementation has been developed in Python 3 and tested on Windows.

``PetroBuffer`` currently only supports a small number of functions. The aim is to expand this package over time.

## Installation/Usage:

As this package has yet to be published on PyPI, it CANNOT be installed using pip alone.

For now, the suggested method is to clone this repository into the same root directory as your project files where you wish to use `PetroBuffer`.

The package can then be pip installed by running
```
pip install PetroBuffer/
```
from your project root, and imported in your files in the same way as other packages, using 
```
import petrobuffer
```

## Acknowledgements

The testing of this package made heavy use of the excellent Excel tools from Kayla Iacovino: an [fO2 buffer calculator](https://doi.org/10.5281/zenodo.5907867)  and a [Ferric/Ferrous converter](https://doi.org/10.5281/zenodo.5907844).
