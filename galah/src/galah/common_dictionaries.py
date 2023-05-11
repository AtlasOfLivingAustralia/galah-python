# all available atlases
atlases = ["Australia","Austria","Brazil","Canada","Estonia","France","Global","GBIF",
           "Guatemala","Portugal","Sweden","Spain","United Kingdom"]

# common names for each atlas
ATLAS_COMMON_NAMES = {
    "Australia": "vernacularName",
    "Austria": "commonName",
    "Brazil": "commonName",
    "Canada": "",
    "Estonia": "",
    "France": "englishVernacularName",
    "Global": "canonicalName",
    "GBIF": "canonicalName",
    "Guatemala": "",
    "Portugal": "",
    "Spain": "vernacularName",
    "Sweden": "",
    "United Kingdom": "",
}

# key works to get taxa
ATLAS_KEYWORDS = {
    "Australia": "taxonConceptID",
    "Austria": "guid",
    "Brazil": "guid", 
    "Canada": "usageKey",
    "Estonia": "guid",
    "France": "id",
    "Global": "usageKey",
    "GBIF": "usageKey",
    "Guatemala": "guid",
    "Portugal": "usageKey",
    "Spain": "taxonConceptID",
    "Sweden": "guid",
    "United Kingdom": "guid",
}

# default selections for occurrence data
ATLAS_SELECTIONS = {
    "Australia": "basic",
    "Austria": [],
    "Brazil": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Canada": [],
    "Estonia": [],
    "France": [],
    "Guatemala": [],
    "Portugal": [],
    "Spain": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Sweden": [],
    "United Kingdom": [],
}

# name of number of counts for atlas_counts
COUNTS_NAMES = {
    "Australia": "totalRecords",
    "Austria": "totalRecords",
    "Brazil": "totalRecords", 
    "Canada": "totalRecords",
    "Estonia": "totalRecords",
    "France": "totalRecords",
    "Global": "count",
    "GBIF": "count",
    "Guatemala": "totalRecords",
    "Portugal": "totalRecords",
    "Spain": "totalRecords",
    "Sweden": "totalRecords",
    "United Kingdom": "totalRecords",
}

# strings for each atlas for depth to determine what taxa it is (improve this selection)
DEPTH_STRINGS = {
    "Australia": "classification",
    "Austria": "searchResults",
    "Brazil": "classification", 
    "Canada": "",
    "Estonia": "",
    "France": "",
    "GBIF": "classification",
    "Global": "classification",
    "Guatemala": "",
    "Portugal": "",
    "Spain": "classification",
    "Sweden": "",
    "United Kingdom": "",
}

# strings for facets
FACETS_STRINGS = {
    "Australia": "speciesID",
    "Austria": "species",
    "Brazil": "species", 
    "Canada": "",
    "Estonia": "",
    "France": "",
    "GBIF": "species",
    "Global": "species",
    "Guatemala": "",
    "Portugal": "",
    "Spain": "species",
    "Sweden": "",
    "United Kingdom": "",
}

# names of species and author for each atlas
TAXONCONCEPT_NAMES = {
    "Australia": {"species_guid": "guid","species": "nameString","author": "author"},
    "Austria": {"species_guid": "guid","species": "species","author": "author"},
    "Brazil": {"species_guid": "guid","species": "nameString","author": "author"},
    "Canada": "",
    "Estonia": "",
    "France": "",
    "GBIF": {"species_guid": "guid","species": "nameString","author": "author"},
    "Global": {"species_guid": "guid","species": "nameString","author": "author"},
    "Guatemala": "",
    "Portugal": "",
    "Spain": {"species_guid": "guid","species": "nameString","author": "author"},
    "Sweden": "",
    "United Kingdom": "",
}

# vernacular names in each atlas
VERNACULAR_NAMES = {
    "Australia": ["commonNames","nameString"],
    "Austria": ["commonNames","commonName"], # try this
    "Brazil": ["commonNames","nameString"], 
    "Canada": "",
    "Estonia": "",
    "France": "",
    "GBIF": "",
    "Global": "",
    "Guatemala": "",
    "Portugal": "",
    "Spain": ["commonNames","nameString"],
    "Sweden": "",
    "United Kingdom": "",
}