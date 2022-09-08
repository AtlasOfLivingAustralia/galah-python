search_taxa()
=================================

This function is used to search for a taxonConceptID, and it is used in ``atlas_counts()`` and ``atlas_occurrences()``.

To get the taxonConceptID for Vulpes vulpes, type

.. prompt::

    import galah
    data=galah.search_taxa("Vulpes vulpes")
    data['taxonConceptID'][0]

which returns

.. program-output:: python3 -c "import galah; print(galah.search_taxa(\"Vulpes vulpes\")[\"taxonConceptID\"][0])"
