import requests,urllib.parse
import pandas as pd

from .search_taxa import search_taxa
from .get_api_url import get_api_url
from .get_api_url import readConfig

import sys

ATLAS_KEYWORDS = {
    "Australia": "taxonConceptID",
    "Austria": "guid",
    "Brazil": "guid", 
    "Canada": "usageKey",
    "Estonia": "guid",
    "France": "usageKey",
    "Guatemala": "guid",
    "Portugal": "usageKey",
    "Spain": "taxonConceptID",
    "Sweden": "guid",
    "United Kingdom": "guid",
}

VERNACULAR_NAMES = {
    "Australia": ["commonNames","nameString"],
    "Austria": "",
    "Brazil": ["commonNames","nameString"], 
    "Canada": "",
    "Estonia": "",
    "France": "",
    "Guatemala": "",
    "Portugal": "",
    "Spain": ["commonNames","nameString"],
    "Sweden": "",
    "United Kingdom": "",
}

TAXONCONCEPT_NAMES = {
    "Australia": {"species_guid": "guid","species": "nameString","author": "author"},
    "Austria": "",
    "Brazil": {"species_guid": "guid","species": "nameString","author": "author"},
    "Canada": "",
    "Estonia": "",
    "France": "",
    "Guatemala": "",
    "Portugal": "",
    "Spain": {"species_guid": "guid","species": "nameString","author": "author"},
    "Sweden": "",
    "United Kingdom": "",
}

FACETS_STRINGS = {
    "Australia": "speciesID",
    "Austria": "",
    "Brazil": "species", 
    "Canada": "",
    "Estonia": "",
    "France": "",
    "Guatemala": "",
    "Portugal": "",
    "Spain": "species", ##??
    "Sweden": "",
    "United Kingdom": "",
}

# this function looks for all species with the associated name
def atlas_species(taxa=None,rank="species",verbose=False):
    """
    Used for getting occurrence data for your species.  To get occurrences for

    To know how many total records are in your chosen atlas, type

    .. prompt:: python

        import galah
        galah.atlas_species(taxa="Heleioporus")

    which returns

    .. program-output:: python -c "import galah; print(galah.atlas_species(taxa=\\\"Heleioporus\\\"))"
    """

    # get configs
    configs = readConfig()

    # first, check if the user has specified a taxa
    if taxa is None:
        return ValueError("You need to specify a name for this function to work, i.e. \"Heleioporus\"")
    elif type(taxa) is not str:
        return ValueError("You can only specify one name for this function so far, i.e. \"Heleioporus\"")

    # call galah_identify (or search_taxa for now?) to do something
    baseURL = get_api_url(column1='api_name', column1value='records_species') #,add_email=True)

    # raise warning - not sure how to fix it
    if configs['galahSettings']['atlas'] in ["Spain"]:
        print("There have been some issues getting all species when using a genus name.  Instead, either use a species name or anything of family or higher order.")

    # get the taxonConceptID for taxa
    if configs['galahSettings']['atlas'] in ["Australia","Brazil","Spain"]:
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS[configs['galahSettings']['atlas']]][0]
        URL = baseURL + "?&fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&facets={}".format(FACETS_STRINGS[configs['galahSettings']['atlas']])
    else:
        raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

    # check to see if user wants the query URL
    if verbose:
        print("URL for querying:\n\n{}\n".format(URL))

    # get url and transform from a text string to a list
    response = requests.get(URL)
    all_ids = response.text[1:-2].split('"\n"')[1:]

    # need to get species, author and
    data_dict = {"species": [], "author": [], "species_guid": [], "kingdom": [],"phylum": [],
                 "class": [],"order": [],"family": [], "vernacular_name": []}

    # species_lookup for each individual species
    baseURL = get_api_url(column1='api_name', column1value='species_lookup')

    # get all the taxonomic information for every species ID
    for species_guid in all_ids:
        
        # check for atlas
        if configs['galahSettings']['atlas'] in ["Brazil","Spain"]:
            URL = baseURL + "/" + urllib.parse.quote(species_guid)
        elif configs['galahSettings']['atlas'] in ["Australia"]:
            URL = baseURL.replace("{id}", species_guid)
        else:
            raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

        # check to see if user wants the query URL
        if verbose:
            print("URL for querying:\n\n{}\n".format(URL))

        # get response from the API
        response = requests.get(URL)
        json = response.json()
        
        # get taxonomic information
        for depth in ['kingdom','phylum','class','order','family']:
            if json['classification'][depth]:
                data_dict[depth].append(json['classification'][depth].lower().capitalize())
            else:
                data_dict[depth].append("")
            
        for others in ['species','author','species_guid']:
            if json['taxonConcept'][TAXONCONCEPT_NAMES[configs["galahSettings"]["atlas"]][others]]:
                data_dict[others].append(
                    json['taxonConcept'][TAXONCONCEPT_NAMES[configs["galahSettings"]["atlas"]][others]].lower().capitalize())
            else:
                data_dict[others].append("")

        # get common names (vernacular names)
        if json[VERNACULAR_NAMES[configs['galahSettings']['atlas']][0]]:
            data_dict["vernacular_name"].append(
                json[VERNACULAR_NAMES[configs['galahSettings']['atlas']][0]][0][VERNACULAR_NAMES[configs['galahSettings']['atlas']][1]])
        else:
            data_dict["vernacular_name"].append("")

    # return data as a pandas dataframe
    return pd.DataFrame.from_dict(data_dict)