Installation
=================================

Installation can be performed a number of ways: the Python Package Index (PyPI), from Anaconda, or from the Github page. 

Python Package Index
--------------------

To install the latest version of galah using pip do:

.. prompt:: 

    pip install galah-python

To upgrade to the latest release:

.. prompt:: 

    pip install --upgrade galah-python

Conda
-----

To install the latest release with conda do:
    
.. prompt:: 

    conda config --add channels conda-forge
    conda install galah-python

To upgrade to the latest stable release:

.. prompt:: 

    conda update galah-python

Source
------

Ensure that you have ``git`` installed, and then clone the repo:


.. prompt:: 

    git clone https://github.com/AtlasOfLivingAustralia/galah_python.git

Then go into the ``galah-python/galah`` directory and run the following command:

.. prompt:: 

    pip install .