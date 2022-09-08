# galah_python

This package is a proof of concept for the translation of the galah package from R into Python.

It is currently under development by Amanda Buyan, supervised by Martin Westgate.

### Current functions finished (listed with their R equivalents):

```
R                           |  Python
----------------------------|--------------------------
atlas_counts()              | galah.atlas_counts()
atlas_occurrences()         | galah.atlas_occurrences()
galah_filter()              | galah.galah_filter()
galah_select()              | galah.galah_select()
galah_group_by()            | galah.galah_group_by()
search_taxa()               | galah.search_taxa()
show_all_fields()           | galah.show_all_fields()
show_all_values()           | galah.show_all_values()
galah_config()              | galah.config()
```

### Functions to be added:

```
R                           |  Python
----------------------------|--------------------------
atlas_media()               | galah.atlas_media()
atlas_species()             | galah.atlas_species()
atlas_taxonomy()            | galah.atlas_taxonomy()
atlas_citation()            | galah.atlas_citation()
galah_identify()            | galah.galah_identify()
galah_geolocate()           | galah.galah_geolocate()
galah_down_to()             | galah.galah_down_to()
search_identifiers()        | galah.search_identifiers()
search_fields()             | galah.search_fields()
search_field_values()       | galah.search_field_values()
search_profile_attributes() | galah.search_profile_attributes()
show_all_profiles()         | galah.show_all_profiles()
show_all_reasons()          | galah.show_all_reasons()
show_all_atlases()          | galah.show_all_atlases()
show_all_ranks()            | galah.show_all_ranks()
show_all_cached_files()     | galah.show_all_cached_files()
clear_cached_files()        | galah.clear_cached_files()
```
