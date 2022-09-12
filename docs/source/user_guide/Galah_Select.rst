galah_select()
=================================

This function is mainly used in ``atlas_occurrences()``.  It is meant to take selections (these can be found from the ``show_all_values()`` page) from occurrence records to get, such as latitude and longitude.  How it works is:

.. prompt::

    import galah
    galah.galah_select(selectionList=['decimalLatitude', 'decimalLongitude'])

which returns

.. program-output:: python3 -c "import galah; print(galah.galah_select(selectionList=[\"decimalLatitude\", \"decimalLongitude\"]))"
