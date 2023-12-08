.. _Taxonomic Filtering:

Taxonomic Filtering
===================

*Callum Waite, Shandiya Balasubramanium*

Taxonomic complexity can confound the process of searching, filtering, and downloading records using galah, but there are a few 
ways to ensure records are not missed by using ``[functions]`` in ``galah``.  Let's start by configuring ``galah`` to the ALA.

.. prompt:: python

    >>> import galah
    >>> galah.galah_config(atlas="Australia",email="your-email-here")

``search_taxa()``
-----------------

``search_taxa()`` enables users to look up taxonomic names before downloading data, which allows for 
disambiguating homonyms and checking that the search term matches the taxon name in the ALA . ``search_taxa()`` 
returns the scientific name, authorship, rank, and full classification for the taxon matched to the provided 
search term.

.. prompt:: python

    >>> galah.search_taxa(taxa="Petroica boodang")
    
.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.search_taxa(taxa=\"Petroica boodang\"))"

It can also return taxonomic information for multiple species, including synonyms and Indigneous names.

.. prompt:: python

    >>> # Muscicapa chrysoptera is a synonym for the Flame Robin, Petroica phoenicea
    >>> # Guniibuu is the Yuwaalaraay Indigenous name for the Red-Capped Robin, Petroica goodenovii
    >>> galah.search_taxa(taxa = ["Muscicapa chrysoptera", "Guniibuu"])
    
.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.search_taxa(taxa = [\"Muscicapa chrysoptera\", \"Guniibuu\"]))"

Where homonyms exist, ``search_taxa()`` will prompt users to clarify the search term by providing one or more taxonomic 
ranks using the ``search_taxa()`` argument ``scientific_name``. This example differentiates among the genus Morganella 
in three kingdoms:

.. prompt:: python

    >>> galah.search_taxa(taxa = ["Morganella"])
    
.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.search_taxa(taxa = \"Morganella\"))"
.. prompt:: python

    >>> galah.search_taxa(scientific_name={"kingdom": ["Fungi"],"scientificName": ["Morganella"]})
    
.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.search_taxa(scientific_name={\"kingdom\": [\"Fungi\"],\"scientificName\": [\"Morganella\"]}))"

This disambiguation of the Morganella taxa can then be used by ``atlas_counts``, ``atlas_occurrences``, 
``atlas_species`` or ``atlas_media`` by providing the keyword ``scientific_name`` to any of these functions.

.. prompt:: python

    >>> galah.atlas_counts(scientific_name={"kingdom": ["Fungi"],"scientificName": ["Morganella"]})
    
.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts(scientific_name={\"kingdom\": [\"Fungi\"],\"scientificName\": [\"Morganella\"]}))"
.. prompt:: python

    >>> galah.atlas_occurrences(scientific_name={"kingdom": ["Fungi"],"scientificName": ["Morganella"]})
    
.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\",email=\"amanda.buyan@csiro.au\");print(galah.atlas_occurrences(scientific_name={\"kingdom\": [\"Fungi\"],\"scientificName\": [\"Morganella\"]}))"


``filters=``
------------

``filters=`` subsets records by searching for exact matches to an expression, and may also be used for taxonomic 
filtering.  for example, if we want to search for multiple species of robins in Australia, we can do this for
single or multiple species.  We can also group the multiple species by their species names so we can compare the 
number of records for each robin.

.. prompt:: python

    >>> galah.atlas_counts(taxa="Petroica boodang")
    
.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts(taxa=\"Petroica boodang\"))"

.. prompt:: python

    >>> aus_petroica = ["Petroica boodang", "Petroica goodenovii", 
    ...                 "Petroica phoenicea", "Petroica rosea",
    ...                 "Petroica rodinogaster", "Petroica multicolor"]
    >>> galah.atlas_counts(
    ...     taxa=aus_petroica,
    ...     group_by=["species","vernacularName"]
    ... )
    
.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");aus_petroica = [\"Petroica boodang\", \"Petroica goodenovii\", \"Petroica phoenicea\", \"Petroica rosea\",\"Petroica rodinogaster\",\"Petroica multicolor\"];print(galah.atlas_counts(taxa=aus_petroica,group_by=[\"species\",\"vernacularName\"]))"

This can be useful in searching for paraphyletic or polyphyletic groups.  For example, to get counts of non-chordates:

.. prompt:: python

    >>> non_chordates = galah.atlas_counts(
    ...     filters=["kingdom=Animalia","phylum!=Chordata"],
    ...     group_by=["phylum"],
    ...     expand=False
    ... )
    >>> non_chordates.head()
    
.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts(filters=[\"kingdom=Animalia\",\"phylum!=Chordata\"],group_by=[\"phylum\"],expand=False).head())"

``filters=``, ``search_taxa()``, and taxonomic ranks
------------------------------------------------------

Deciding between using ``filters=`` and ``search_taxa()`` in a query comes down to how a record has been classified, 
and whether or not you have the correct unique name and classification of the taxa of interest.

The ALA has fields for the primary taxonomic ranks (kingdom, phylum, class, order, family, genus, species) and some 
secondary ranks (e.g. subfamily, subgenus), all of which may be used with ``filters=`` and ``search_taxa()``. 
Additionally, there is a field named ``scientificName``, which refers to the lowest taxonomic rank to which a record 
has been identified e.g.

.. prompt:: python

    >>> import numpy as np
    >>> pitta_ranks = galah.atlas_counts(
    ...     taxa="Pitta",
    ...     group_by=["scientificName","taxonRank"]
    ... )
    >>> pitta_ranks = pitta_ranks.loc[pitta_ranks["scientificName"].notnull()]
    >>> pitta_ranks

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);import numpy as np;galah.galah_config(atlas=\"Australia\");pitta_ranks = galah.atlas_counts(taxa=\"Pitta\",group_by=[\"scientificName\",\"taxonRank\"]);print(pitta_ranks.loc[pitta_ranks[\"scientificName\"].notnull()])"

If, for instance, you have the correct species or subspecies name, then searching for matches against the species 
and subspecies fields, respectively, will provide more precise results. This is because the field ``scientificName`` 
may include subgenera. If you’ve used ``search_taxa()`` to get the ALA-matched name of a taxon and only want records 
identified to a particular level of classification, searching for matches against ``scientificName`` is recommended.

Paraphyletic or polyphyletic groups may contain taxa identified to different taxonomic levels. In this case, it is 
simpler to use ``search_taxa()``. In the example below, ``search_taxa()`` matches terms to one genus, three species, 
and two subspecies. This can then be used in ``atlas_counts()`` to get counts for each scientific name.

.. prompt:: python

    >>> tas_endemic = ["Sarcophilus", # Tasmanian Devil
    ...                 "Bettongia gaimardi", # Tasmanian Bettong
    ...                 "Melanodryas vittata", # Dusky Robin
    ...                 "Platycercus caledonicus",# Green Rosella
    ...                 "Aquila audax fleayi", # Tasmanian Wedge-Tailed Eagle
    ...                 "Tyto novaehollandiae castanops" # Tasmanian Masked Owl
    ...               ]
    >>> galah.search_taxa(taxa=tas_endemic)

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");tas_endemic = [\"Sarcophilus\",\"Bettongia gaimardi\",\"Melanodryas vittata\",\"Platycercus caledonicus\",\"Aquila audax fleayi\",\"Tyto novaehollandiae castanops\"];print(galah.search_taxa(taxa=tas_endemic))"

.. prompt:: python

    >>> galah.atlas_counts(
    ...     taxa=tas_endemic,
    ...     group_by=["scientificName"],
    ...     expand=False
    ... )

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");tas_endemic = [\"Sarcophilus\",\"Bettongia gaimardi\",\"Melanodryas vittata\",\"Platycercus caledonicus\",\"Aquila audax fleayi\",\"Tyto novaehollandiae castanops\"];print(galah.atlas_counts(taxa=tas_endemic,group_by=[\"scientificName\"],expand=False))"