atlas_media()
================================

This function is for getting the number of occurrence records before you're ready
to download.

.. prompt::

    galah.atlas_media(
         taxa=None,
         filters=None
         fields=None,
         verbose=False,
         multimedia=None,
         use_data_profile=False,
         **collect=False,
         **path=None
    )

** has been implemented but caching has not yet

Search for media files on a species
___________________________________

To know how many total occurrences records are in the Atlas (and to test the function), type

.. prompt::

    import galah
    galah.atlas_media(taxa="Ornithorhynchus anatinus")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_media(taxa=\"Ornithorhynchus anatinus\"))"

Since this is a lot of records, you may want to filter down the results, for example by year or by the longitude (though there are other filters you may wish to use; the ``show_all()`` and ``search_all()`` pages can help you find other filters).

Once you have the filters chosen, you would write them as so 

.. prompt::

    import galah
    filters=["year=2020","decimalLongitude>153.0"]
    galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=filters)

which returns

.. program-output:: python3 -c "import galah; filters=[\"year=2020\",\"decimalLongitude>153.0\"];print(galah.atlas_media(taxa=\"Ornithorhynchus anatinus\",filters=filters))"

If you only want images, rather than other forms of multimedia, you can specify this by setting the ``multimedia="images"`` variable, like so:

.. prompt::

    import galah
    filters=["year=2020","decimalLongitude>153.0"]
    galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=filters,multimedia="images")

which returns

.. program-output:: python3 -c "import galah; filters=[\"year=2020\",\"decimalLongitude>153.0\"];print(galah.atlas_media(taxa=\"Ornithorhynchus anatinus\",filters=filters,multimedia=\"images\"))"

-----------------------------------
Need to implement the section below
-----------------------------------

To download the data, you have to set the variable ``collect=True``.  If you don't specify a directory to download the images into, they will be downloaded into a cache directory.  However, if you want to specify the directory, you set ``path=PATH/TO/FILE``.  If the path doesn't exist, it will make the directory so it has a place to download the directory.  What the command to download images will look like is

.. prompt::

    import galah
    filters=["year=2020","decimalLongitude>153.0"]
    galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=filters,multimedia="images",collect=True,path=\"images-orn\")
