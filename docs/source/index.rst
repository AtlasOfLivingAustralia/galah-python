:notoc:

|galah-logo|   galah 
=====================================

.. |galah-logo| image:: _static/logo/logo.png
    :width: 150px
    :alt: galah hexagon logo

**Date**: |today| **Version**: |version|

**galah** is an interface to biodiversity data hosted by the ‘living atlases’; a set of organisations that share a common codebase, 
and act as nodes of the Global Biodiversity Information Facility (GBIF). These organisations collate and store observations of 
individual life forms, using the ‘Darwin Core’ data standard. galah was built and is maintained by the `Science & Decision Support 
Team <https://labs.ala.org.au/>`_ at the `Atlas of Living Australia (ALA) <https://www.ala.org.au/>`_.

galah enables users to locate and download species occurrence records (observations, specimens, eDNA records, etc.), taxonomic information, 
or associated media such as images or sounds, and to restrict their queries to particular taxa or locations. Users can specify which columns 
are returned by a query, or restrict their results to occurrences that meet particular data-quality criteria. All functions return a pandas 
dataframe as their standard format.

The package is named for the bird of the same name (Eolophus roseicapilla), a widely-distributed endemic Australian species. 
The logo was designed by `Ian Brennan <http://www.iangbrennan.org/>`_.

If you have any comments, questions or suggestions, please `contact us <mailto:support@ala.org.au>`_.

.. toctree::
   :maxdepth: 5
   :hidden:

   Getting Started <getting_started/index>
   Galah User Guide <galah_user_guide/index>
   API Docs <apidocs/galah>
   Authors <authors/index>

.. grid:: 1 2 2 2
    :gutter: 4

    .. grid-item-card::
        :link: getting_started/index.html
        :class-card: sd-text-black
        :text-align: center

        .. raw:: html
            :file: _static/icons/getting_started_rocket.svg
                
        **Getting started**

        New to ``galah``?

    .. grid-item-card::
        :class-card: sd-text-black
        :text-align: center

        .. raw:: html
            :file: _static/icons/configuration.svg

        **Galah User Guide**

        Want to know more about how to use ``galah``?

    .. grid-item-card::
        :link: apidocs/galah.html
        :class-card: sd-text-black
        :text-align: center

        .. raw:: html
            :file: _static/icons/user_guide.svg

        **API Docs**

        Want to browse ``galah``'s API docs?
    
    .. grid-item-card:: 
        :class-card: sd-text-black
        :link: authors/index.html
        :text-align: center

        .. raw:: html
            :file: _static/icons/faq.svg

        **Authors**

        Who wrote ``galah``?