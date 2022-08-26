## galah_python

This package is a proof of concept for the translation of the galah package from R into Python.

It is currently under development by Amanda Buyan, supervised by Martin Westgate.

#### Current functions finished (listed with their R equivalents):

```
R                           |  Python
----------------------------|--------------------------
atlas_counts()              | galah.atlas.counts(X,Y)
atlas_occurrences()         | galah.atlas.occurrences(X,Y)
galah_filter()              | galah.galah.filter(X,Y)
galah_select()              | galah.galah.select(X,Y)
galah_group_by()            | galah.galah.groupBy(X,Y)
search_taxa()               | galah.search.taxa()
show_all_fields()           | galah.search.showAllFields()
show_all_values()           | galah.search.showAllValues()
galah_config()              | galah.config(email)
```

#### Functions to be added:

Query: create a ```galah.show``` since there are lots of ```showAll``` functions?

```
R                           |  Python
----------------------------|--------------------------
atlas_media()               | galah.atlas.media()
atlas_species()             | galah.atlas.species()
atlas_taxonomy()            | galah.atlas.taxonomy()
atlas_citation()            | galah.atlas.citation()
galah_identify()            | galah.galah.identify()
galah_geolocate()           | galah.galah.geolocate()
galah_down_to()             | galah.galah.downTo()
search_identifiers()        | galah.search.identifiers()
search_fields()             | galah.search.fields()
search_field_values()       | galah.search.fieldValues()
search_profile_attributes() | galah.search.profileAttributes()
show_all_profiles()         | galah.search.showAllProfiles()
show_all_reasons()          | galah.search.showAllReasons()
show_all_atlases()          | galah.search.showAllAtlases()
show_all_ranks()            | galah.search.showAllRanks()
show_all_cached_files()     | galah.search.showAllCachedFiles()
clear_cached_files()        | galah.search.clearCachedFiles()
```