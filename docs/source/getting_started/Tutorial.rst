Tutorial
=================================

Now that you have successfully installed ``galah``, we'll provide a quick introduction on the functions you will mainly be using to get data. If you're looking for a quick reference guide for commands, the User Guide (Amanda to add hyperlnk) collates all the available commands wih example.  This tutorial serves as an initial method to get you used to using different commands. 

First, you will need to configure galah.  To do this, run the following:

.. prompt::

    import galah
    galah.galah_config(email="youremail@example.com")

This will not return anything.  No error messages means it is configured correctly.

Now that ``galah`` is configured, we will get counts of records, so you know how many you are downloading.  Let's choose the species "Vulpes vulpes", or the red fox.  To get the total number of records in the ALA, type

.. prompt::

    import galah
    galah.atlas_counts(species="Vulpes vulpes")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts(species=\"Vulpes vulpes\"))"

From here, you can narrow down your query by doing a few things.  Let's first investigate how to apply filters.

For example, if you are only interested in red foxes spotted in Australia in 2020, you can investigate how many records there are by typing

.. prompt::

    import galah
    galah.atlas_counts(species="Vulpes vulpes",filters="year=2020")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts(species=\"Vulpes vulpes\",filters=\"year=2020\"))"

Now that you have successfully determined the number of records for the red fox, you can download the occurrence records.  To do this, write the following:

.. prompt::

    import galah
    galah.atlas_occurrences(species="Vulpes vulpes",filters="year=2020")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_occurrences(species=\"Vulpes vulpes\",filters=\"year=2020\"))"


