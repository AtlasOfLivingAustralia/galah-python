galah_filter()
=================================

Arguments for ``galah_filter()`` are:

.. prompt::

    galah.galah_filter(
         filters,
         profile=None,
         ifgroupby=False,
    )

This function is mainly used in ``atlas_counts()`` and ``atlas_occurrences()``.  It converts a specified filter to a URL-friendly syntax.  An example of its output is below.

.. prompt::

    import galah
    galah.galah_filter("year=2020")

which returns

.. program-output:: python3 -c "import galah; print(galah.galah_filter(\"year=2020\"))"
