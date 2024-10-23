# all available atlases
atlases = ["Australia","Austria","Brazil","France","Global","GBIF","Guatemala","Spain","Sweden"] #,"United Kingdom"]

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
    "Sweden": "taxonConceptID", # was guid
    "United Kingdom": "guid",
}

# error messages to tell the user where to register for the living atlases
ATLAS_OCCURRENCES_ERROR_MESSAGES = {
    "Australia": "go to https://auth.ala.org.au/cas/login to register.",
    "Austria": "go to https://auth.biodiversityatlas.at/cas/login to register.",
    "Brazil": "email atendimento_sibbr@rnp.br to find out more information.",
    "France": "visit https://inpn.mnhn.fr/contact/contacteznous to find out more information.",
    "GBIF": "go to https://www.gbif.org/user/profile to register.",
    "Global": "go to https://www.gbif.org/user/profile to register.",
    "Spain": "go to https://auth.gbif.es/cas/login?lang=en to register."
}

# specifying what each atlas' status is
ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS = {
    "Australia": {"finished_status": "finished","zipURL_arg": "downloadUrl","separator": ","},
    "Austria": {"finished_status": "finished","zipURL_arg": "downloadUrl","separator": ","},
    "Brazil": {"finished_status": "finished","zipURL_arg": "downloadUrl","separator": ","},
    "France": {"finished_status": "finished","zipURL_arg": "downloadUrl","separator": ","},
    "GBIF": {"finished_status": "SUCCEEDED","zipURL_arg": "downloadLink","separator": "\t"},
    "Global": {"finished_status": "SUCCEEDED","zipURL_arg": "downloadLink","separator": "\t"},
    "Guatemala": {"finished_status": "finished","zipURL_arg": "downloadUrl","separator": ","},
    "Spain": {"finished_status": "finished","zipURL_arg": "downloadUrl","separator": ","},
    "Sweden": {"finished_status": "finished","zipURL_arg": "downloadUrl","separator": ","}
}

# expanding species fields
ATLAS_SPECIES_FIELDS = {
    "Australia": {"kingdom": "kingdomID", "phylum": "phylumID", "class": "classID", 
                  "order": "orderID", "family": "familyID","genus": "genusID", 
                  "species": "speciesID", "subspecies": "subspeciesID"},
    "Austria": {"kingdom": "kingdom_guid", "phylum": "phylum_guid","class": "class_guid", 
               "order": "order_guid", "family": "family_guid","genus": "genus_guid", 
               "species": "species_guid", "subspecies": "subspecies_guid"},
    "Brazil": {"kingdom": "kingdom_guid", "phylum": "phylum_guid","class": "class_guid", 
               "order": "order_guid", "family": "family_guid","genus": "genus_guid", 
               "species": "species_guid", "subspecies": "subspecies_guid"},
    "Canada": {},
    "Estonia": {},
    "France": {"kingdom": "kingdomID", "phylum": "phylumID", "class": "classID", 
                  "order": "orderID", "family": "familyID","genus": "genusID", 
                  "species": "speciesID", "subspecies": "subspeciesID"},
    "GBIF": {"kingdom": "KINGDOM_KEY", "phylum": "PHYLUM_KEY", "class": "CLASS_KEY", 
                  "order": "ORDER_KEY", "family": "FAMILY_KEY","genus": "GENUS_KEY", 
                  "species": "SPECIES_KEY", "subspecies": "SUBSPECIES_KEY"},
    "Global": {"kingdom": "KIMGDOM_KEY", "phylum": "PHYLUM_KEY", "class": "CLASS_KEY", 
                  "order": "ORDER_KEY", "family": "FAMILY_KEY","genus": "GENUS_KEY", 
                  "species": "SPECIES_KEY"}, #, "subspecies": "SUBSPECIES_KEY"},
    "Guatemala": {"kingdom": "kingdom_guid", "phylum": "phylum_guid","class": "class_guid", 
                  "order": "order_guid", "family": "family_guid","genus": "genus_guid", 
                  "species": "species_guid", "subspecies": "subspecies_guid"},
    "Portugal": {},
    "Spain": {"kingdom": "kingdomID", "phylum": "phylumID", 
                  "class": "classID", "order": "orderID", "family": "familyID", 
                  "genus": "genusID", "species": "speciesID", "subspecies":"subspeciesID"},
    "Sweden": {"kingdom": "kingdom_id", "phylum": "phylum_id","class": "class_id", 
               "order": "order_id", "family": "family_id","genus": "genus", 
               "species": "species", "subspecies": "subspecies"},
    "United Kingdom": {}
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
    "Guatemala": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Portugal": [],
    "Spain": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Sweden": "basic",
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

# definitions to change algebraic symbols to English predicates for GBIF
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

# denotes keys where the results are
SEARCH_TAXA_ENTRIES = {
    "Austria": ['searchResults','results'],
    "Brazil": ['searchResults','results'],
    "France": ['_embedded','taxa'],
    "Guatemala": ['searchResults','results'],
    "Sweden": ['searchResults','results'],
    "United Kingdom": ['searchResults','results'],
    "UK": ['searchResults','results']
}

# fields to return for search_taxa
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
    "Sweden": ['scientificName', 'scientificNameAuthorship', 'taxonConceptID','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'commonName'],
    "United Kingdom": ['scientificName', 'scientificNameAuthorship', 'guid','rank','match_type','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 'commonName']
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

MM_EXTENSIONS = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "audio/mpeg": "mpg",
    "audio/x-wav": "wav",
    "audio/mp4": "mp4",
    "image/gif": "gif",
    "video/3gpp": "3gp",
    "video/quicktime": "mov",
    "audio/vnd.wave": "wav" 
}