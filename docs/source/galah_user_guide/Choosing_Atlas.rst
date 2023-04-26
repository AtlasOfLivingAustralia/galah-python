Choosing an Atlas
=================

The GBIF network consists of a series of ‘node’ organisations who collate biodiversity 
data from their own countries, with GBIF acting as an umbrella organisation to store data from all 
nodes. Several nodes have their own APIs, often built from the ‘living atlas’ codebase developed 
by the ALA. 

At present, galah supports the following functions and atlases:

    * Australia
    * Brazil
    * Spain

Set Organisation
----------------

Set which atlas you want to use by changing the atlas argument in ``galah.galah_config()``. The atlas argument 
can accept a  a region to select a given atlas, all of which are available 
via ``galah.show_all(atlases=True)``. Once a value is provided, it will automatically update galah’s server 
configuration to your selected atlas. The default atlas is Australia.

If you intend to download records, you may need to register a user profile with the relevant atlas first. 

.. prompt:: python

    >>> import galah
    >>> galah.galah_config(atlas="Spain", email="your-email-here")


Look up Information
-------------------

You can use the same look-up functions to find useful information about the Atlas you have set. 
Available information may vary for each Living Atlas.

.. prompt:: python

    >>> galah.galah_config(atlas="Australia")

.. prompt:: python

    >>> galah.show_all(datasets=True)

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.show_all(datasets=True))"

.. prompt:: python

    >>> galah.show_all(fields=True)

.. program-output:: python3 -c "import galah;galah.galah_config(atlas=\"Australia\");import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.show_all(fields=True))"

.. prompt:: python

    >>> galah.search_all(datasets="year")

.. program-output:: python3 -c "import galah;galah.galah_config(atlas=\"Australia\");import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.search_all(datasets=\"year\"))"

.. prompt:: python

    >>> galah.search_taxa(taxa="Heleioporus")

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.search_taxa(taxa=\"Heleioporus\"))"


Download data
-------------

You can build queries as you normally would in galah. For taxonomic queries, use ``galah.search_taxa()`` to 
make sure your searches are returning the correct taxonomic data.

.. prompt:: python

    >>> galah.galah_config(atlas="Australia")

.. prompt:: python

    >>> # Returns no data due to misspelling
    >>> galah.search_taxa(taxa="vlps")

.. program-output:: python3 -c "import galah;print(galah.search_taxa(taxa=\"vlps\"))"

.. prompt:: python

    >>> # Returns data
    >>> galah.search_taxa(taxa="Vulpes vulpes")

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.search_taxa(taxa=\"Vulpes vulpes\"))"

.. prompt:: python

    >>> galah.atlas_counts(taxa="Vulpes vulpes", filters="year>2010")

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.atlas_counts(taxa=\"Vulpes vulpes\", filters=\"year>2010\"))"

Download species occurrence records from other atlases with ``galah.atlas_occurrences()``

.. prompt:: python

    >>> galah.atlas_occurrences(taxa="Vulpes vulpes", filters="year>2010", fields=["taxon_name", "year"])

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\",email=\"amanda.buyan@csiro.au\");print(galah.atlas_occurrences(taxa=\"Vulpes vulpes\", filters=\"year>2010\", fields=[\"taxon_name\", \"year\"]))"


Complex queries with multiple Atlases
-------------------------------------

It is also possible to create more complex queries that return data from multiple Living Atlases. 
As an example, setting atlases within a loop with galah_config() allows us to 
return the total 0number of species records in each Living Atlas in one table.

.. prompt:: python

    >>> import galah
    >>> import pandas as pd
    >>> atlases = ["Australia","Brazil","Spain"]
    >>> counts_dict = {"Atlas": [], "Total Records": []}
    >>> for atlas in atlases:
    >>>     galah.galah_config(atlas=atlas)
    >>>     counts_dict["Atlas"].append(atlas)
    >>>     counts_dict["Total Records"].append(galah.atlas_counts()["totalRecords"][0])
    >>> pd.DataFrame(counts_dict)

.. program-output:: python galah_user_guide/table.py 