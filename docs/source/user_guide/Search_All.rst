search_all()
=================================

.. prompt::

    galah.search_all(
         assertions=None,
         atlases=None,
         apis=None,
         collections=None,
         datasets=None,
         fields=None,
         licences=None,
         lists=None,
         profiles=None,
         providers=None,
         reasons=None,
         ranks=None,
         column_name=None
    )

This is to find all the possible values of the field you want to query/filter by.  To use, type

.. prompt::

    import galah
    galah.search_all(assertions="AMBIGUOUS_COLLECTION")

which returns

.. program-output:: python3 -c "import galah;print(galah.search_all(\"AMBIGUOUS_COLLECTION\"))"

If you want to search a different column other than the first one (the default), you can specify ``column_name`` by the following:

.. prompt::

    import galah
    galah.search_all(assertions="collection",column_name="description")

which returns

.. program-output:: python3 -c "import galah;print(galah.search_all(assertions=\"collection\",column_name=\"description\"))"
