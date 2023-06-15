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
    "Guatemala": "guid", # was guid
    "Portugal": "usageKey",
    "Spain": "taxonConceptID",
    "Sweden": "guid", # was guid
    "United Kingdom": "guid",
}

ATLAS_RANKS = {
    "Australia": "rank",
    "Austria": "rank",
    "Brazil": "rank",
    "Canada": "",
    "Estonia": "",
    "France": "rankName",
    "Global": "rank",
    "GBIF": "rank",
    "Guatemala": "rank",
    "Portugal": "",
    "Spain": "rank",
    "Sweden": "rank",
    "United Kingdom": "",
}

# expanding species fields
ATLAS_SPECIES_FIELDS = {
    "Australia": ["kingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies"],
    "Austria": ["kingdom", "phylum", "class", "order", "family", "genus", "species"],
    "Brazil": ["kingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies"],
    "Canada": [],
    "Estonia": [],
    "France": ["kingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies"],
    "GBIF": ["kingdom", "phylum", "class", "order", "family", "genus", "species"],
    "Global": ["kingdom", "phylum", "class", "order", "family", "genus", "species"],
    "Guatemala": ["kingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies"],
    "Portugal": [],
    "Spain": ["kingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies"],
    "Sweden": ["kingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies"],
    "United Kingdom": []
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
    "Guatemala": "searchResults",
    "Portugal": "",
    "Spain": "classification",
    "Sweden": "searchResults",
    "United Kingdom": "",
}

FRANCE_FIELDS = {
    "subspecies": "subspecies" ,
    "species": "species", 
    "genus": "genusName",
    "family": "familyName",
    "order": "orderName",
    "class": "className",
    "phylum": "phylumName",
    "kingdom": "kingdomName",
}

# translating French ranks into English ranks
FRANCE_TRANSLATION_RANKS = {
    "Sous-Espèce": "subspecies" ,
    "Espèce": "species" , 
    "Genre": "genus" ,
    "Famille": "family" ,
    "Ordre": "order" ,
    "Classe": "class" ,
    "Phylum": "phylum" ,
    "Règne": "kingdom" ,
}

GBIF_PREDICATE_DEFINITIONS = {
    '=':'equals',
    '==':'equals',
    '&':['and','equals'],
    '|':['or','equals'],
    '<':'lessThan',
    '<=':'lessThanOrEquals',
    '=<':'lessThanOrEquals',
    '>':'greaterThan',
    '>=':'greaterThanOrEquals',
    '=>':'greaterThanOrEquals',
    'in':'in',
    'within':'within', # geometry
    'geoDistance':'geoDistance', #latitude, longitude, distance
    '!=':['not','equals'],
    '=!':['not','equals'],
    'like':'like',
    'isNull':'isNull', # parameter
    'isNotNull':'isNotNull', # parameter
}

# names of species and author for each atlas
TAXONCONCEPT_NAMES = {
    "Australia": {"guid": "guid","author": "author"}, # "species": "nameString",
    "Austria": {"guid": "guid","author": "author"}, # "species": "species",
    "Brazil": {"guid": "id","author": "author"}, #"species": "nameString",
    "Canada": "",
    "Estonia": "",
    "France": {"guid": "id","author": "authority"}, #"species": "scientificName",
    "GBIF": {"guid": "usageKey","author": "author"}, #"species": "nameString",
    "Global": {"guid": "usageKey","author": "author"}, #"species": "nameString",
    "Guatemala": {"guid": "guid","author": "author"},
    "Portugal": "",
    "Spain": {"guid": "guid","author": "author"}, #"species": "nameString",
    "Sweden": {"guid": "guid","author": "author"},
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
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'vernacularName'],
    "Global": ['scientificName', 'scientificNameAuthorship', 'usageKey','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'vernacularName'],
    # was guid
    "Guatemala": ['scientificName', 'scientificNameAuthorship', 'guid','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'commonName'],
    "Portugal": "",
    "Spain": ['scientificName', 'scientificNameAuthorship', 'taxonConceptID','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'vernacularName'],
    "Sweden": ['scientificName', 'scientificNameAuthorship', 'guid','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'commonName'],
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
    "GBIF": ["vernacularName","vernacularName"],
    "Global": ["vernacularName","vernacularName"],
    "Guatemala": ["commonName","commonName"],
    "Portugal": "",
    "Spain": ["commonNames","nameString"],
    "Sweden": ["commonName","commonName"],
    "United Kingdom": "",
}