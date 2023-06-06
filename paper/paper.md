---
title: 'Galah: A Python package for ecologists'
tags:
  - Python
  - ecology
  - species
  - species occurrence
  - atlas
authors:
  - name: Amanda Buyan
    orcid: 0000-0003-3956-3284
    equal-contrib: true
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Martin Westgate
    corresponding: true # (This is how to denote the corresponding author)
    orcid: 0000-0003-0854-2034
    affiliation: "1"
affiliations:
 - name: Atlas of Living Australia, CSIRO, Australia
   index: 1
date: 1 July 2023
bibliography: paper.bib

---

# Summary

Biodiversity is essential for all processes on earth.  Knowing where flora 
and fauna exist is key to understanding the biodiversity, and therefore 
overall health, of an area.  If biodiversity is low, this can indicate an 
ecosystem is on the verge of destruction.  Being able to easily access 
biodiversity data is therefore crucial to researchers, decision makers and 
the general public.  'Living atlases', or a set of organisations that share 
a common codebase and act as nodes of the 
[Global Biodiversity Information Facility (GBIF)](gbif.org), collate and store 
observations of individual life forms using the ‘Darwin Core’ data standard.  
Accessing this data through Python, however, is not straightforward.

`Galah` is an interface to this biodiversity data, designed to get current 
data using API endpoints from the various living atlases.  This data includes 
information such as taxonomic backbones, counts of how many observances of 
your particular species there are, and can be filtered by month, year, and 
type of observation, among many other things.  It also allows you to download 
species records for use in research, as well aspolicy and decision making.

`Galah` was designed to be used by a range of individuals, from students, researchers,
policy and decision makers, to the Python enthusiast curious about what species are
in their backyard.  The combination of uniform data structures, along with the 
ability to query multiple living atlases, will enable exciting scientific discoveries
around the globe.  The source code for `Galah` has been made available on 
[Github](https://github.com/AtlasOfLivingAustralia/galah-python), with the website 
containing all the documentation available at the [Galah homepage](galah.ala.org.au/Python).

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Dax Kellie and Caitlyn Ramsay during the genesis of this project.

# References
