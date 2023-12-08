atlas_occurrences()
=================================

Amanda has to write something good here.  Add code first.

.. prompt::

    galah.atlas_occurrences(
         taxa=None,
         filters=None,
         test=False,
         verbose=False,
         fields=None,
         assertions=None,
         use_data_profile=False,
         doi=False,**
    )

** is not implemented - will be soon (?)

WARNING: You cannot use ``atlas_occurrences()`` without a taxa name.

Let's start again with the red fox, or "Vulpes vulpes".  To get all occurrence records, type

.. prompt::

    import galah
    galah.atlas_occurrences(taxa="Vulpes vulpes")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_occurrences(\"Vulpes vulpes\"))"
