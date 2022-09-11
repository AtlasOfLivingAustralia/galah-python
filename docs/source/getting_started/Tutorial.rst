Tutorial
=================================

Now that you have successfully installed ``galah``, we'll provide a quick introduction on the functions you will mainly be using to get data. If you're looking for a quick reference guide for commands, the User Guide (Amanda to add hyperlnk) collates all the available commands wih example.  This tutorial serves as an initial method to get you used to using different commands. 

First, you will need to configure galah.  To do this, run the following:

.. prompt::

    import galah
    galah.galah_config(email="youremail@example.com")

This will not return anything.  No error messages means it is configured correctly.

Now that ``galah`` is configured, we will get counts of records, so you know how many you are downloading.  To do this, type

.. prompt::

    import galah
    galah.atlas_counts()

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_counts())"
