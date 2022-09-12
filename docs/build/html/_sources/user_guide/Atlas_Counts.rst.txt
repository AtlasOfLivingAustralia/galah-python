atlas_counts()
================================


This function is for getting the number of occurrence records before you're ready
to download.


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

Say you want to get the total count of one particular species' records within the atlas.  Let's choose
"Vulpes vulpes", or the red fox.  To do this, run

.. prompt::

    import galah
    galah.atlas_counts("Vulpes vulpes")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts(\"Vulpes vulpes\"))"

Filtering Results
-----------------

Now, what if you want to filter the results, i.e. only find entries for the year 2020?  Let's start with one species.  Write

.. prompt::

    import galah
    galah.atlas_counts("Vulpes vulpes",filters="year=2020")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts(\"Vulpes vulpes\",filters=\"year=2020\"))"

Multiple Species
________________

Specifying Multiple Species
---------------------------

If you didn't want to get occurrence records just for the Red Fox, but for multiple species, this is also possible.  To do this, run

.. prompt::

    import galah
    species_array=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"]
    galah.atlas_counts(species_array)

which returns

.. program-output:: python3 -c "import galah; species_array=[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"]; print(galah.atlas_counts(species_array))"

Separating Counts of Multiple Species
-------------------------------------

However, maybe you want to know how many entries correspond with each species, not just the total for all.  To separate the counts out, run

.. prompt::

    import galah
    species_array=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"]
    galah.atlas_counts(species_array,separate=True)

which returns

.. program-output:: python3 -c "import galah; species_array=[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"]; print(galah.atlas_counts(species_array,separate=True))"

Filtering Results for Multiple Species
--------------------------------------

A similar syntax is used with multiple species:

.. prompt::

    import galah
    species_array=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"]
    galah.atlas_counts(species_array,filters="year=2020")

which returns

.. program-output:: python3 -c "import galah; species_array=[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"]; print(galah.atlas_counts(species_array,filters=\"year=2020\"))"

Separating Filtered Results for Multiple Species
------------------------------------------------

These species counts can be separated:

.. prompt::

    import galah
    species_array=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"]
    galah.atlas_counts(species_array,filters="year=2020",separate=True)

which returns

.. program-output:: python3 -c "import galah; species_array=[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"]; print(galah.atlas_counts(species_array,filters=\"year=2020\",separate=True))"
