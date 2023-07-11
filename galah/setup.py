'''
This is the setup script for galah.  It contains all of the package information
and dependencies
'''
from setuptools import setup,find_packages

setup(
    #name='galah',
    version='0.5.0',
    license='MPL-2.0',
    author='Amanda Buyan',
    author_email='amanda.buyan@csiro.au',
    description="Get counts and information on species from many different atlases",
    long_description="Get counts and information on species from many different atlases",
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'':'src'},
    url='',
    keywords='galah',
    #'tempfile'
    install_requires=[
        'numpy','pandas','requests','urllib3','TIME-python','zip-files','configparser','glob2','bytesbufio','shutils','setuptools','shapely','pytest','unittest2py3k','mkl'
    ],
    include_package_data = True,
    package_data = {
    # If any package contains *.ini files or *.csv files, include them
    '': ['config.ini','node_config.csv','gbif_assertions.csv','gbif_fields.csv'],
    },
)
