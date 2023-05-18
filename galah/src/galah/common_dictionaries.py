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
    "Guatemala": "id", # was guid
    "Portugal": "usageKey",
    "Spain": "taxonConceptID",
    "Sweden": "id", # was guid
    "United Kingdom": "guid",
}

# default selections for occurrence data
ATLAS_SELECTIONS = {
    "Australia": "basic",
    "Austria": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Brazil": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Canada": [],
    "Estonia": [],
    "France": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Global": ["decimalLatitude", "decimalLongitude", "eventDate", "scientificName", "taxonConceptID", "recordID", "dataResourceName", "occurrenceStatus"],
    "GBIF": ["decimalLatitude", "decimalLongitude", "eventDate", "scientificName", "taxonConceptID", "recordID", "dataResourceName", "occurrenceStatus"],
    "Guatemala": [],
    "Portugal": [],
    "Spain": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Sweden": [],
    "United Kingdom": [],
}

ATLAS_SPECIES_FIELDS = {
    "Australia": ['kingdom','phylum', 'class', 'order', 'family', 'genus'],
    "Austria": ['kingdom','phylum', 'class', 'order', 'family', 'genus'],
    "Brazil": ['kingdom','phylum', 'class', 'order', 'family', 'genus'],
    "Canada": "",
    "Estonia": "",
    "France": ['kingdomName', 'phylumName','className', 'orderName', 'familyName', 'genusName'],
    "GBIF": ['kingdom','phylum', 'class', 'order', 'family', 'genus'],
    "Global": ['kingdom','phylum', 'class', 'order', 'family', 'genus'],
    "Guatemala": ['kingdom','phylum', 'class', 'order', 'family', 'genus'],
    "Portugal": "",
    "Spain": ['kingdom','phylum', 'class', 'order', 'family', 'genus'],
    "Sweden": "",
    "United Kingdom": "",
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
    "France": "_embedded",
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
    "France": "species",
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
    "Brazil": {"species_guid": "id","species": "nameString","author": "author"},
    "Canada": "",
    "Estonia": "",
    "France": {"species_guid": "id","species": "scientificName","author": "authority"},
    "GBIF": {"species_guid": "guid","species": "nameString","author": "author"},
    "Global": {"species_guid": "guid","species": "nameString","author": "author"},
    "Guatemala": "",
    "Portugal": "",
    "Spain": {"species_guid": "guid","species": "nameString","author": "author"},
    "Sweden": "",
    "United Kingdom": "",
}

SEARCH_TAXA_ENTRIES = {
    "Austria": ['searchResults','results'],
    "Brazil": ['searchResults','results'],
    "France": ['_embedded','taxa'],
    "Guatemala": ['searchResults','results'],
    "Sweden": ['searchResults','results']
}

SEARCH_TAXA_FIELDS = {
    "Australia": ['scientificName', 'scientificNameAuthorship', 'taxonConceptID','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'vernacularName'],
    "Austria": ['scientificName', 'scientificNameAuthorship', 'guid','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'commonName'],
    "Brazil": ['scientificName', 'scientificNameAuthorship', 'guid','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'commonName'], 
    "Canada": "",
    "Estonia": "",
    "France": ['scientificName', 'authority', 'id','rankName','match_type','kingdomName', 'phylumName', 
               'className', 'orderName', 'familyName', 'genusName', 'species', 'issues', 'englishVernacularName'],
    "GBIF": ['scientificName', 'scientificNameAuthorship', 'usageKey','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'canonicalName'],
    "Global": ['scientificName', 'scientificNameAuthorship', 'usageKey','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'canonicalName'],
    # was guid
    "Guatemala": ['scientificName', 'scientificNameAuthorship', 'id','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'commonName'],
    "Portugal": "",
    "Spain": ['scientificName', 'scientificNameAuthorship', 'taxonConceptID','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'vernacularName'],
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
    # not sure about this
    "France": ["commonNames","englishVernacularName"],
    "GBIF": "",
    "Global": "",
    "Guatemala": "",
    "Portugal": "",
    "Spain": ["commonNames","nameString"],
    "Sweden": "",
    "United Kingdom": "",
}