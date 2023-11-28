# galah <a href="https://galah.ala.org.au/Python/"><img src="docs/source/_static/logo/logo.png" align="right" style="margin: 0px 10px 0px 10px;" alt="" height="138"/></a>

<!-- badges: start -->

[![pypi](https://img.shields.io/pypi/v/galah-python.svg)](https://pypi.org/project/galah-python/)

<!-- badges: end -->

## Overview

`galah-python` is a Python interface to biodiversity data hosted by the [Global
Biodiversity Information Facility](https://www.gbif.org) (GBIF) and
those members of the GBIF node network that maintain their own APIs
(i.e. the [‘living atlases’](https://living-atlases.gbif.org)). These
organisations collate and store observations of individual life forms,
using the [‘Darwin Core’](https://dwc.tdwg.org) data standard. `galah-python`
was built and is maintained by the [Science & Decision Support
Team](https://labs.ala.org.au) at the [Atlas of Living
Australia](https://www.ala.org.au) (ALA).

`galah-python` enables users to locate and download species occurrence records
(observations, specimens, eDNA records, etc.), taxonomic information, or
associated media such as images or sounds, and to restrict their queries
to particular taxa or locations. Users can specify which columns are
returned by a query, or restrict their results to occurrences that meet
particular data-quality criteria. All functions return a `Pandas DataFrame` as
their standard format.

The package is named for the bird of the same name (*Eolophus
roseicapilla*), a widely-distributed endemic Australian species. The
logo was designed by [Ian Brennan](https://www.iangbrennan.org/).

If you have any comments, questions or suggestions, please [contact
us](mailto:support@ala.org.au).

## Getting started

- The [Getting Started Tutorial](https://galah.ala.org.au/Python/getting_started/Tutorial.html)
  provides an introduction to the core package functions.
- For an outline of the package structure, and a list of all the
  available functions, view the [API docs
  page](https://galah.ala.org.au/Python/apidocs/galah.html).

## Installation

See the [installation docs](https://galah.ala.org.au/Python/getting_started/Installation.html) for full details.  

Install the `galah-python` package

```bash
$ pip install galah-python
```

`galah-python` depends on the following packages:

  *  `numpy`
  *  `pandas`
  *  `requests`
  *  `urllib3`
  *  `TIME-python`
  *  `zip-files`
  *  `configparser`
  *  `glob2`
  *  `shutils`
  *  `setuptools`
  *  `shapely`
  *  `pytest`
  *  `unittest2py3k`

## Usage

Visit the [galah package website](galah.ala.org.au/Python) for documentation and vignettes to get started.

## License

`galah-python` was created by Amanda Buyan, with contributions by Caitlin Ramsay, Dax Kellie and Martin Westgate under a MPL-2.0 license.

## Credits

`galah-python` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
