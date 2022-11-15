.. PetroBuffer documentation master file, created by
   sphinx-quickstart on Tue Nov 15 12:00:19 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PetroBuffer's documentation!
=======================================

``PetroBuffer`` is a Python package which performs redox and buffer conversions common in geochemistry.

The current implementation has been developed in Python 3 and tested on Windows.

Installation/Usage:
*******************

As this package has yet to be published on PyPI, it CANNOT be installed using pip.

For now, the suggested method is to put the folder `petrobuffer` and it's contents in the same directory as your source files and call ``import petrobuffer``.

Limitations
***********

- ``PetroBuffer`` currently only supports a small number of functions. The aim is to expand this module over time.

Acknowledgements
****************

The testing of this package made heavy use of the excellent Excel tools from Kayla Iacovino: an `fO2 buffer calculator <https://doi.org/10.5281/zenodo.5907867>`_  and a `Ferric/Ferrous converter <https://doi.org/10.5281/zenodo.5907844>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   models
   examples
   petrobuffer

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
