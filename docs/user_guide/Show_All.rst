show_all()
=================================

This command is to get all of the fields you can group or filter by, and takes no arguments.  

.. prompt::

    galah.show_all(
         assertions=False,
         atlases=False,
         apis=False,
         collections=False,
         datasets=False,
         fields=False,
         licences=False,
         lists=False,
         profiles=False,
         providers=False,
         ranks=False,
         reasons=False,
    )

To use the ``show_all()``, set one or more of the above fields to ``True``.  

An example of this is:

.. prompt::

    import galah
    galah.show_all(assertions=True)

which returns

.. program-output:: python3 -c "import galah; print(galah.show_all(assertions=True))"
