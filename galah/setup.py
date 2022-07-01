'''
This is the setup script for galah.  It contains all of the package information
and dependencies
'''

from setuptools import setup,find_packages

setup(
    name='galah',
    version='0.1',
    license='MIT',
    author='Amanda Buyan','Martin Westgate',
    author_email='amanda.buyan@csiro.au','martin.westgate@csiro.au',
    packages=find_packages('src'),
    package_dir={'':'src'},
    url='',
    keywords='galah',
    install_requires=[
        'scipy','numpy','pandas','requests'
    ]
)
