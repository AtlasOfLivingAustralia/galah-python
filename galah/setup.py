'''
This is the setup script for galah.  It contains all of the package information
and dependencies
'''

from setuptools import setup,find_packages

setup(
    name='galah',
    version='0.1.0',
    license='MIT',
    author='Amanda Buyan',
    author_email='amanda.buyan@csiro.au',
    packages=find_packages('src'),
    package_dir={'':'src'},
    url='',
    keywords='galah',
    #'tempfile'
    install_requires=[
        'numpy','pandas','requests','urllib3','TIME-python','zip-files','configparser','glob2','bytesbufio','shutils',
    ],
    include_package_data = True,
    package_data = {
    # If any package contains *.ini files or *.csv files, include them
    '': ['config.ini','node_config.csv'],
    },
)
