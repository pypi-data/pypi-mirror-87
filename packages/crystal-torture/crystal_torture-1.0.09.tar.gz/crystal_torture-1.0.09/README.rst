|JOSS status| |DOI| |PyPI version| |Build Status| |Coverage Status| |Documentation Status| |Python 3.6| |Python 3.7|

**crystal\_torture:**
---------------------

``crystal_torture`` is a Python, Fortran and OpenMP crystal structure
analysis module. The module contains a set of classes that enable:

-  a crystal structure to be converted into a graph for network analysis
-  connected clusters of crystal sites (nodes) to be retrieved and
   output
-  periodicity of connected clusters of crystal sites to be determined
-  relative path tortuosity to traverse a crystal within a connected
   cluster to be calculated for each site

Installation
------------

``crystal_torture`` requires python 3.6 and above. To install do:

::

    pip install crystal_torture

or download directly from
`GitHub <http://github.com/connorourke/crystal_torture/releases>`__, or
clone:

::

     git clone https://github.com/connorourke/crystal_torture

and install

::

    cd crystal_torture
    python setup.py install

Tests
-----

``crystal_torture`` is automatically tested on each commit
`here <http://travis-ci.org/connorourke/crystal_torture>`__, but the
tests can be manually run:

::

    python -m unittest discover

Examples
--------

Examples on how to use ``crystal_torture`` can be found in a Jupyter
notebook in the ``examples`` directory
`crystal\_torture\_examples.ipynb <http://nbviewer.jupyter.org/github/connorourke/crystal_torture/blob/master/examples/crystal_torture_examples.ipynb>`__

Documentation
-------------

Documentation can be found
`here <https://crystal-torture.readthedocs.io/en/latest/>`__

.. |JOSS status| image:: http://joss.theoj.org/papers/c3d8e702ecfee04f16a0ad6f14d96419/status.svg
   :target: http://joss.theoj.org/papers/c3d8e702ecfee04f16a0ad6f14d96419
.. |PyPI version| image:: https://badge.fury.io/py/crystal-torture.svg 
   :target: https://badge.fury.io/py/crystal-torture
.. |Build Status| image:: https://travis-ci.com/connorourke/crystal_torture.svg?token=nTMqYYEUasQRTBsU6oCc&branch=master
   :target: https://travis-ci.com/connorourke/crystal_torture
.. |Coverage Status| image:: https://coveralls.io/repos/github/connorourke/crystal_torture/badge.svg?branch=master
   :target: https://coveralls.io/github/connorourke/crystal_torture?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/crystal-torture/badge/?version=latest
   :target: https://crystal-torture.readthedocs.io/en/latest/?badge=latest
.. |Python 3.6| image:: https://img.shields.io/badge/python-3.6-blue.svg 
   :target: https://www.python.org/downloads/release/python-360/
.. |Python 3.7| image:: https://img.shields.io/badge/python-3.7-blue.svg 
   :target: https://www.python.org/downloads/release/python-360/
.. |DOI| image:: https://zenodo.org/badge/139595328.svg
   :target: https://zenodo.org/badge/latestdoi/139595328
