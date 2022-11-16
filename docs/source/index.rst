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
petrobuffer is available on PyPi, and can be downloaded with pip:
::
   
   pip install petrobuffer

.. note:: 
   petrobuffer is not yet packaged for Anaconda, and as such ``conda install petrobuffer`` will not work.

Alternatively, to access the most up-to-date *development* version, you can `clone the package from github <https://github.com/pipliggins/PetroBuffer>`_ into the same root directory as your project files where you wish to use PetroBuffer.

The package can then be pip installed by running
::

   pip install PetroBuffer/

from your project root, and imported in your files in the same way as other packages, using
::

   import petrobuffer

.. warning::
   Note that breaking changes occur can occur when importing a package this way, and it is not guaranteed to remain stable.

For usage examples, see :doc:`examples`.

Limitations
***********

- ``PetroBuffer`` currently only supports a small number of functions. The aim is to expand this package over time.

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
