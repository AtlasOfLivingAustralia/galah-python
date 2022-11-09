atlas_species()
=================================

Arguments for ``atlas_species()`` are:

.. prompt::

    galah.atlas_species(
         taxa=None,
         verbose=False,
    )

This function is mainly used to determine the taxonomy of a particular genus.  An example of its output is below.

.. prompt::

    import galah
    galah.atlas_species(taxa="Heleioporus")

which returns

.. program-output:: python3 -c "import galah; print(galah.atlas_species(taxa=\"Heleioporus\"))"
