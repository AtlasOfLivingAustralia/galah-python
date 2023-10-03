Tutorial
=================================

*Note: You will need to register your email address at the atlas you want to download data for, otherwise you will get no data!*

Now that you have successfully installed ``galah-python``, we'll provide a quick introduction on the functions you will mainly be using to get data. If you're looking for a quick reference guide for commands, the `User Guide <../galah_user_guide/index.rst>`_ collates all the available commands with examples.  This tutorial serves as an initial method to get you used to using different commands. 

First, you will need to configure galah.  To do this, run the following:

.. prompt::

    import galah
    galah.galah_config(email="youremail@example.com")

This will not return anything.  No error messages means it is configured correctly.

Now that ``galah`` is configured, we will get counts of records, so you know how many you are downloading.  Let's choose the taxa "Vulpes vulpes", or the red fox.  To get the total number of records in the ALA, type

.. prompt::

    import galah
    galah.atlas_counts(taxa="Vulpes vulpes")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts(taxa=\"Vulpes vulpes\"))"

From here, you can narrow down your query by doing a few things.  Let's first investigate how to apply filters.

For example, if you are only interested in red foxes spotted in Australia in 2020, you can investigate how many records there are by typing

.. prompt::

    import galah
    galah.atlas_counts(taxa="Vulpes vulpes",filters="year=2020")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts(taxa=\"Vulpes vulpes\",filters=\"year=2020\"))"

Now that you have successfully determined the number of records for the red fox, you can download the occurrence records.  To do this, write the following:

.. prompt::

    import galah
    galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2020")

which returns

.. program-output:: python3 -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.atlas_occurrences(taxa=\"Vulpes vulpes\",filters=\"year=2020\"))"

If you only want a few columns of data, rather than the plethora above, use the `fields` option as follows:

.. prompt::

    import galah
    galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2020",fields=["scientificName","decimalLatitude","decimalLongitude"])

which returns

.. program-output:: python3 -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(galah.atlas_occurrences(taxa=\"Vulpes vulpes\",filters=\"year=2020\",fields=[\"scientificName\",\"decimalLatitude\",\"decimalLongitude\"]))"


