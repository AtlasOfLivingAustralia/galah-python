Tutorial
=================================

Now that you have successfully installed ``galah``, we'll provide a quick introduction on the functions you will mainly be using to get data.

First, we will get counts of records, so you know how many you are downloading.  To do this, type

.. prompt::

    import galah
    galah.atlas_counts()

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts())"
