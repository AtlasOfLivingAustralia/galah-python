Tutorial
=================================

*Note: You will need to register your email address at the atlas you want to download data for, otherwise you will get no data!*

Now that you have successfully installed ``galah-python``, we'll provide a quick introduction on the functions you will 
mainly be using to get data. If you're looking for a quick reference guide for commands, the 
`User Guide <../galah_user_guide/index.rst>`_ collates all the available commands with examples.  
This tutorial serves as an initial method to get you used to using different commands. 

Configuring ``galah``
--------------------------

First, you will need to set some stored parameters to get full use out of the ``galah`` package.  There are two 
key parameters that you will need to set, especially to get occurrences: ``atlas`` and ``email``.  

**Choosing an Atlas**

First, you will need to choose an atlas to get information from.  If you're not sure what atlases ``galah-python`` 
has on offer, run the command

.. prompt:: python

    >> import galah
    >> galah.show_all(atlases=True)

and a list like this will appear:

.. program-output:: python -c "import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);import galah;galah.show_all(atlases=True)"

To choose an atlas, select the region that the atlas represents.  By default, the atlas is set to ``Australia``, which is
what we will sue for this example.  However, for those interested in the other atlases on offer, say the Brazilian atlas,
type

.. prompt:: python

    >>> galah.galah_config(atlas="Brazil")

**Storing Your Email**

To download data from the atlases, you will need a registered email address.  For the ALA, go to ``https://auth.ala.org.au/userdetails/registration/createAccount``.
Once you have registered your email, you can store it in ``galah`` like so:

.. prompt::

    >>> import galah
    >>> galah.galah_config(email="youremail@example.com")

.. program-output:: python -c "import galah;galah.galah_config(email=\"youremail@example.com\")"

This will not return anything.  No error messages means it is configured correctly.  To see what your configuation settings 
are, type

.. prompt::

    >>> galah.galah_config()

.. program-output:: python -c "import galah;galah.galah_config()"

Building queries
-------------------------

Now that ``galah`` is configured, we will get counts of records, so you know how many you are downloading.  To see how 
many records are currently in the ALA, type

.. prompt:: python

    >>> galah.atlas_counts()

.. program-output:: python -c "import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);import galah;galah.galah_config(email=\"ala4r@ala.org.au\");galah.atlas_counts()"

If you are not interested in a specific species, but in the number of records in the atlas from the year 2020 onwards, you can
add this to the ``filters`` argument of ``atlas_counts()``.

.. prompt:: python

    >>> galah.atlas_counts(filters="year>=2020")

.. program-output:: python -c "import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);import galah;galah.atlas_counts(filters=\"year>=2020\")"

If you are wondering how the number of records for all species in the ALA changed over each year from 2020 onwards, you can
tell ``galah`` to group your results by year, to get yearly counts.

.. prompt:: python

    >>> galah.atlas_counts(filters="year>=2020",group_by="year")

.. program-output:: python -c "import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);import galah;galah.atlas_counts(filters=\"year>=2020\",group_by=\"year\")"

To narrow down your search by a specific species, you can use the ``search_taxa()`` function to check whether or not the
taxonomic information for the species you are wanting to search.  For this example, lLet's choose the taxa *Vulpes vulpes*, 
or the red fox.  

.. prompt:: python

    >>> galah.search_taxa(taxa="Vulpes vulpes")

.. program-output:: python -c "import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);import galah;galah.search_taxa(taxa=\"Vulpes vulpes\")"

Now that we can see we indeed have the red fox, we can see how many records the ALA has of the red fox.  

.. prompt::

    >>> import galah
    >>> galah.atlas_counts(taxa="Vulpes vulpes")

.. program-output:: python -c "import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);import galah;galah.atlas_counts(taxa=\"Vulpes vulpes\")"

Now, we can put our ``filters`` query together with our red fox query, to see how many occurrences of red foxes in the ALA
were seen each year from 2020 onwards.

.. prompt::

    >>> import galah
    >>> galah.atlas_counts(taxa="Vulpes vulpes",filters="year>=2020",group_by="year")

.. program-output:: python -c "import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);import galah;galah.atlas_counts(taxa=\"Vulpes vulpes\",filters=\"year>=2020\",group_by=\"year\")"


Downloading records
-------------------------

Now that we know the number of red fox occurrences in each year starting with 2020, we will now download these records.  
To do this, we will take the query from above and change the function name from ``atlas_counts()`` to ``atlas_occurrences()``.

.. prompt::

    >>> import galah
    >>> galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year>=2020")

.. program-output:: python -c "import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);import galah;galah.atlas_occurrences(taxa=\"Vulpes vulpes\",filters=\"year>=2020\")"

If you are only interested in the scientific name, as well as latitude and longitude, use the ``fields`` option as follows:

.. prompt::

    import galah
    galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year>=2020",fields=["scientificName","decimalLatitude","decimalLongitude"])

.. program-output:: python3 -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.atlas_occurrences(taxa=\"Vulpes vulpes\",filters=\"year>=2020\",fields=[\"scientificName\",\"decimalLatitude\",\"decimalLongitude\"]))"

Check out other vignettes and the API docs for more information on how to use each of these functions, as well as to 
learn more about searching for information on how to filter your data.
