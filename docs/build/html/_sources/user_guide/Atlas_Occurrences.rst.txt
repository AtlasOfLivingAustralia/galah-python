atlas_occurrences()
=================================

Amanda has to write something good here.  Add code first.

WARNING: You cannot use ``atlas_occurrences()`` without a species name.

Let's start again with the red fox, or "Vulpes vulpes".  To get all occurrence records, type

.. prompt::

    import galah
    galah.atlas_occurrences(species="Vulpes vulpes")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_occurrences(\"Vulpes vulpes\"))"
