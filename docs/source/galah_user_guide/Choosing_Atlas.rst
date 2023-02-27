Choosing an Atlas
=================

The GBIF network consists of a series of ‘node’ organisations who collate biodiversity 
data from their own countries, with GBIF acting as an umbrella organisation to store data from all 
nodes. Several nodes have their own APIs, often built from the ‘living atlas’ codebase developed 
by the ALA. 

At present, galah supports the following functions and atlases:

    * Australia
    * Spain
    * Brazil

Set Organisation
Set which atlas you want to use by changing the atlas argument in ``galah_config()``. The atlas argument 
can accept a full name, an acronym, or a region to select a given atlas, all of which are available 
via ``galah.show_all(atlases=True)``. Once a value is provided, it will automatically update galah’s server 
configuration to your selected atlas. The default atlas is Australia.

If you intend to download records, you may need to register a user profile with the relevant atlas first. 

.. prompt::

    import galah
    galah.galah_config(atlas="Spain", email="your-email-here")


Look up Information
-------------------

You can use the same look-up functions to find useful information about the Atlas you have set. 
Available information may vary for each Living Atlas.

.. prompt::

    galah.galah_config(atlas="Guatemala")

.. prompt::

    galah.show_all(datasets=True)

.. prompt::

    galah.show_all(fields=True)

.. prompt::

    galah.search_all(datasets="year")

.. prompt::

    galah.search_taxa(taxa="lagomorpha")


Download data
-------------

You can build queries as you normally would in galah. For taxonomic queries, use ``galah.search_taxa()`` to 
make sure your searches are returning the correct taxonomic data.

.. prompt::

    galah.galah_config(atlas="United Kingdom")

.. prompt::

    # Returns no data due to misspelling
    galah.search_taxa(taxa="vlps")

.. prompt::

    # Returns data
    galah.search_taxa(taxa="vulpes")

.. prompt::

    galah.atlas_counts(taxa="vulpes", filters="year>2010")

Download species occurrence records from other atlases with ``galah.atlas_occurrences()``

.. prompt::

    galah.atlas_occurrences(taxa="lagomorpha", filters="year<=1980", select="taxon_name, year")


Complex queries with multiple Atlases
-------------------------------------

It is also possible to create more complex queries that return data from multiple Living Atlases. 
As an example, setting atlases within a loop with galah_config() and purrr::map() allows us to 
return the total number of species records in each Living Atlas in one table.

Amanda to do this part and make table with counts from all atlases