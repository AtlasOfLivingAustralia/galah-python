Configuring Galah
=================


To configure your Galah environment, you can specify a number of variables.  To see what options are preset, run the
following command:

.. prompt:: python

    import galah
    galah.galah_config()

.. program-output:: python -c "import galah;print(galah.galah_config())"

To set any of these options (for example, email), run the following command:

.. prompt:: python

    galah.galah_config(email="myemail@example.com")
    galah.galah_config()

.. program-output:: python -c "import galah;galah.galah_config(email=\"myemail@example.com\");print(galah.galah_config())"

.. program-output:: python -c "import galah;galah.galah_config(email=\"amanda.buyan@csiro.au\")"