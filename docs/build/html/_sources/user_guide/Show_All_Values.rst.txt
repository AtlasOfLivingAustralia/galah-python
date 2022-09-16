show_all_values()
=================================

.. prompt::

    galah.show_all_values(
         field
    )

This is to find all the possible values of the field you want to query/filter by.  To use, type

.. prompt::

    import galah
    galah.show_all_values("basisOfRecord")

which returns

.. program-output:: python3 -c "import galah;print(galah.show_all_values(\"basisOfRecord\"))"
