Introduction
=================================

galah is a Python interface to biodiversity data hosted by the Atlas of Living Australia (`ALA <https://www.ala.org.au/>`). It is based off of the R package of the same name. With this package you can locate and download:

- Species occurrence records (observations, specimens, eDNA records, etc.)

- Taxonomic Information

- Media, such as image or sounds

In addition, users can:

- Restrict their queries to particular taxa or locations

- Specify which columns are returned by a query

- Restrict their results to occurrences that meet particular data-quality criteria

All functions return a galah dataframe as their standard format.

The ALA is an aggregator of biodiversity data, focussed primarily on observations of individual life forms. Like the Global Biodiversity Information Facility (`GBIF <https://www.gbif.org/>`_), the basic unit of data at ALA is an occurrence record (what species is found where, and when), based on the `‘Darwin Core’ <https://dwc.tdwg.org/>`_ data standard.

The galah package is named for the bird of the same name (Eolophus roseicapilla), a widely-distributed endemic Australian species. The logo was designed by Ian Brennan.
