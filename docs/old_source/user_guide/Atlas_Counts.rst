atlas_counts()
================================

This function is for getting the number of occurrence records before you're ready
to download.

.. prompt::

    galah.atlas_counts(
         taxa=None,
         filters=None,
         group_by=None,
         expand=True,
         separate=False,
         verbose=False,
         use_data_profile=False,
    )

Total Occurrences in the ALA
____________________________

To know how many total occurrences records are in the Atlas (and to test the function), type

.. prompt::

    import galah
    galah.atlas_counts()

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts())"

Single Species
______________


Specifying a Species
--------------------

Say you want to get the total count of one particular taxa' records within the atlas.  Let's choose
"Vulpes vulpes", or the red fox.  To do this, run

.. prompt::

    import galah
    galah.atlas_counts("Vulpes vulpes")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts(\"Vulpes vulpes\"))"

Filtering Results
-----------------

Now, what if you want to filter the results, i.e. only find entries for the year 2020?  Let's start with one taxa.  Write

.. prompt::

    import galah
    galah.atlas_counts("Vulpes vulpes",filters="year=2020")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts(\"Vulpes vulpes\",filters=\"year=2020\"))"

Multiple Species
________________

Specifying Multiple Species
---------------------------

If you didn't want to get occurrence records just for the Red Fox, but for multiple taxa, this is also possible.  To do this, run

.. prompt::

    import galah
    taxa_array=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"]
    galah.atlas_counts(taxa_array)

which returns

.. program-output:: python3 -c "import galah; taxa_array=[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"]; print(galah.atlas_counts(taxa_array))"

Separating Counts of Multiple Species
-------------------------------------

However, maybe you want to know how many entries correspond with each taxa, not just the total for all.  To separate the counts out, run

.. prompt::

    import galah
    taxa_array=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"]
    galah.atlas_counts(taxa_array,separate=True)

which returns

.. program-output:: python3 -c "import galah; taxa_array=[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"]; print(galah.atlas_counts(taxa_array,separate=True))"

Filtering Results for Multiple Species
--------------------------------------

A similar syntax is used with multiple taxa:

.. prompt::

    import galah
    taxa_array=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"]
    galah.atlas_counts(taxa_array,filters="year=2020")

which returns

.. program-output:: python3 -c "import galah; taxa_array=[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"]; print(galah.atlas_counts(taxa_array,filters=\"year=2020\"))"

Separating Filtered Results for Multiple Species
------------------------------------------------

These taxa counts can be separated:

.. prompt::

    import galah
    taxa_array=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"]
    galah.atlas_counts(taxa_array,filters="year=2020",separate=True)

which returns

.. program-output:: python3 -c "import galah; taxa_array=[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"]; print(galah.atlas_counts(taxa_array,filters=\"year=2020\",separate=True))"
