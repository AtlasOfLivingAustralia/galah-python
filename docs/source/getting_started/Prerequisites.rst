Prerequisites
=================================

You will need the following packages to be able to run ``galah``:

- `numpy <https://numpy.org/>`_
- `pandas <https://pandas.pydata.org/>`_
- `requests <https://requests.readthedocs.io/en/latest/>`_
- `urllib3 <https://urllib3.readthedocs.io/en/stable/>`_
- `TIME-python <https://pypi.org/project/TIME-python/>`_
- `zip-files <https://pypi.org/project/zip-files/>`_
- `configparser <https://pypi.org/project/configparser/>`_
- `glob2 <https://pypi.org/project/glob2/>`_
- `shutils <https://pypi.org/project/shutils/>`_
- `setuptools <https://pypi.org/project/setuptools/>`_
- `shapely <https://pypi.org/project/shapely/>`_
- `pytest <https://pypi.org/project/pytest/>`_
- `unittest2py3k <https://pypi.org/project/unittest2py3k/>`_

To install all of these at once, run

.. prompt:: 

    pip install numpy scipy pandas requests urllib3 TIME-python zip-files configparser glob2 bytesbufio shutils setuptools shapely pytest unittest2py3k

WARNING: If you're installing all of the packages in one go, make sure you check that the installation ran successfully.  If one package doesn't work, the rest following won't install...