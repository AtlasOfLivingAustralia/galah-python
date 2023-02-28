Narrow Results
==============

Each occurrence record contains taxonomic information and information about the observation itself, like 
its location and the date of observation. These pieces of information are recorded and categorised into 
respective fields. When you import data using galah, columns of the resulting tibble correspond to these 
fields.

Data fields are important because they provide a means to manipulate queries to return only the 
information that you need, and no more. Consequently, much of the architecture of galah has been designed 
to make narrowing as simple as possible. These arguments include:

* taxa
* filters
* select
* group_by
* down_to

taxa
----

Perhaps unsurprisingly, ``galah.search_taxa()`` searches for taxonomic information. It uses fuzzy matching 
to work a lot like the search bar on the Atlas of Living Australia website, and you can use it to search for 
taxa by their scientific name. Finding your desired taxon with ``galah.search_taxa()`` is an important step 
to using this taxonomic information to download data with galah.

For example, to search for reptiles, we first need to identify whether we have the correct query:

.. prompt::

    import galah
    galah.search_taxa(taxa="Reptilia")

Once we know that our search matches the correct taxon or taxa, we can use it as an argument to narrow the 
results of our queries:

.. prompt::

    galah.atlas_counts(taxa="Reptilia")

If you’re using an international atlas, ``galah.search_taxa()`` will automatically switch to using the local name-matching 
service. For example, Portugal uses the GBIF taxonomic backbone, but integrates seamlessly with our standard 
workflow.

.. prompt::

    galah.galah_config(atlas="Portugal")

.. prompt::

    galah.atlas_counts(taxa="Bufo", group_by="species")


filters
-------

Perhaps the most important argument in galah is ``filters``, which is used to filter the rows of queries:

.. prompt::

    # Get total record count since 2000
    galah.atlas_counts(filters="year>2000")

.. prompt::

    # Get total record count for iNaturalist in 2021
    galah.atlas_counts(filters="[dataResourceName='iNaturalist Australia',year=2021]")

To find available fields and corresponding valid values, use the field lookup functions 
``galah.show_all()``, ``galah.search_all()`` & ``show_values()``.

Finally, a special case of ``filters`` is to make more complex taxonomic queries than are possible using ``galah.search_taxa``. 
By using the ``taxonConceptID`` field, it is possible to build queries that exclude certain taxa, for example. This can 
be useful for paraphyletic concepts such as invertebrates:

**Amanda to check how to do this**

apply_profile
-------------

When working with the ALA, a notable feature is the ability to specify a profile to remove records that are suspect in some way.
Profiles are groups of data quality filters.

.. prompt::

    galah.galah_config(use_data_profile="ALA")
    galah.atlas_counts(filter="year>2000")

To see a full list of data quality profiles, use ``galah.show_all(profiles=True)``.