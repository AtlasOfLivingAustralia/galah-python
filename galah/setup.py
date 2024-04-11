'''
This is the setup script for galah.  It contains all of the package information
and dependencies
'''
from setuptools import setup,find_packages
import os

pkg_vars  = {}

with open("src/galah/version.py") as fp:
    exec(fp.read(), pkg_vars)

os.system("conda install geos")
os.system("pip install packaging")

setup(
    #name='galah',
    version=pkg_vars['__version__'],
    license='MPL-2.0',
    author='Amanda Buyan',
    author_email='amanda.buyan@csiro.au',
    description="Get counts and information on species from many different atlases",
    long_description="Get counts and information on species from many different atlases",
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'':'src'},
    url='https://galah.ala.org.au/Python/',
    keywords='galah',
    #'tempfile'
    install_requires=[
        'setuptools',
        'numpy',
        'pandas',
        'requests',
        'urllib3',
        'zip-files',
        'configparser',
        'glob2',
        'bytesbufio',
        'shutils',
        'pytest',
        'unittest2py3k',
        'shapely',
        'geopandas'
    ],


    # ], #,'PyJWT','python-jwt'
    #'TIME-python',
    include_package_data = True,
    package_data = {
    # If any package contains *.ini files or *.csv files, include them
    '': ['config.ini','node_config.csv','gbif_assertions.csv','gbif_fields.csv','ALA_keys.json'],
    },
)
