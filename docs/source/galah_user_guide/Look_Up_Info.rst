Look Up Information
===================

There are two simplified functions to look up information: 

    * ``galah.show_all()``
    * ``galah.search_all()``

These are individual functions that are able to return all types of information in one place, rather than using specific 
sub-functions to look up information.

For example, to show all available Living Atlases supported:

.. prompt:: python

    >>> galah.show_all(atlases=True)

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.show_all(atlases=True))"


To search for a specific available Living Atlas:

.. prompt:: python

    >>> galah.search_all(atlases="Spain")

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.search_all(atlases=\"Spain\"))"

To show all fields:

.. prompt:: python

    >>> galah.show_all(fields=True)

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.show_all(fields=True))"

And to search for a specific field:

.. prompt:: python

    >>> galah.search_all(fields="Australian States",column_name="description")

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.search_all(fields=\"Australian States\",column_name=\"description\"))"



Here is a list of information types that can be used with ``galah.show_all()`` and ``galah.search_all()``:

.. table:: Information for ``galah.show_all()`` and ``galah.search_all()``
    :widths: 30 100

    +------------------------+-----------------------------------------------------------------------------+
    | **Information type**   | **Description**                                                             |
    +========================+=============================================================================+
    | *Configuration*        |                                                                             |
    +------------------------+-----------------------------------------------------------------------------+
    | ``atlases``            | Show what living atlases are available                                      |
    +------------------------+-----------------------------------------------------------------------------+
    | ``apis``               | Show what APIs & functions are available for each atlas                     |
    +------------------------+-----------------------------------------------------------------------------+
    | ``reasons``            | Show what values are acceptable as ‘download reasons’ for a specified atlas |
    +------------------------+-----------------------------------------------------------------------------+
    | *Taxonomy*             |                                                                             |
    +------------------------+-----------------------------------------------------------------------------+
    | ``identifiers``        | Take a universal identifier and return taxonomic information                |
    +------------------------+-----------------------------------------------------------------------------+
    | ``ranks``              | Show valid taxonomic ranks (e.g. Kingdom, Class, Order, etc.)               |
    +------------------------+-----------------------------------------------------------------------------+
    | *Filters*              |                                                                             |
    +------------------------+-----------------------------------------------------------------------------+
    | ``fields``             | Show fields that are stored in an atlas                                     |
    +------------------------+-----------------------------------------------------------------------------+
    | ``assertions``         | Show results of data quality checks run by each atlas                       |
    +------------------------+-----------------------------------------------------------------------------+
    | *Group filters*        |                                                                             |
    +------------------------+-----------------------------------------------------------------------------+
    | ``profiles``           | Show what data quality profiles are available                               | 
    +------------------------+-----------------------------------------------------------------------------+
    | ``lists``              | Show what species lists are available                                       |
    +------------------------+-----------------------------------------------------------------------------+
    | *Data providers*       |                                                                             |
    +------------------------+-----------------------------------------------------------------------------+
    | ``providers``          | Show which institutions have provided data                                  |
    +------------------------+-----------------------------------------------------------------------------+
    | ``collections``        | Show the specific collections within those institutions                     |	
    +------------------------+-----------------------------------------------------------------------------+
    | ``datasets``           | Shows all the data groupings within those collections                       |
    +------------------------+-----------------------------------------------------------------------------+

``_values`` functions
---------------------

Sifting through the output of ``galah.show_all(fields=True)`` to find a specific field can be inefficient. 
Instead, we might wish to use search_fields to look for specific fields that match a search, and get 
their possible values to filter our results. 


If we want to know what kinds of fields describe the basis of how an occurrence was recorded, you can 
search for the keyword "basis" using ``galah.search_all()``:

.. prompt:: python
    
    >>> galah.search_all(fields="basis")

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.search_all(fields=\"basis\"))"

Once a desired field is found, you can use show_values to understand the information 
contained within that field, e.g.

.. prompt:: python

    >>> galah.show_values(field="basisOfRecord")

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.show_values(field=\"basisOfRecord\"))"

You can even narrow down your search by searching for matching values:

.. prompt:: python

    >>>  galah.search_values(field="basisOfRecord",value="SPECIMEN")

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.search_values(field=\"basisOfRecord\",value=\"SPECIMEN\"))"

This provides the information you need to pass meaningful queries to galah_filter.

.. prompt:: python

    >>> galah.atlas_counts(filters="basisOfRecord=LIVING_SPECIMEN")

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts(filters=\"basisOfRecord=LIVING_SPECIMEN\"))"