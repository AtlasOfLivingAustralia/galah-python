.. _Download Data:

Download Data
=============

The ``atlas_`` functions are used to return data from the atlas chosen using ``galah_config()``. They are:

    * ``atlas_counts()``
    * ``atlas_occurrences()``
    * ``atlas_species()``
    * ``atlas_media()``

Record counts
-------------

``galah.atlas_counts()`` provides summary counts on records in the specified atlas, without needing to download all the records.

.. prompt:: python

    >>> galah.galah_config(atlas="Australia")
    >>> galah.atlas_counts()

.. program-output:: python -c "import galah;galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts())"

In addition to ``filters`` arguments, ``galah.atlas_counts()`` has an optional ``group_by`` argument, which provides counts grouped 
by the requested field.

.. prompt:: python

    >>> galah.atlas_counts(group_by="kingdom")

.. program-output:: python -c "import galah;galah.galah_config(atlas=\"Australia\");import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.atlas_counts(group_by=\"kingdom\",expand=False))"

Species lists
-------------

A common use case of atlas data is to identify which species occur in a specified region, time period, 
or taxonomic group. ``galah.atlas_species()`` is similar to search_taxa, in that it returns taxonomic information and 
unique identifiers in a dataframe. It differs in not being able to return information on taxonomic levels other 
than the species; but also in being more flexible by supporting filtering:

.. prompt:: python

    >>> galah.atlas_species(taxa="Rodentia",filters="stateProvince=Northern Territory")

.. program-output:: python -c "import galah;galah.galah_config(atlas=\"Australia\");import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.atlas_species(taxa=\"Rodentia\",filters=\"stateProvince=Northern Territory\"))"


Occurrence data
---------------

To download occurrence data you will need to specify your email in ``galah.galah_config()``. This email must be 
associated with an active account on your chosen atlas. See more information in the config section.

.. prompt:: python

    >>> galah_config(email = "your_email@email.com", atlas = "Australia")

After specifying your email, you can download occurrence records of, for example, Eolophus roseicapilla:

.. prompt:: python

    >>> galah.atlas_occurrences(taxa="Eolophus roseicapilla",filters=["stateProvince=Australian Capital Territory","year>=2010"],fields=["institutionID","basic"])

.. program-output:: python -c "import galah;galah.galah_config(atlas=\"Australia\",email=\"amanda.buyan@csiro.au\");import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\",email=\"amanda.buyan@csiro.au\");print(galah.atlas_occurrences(taxa=\"Eolophus roseicapilla\",filters=[\"stateProvince=Australian Capital Territory\",\"year>=2010\"],fields=[\"institutionID\",\"basic\"]))"

Media metadata
--------------

In addition to text data describing individual occurrences and their attributes, ALA stores images, sounds and videos 
associated with a given record. Metadata on these records can be downloaded using ``galah.atlas_media()`` and the same set of 
filters as the other data download functions.

.. prompt:: python

    >>> galah.atlas_media(taxa="Eolophus roseicapilla",filters=["year=2020","stateProvince=Australian Capital Territory"])    

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\",email=\"amanda.buyan@csiro.au\");print(galah.atlas_media(taxa=\"Eolophus roseicapilla\",filters=[\"year=2020\",\"stateProvince=Australian Capital Territory\"]))"

To actually download the media files to your computer, add the argument ``collect``.  By default, it downloads the data to your
current working directory, but you can specify the folder to download to with the ``path`` argument.


Configuring galah
-----------------

Various aspects of the galah package can be customized.

*Email*

To download occurrence records, you will need to provide an email address registered with the ALA. You can create an account 
`here <https://auth.ala.org.au/userdetails/registration/createAccount>`_. Once an email is registered with the ALA, it should 
be stored in the config:

.. prompt:: python
    
    >>> galah.galah_config(email = "myemail@gmail.com")

*Setting a download reason*

ALA requires that you provide a reason when downloading occurrence data (via the ``galah.atlas_occurrences()`` function). 
The reason is set to 4 (scientific research) by default, but you can change this using ``galah_config()``. See ``galah.show_all(reasons=True)`` 
for valid download reasons.

.. prompt:: python

    >>> galah.galah_config(reason = 5)


Debugging
---------

If things aren’t working as expected, more detail (particularly about web requests) 
can be obtained by setting the ``verbose`` option in many functions.