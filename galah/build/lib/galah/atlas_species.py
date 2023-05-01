import requests,urllib.parse
import pandas as pd

from .search_taxa import search_taxa
from .get_api_url import get_api_url,readConfig
from .galah_filter import galah_filter

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
    "Spain": "species",
    "Sweden": "",
    "United Kingdom": "",
}

# this function looks for all species with the associated name
def atlas_species(taxa=None,filters=None,verbose=False):
    """
    While there are reasons why users may need to check every record meeting their search criteria (i.e. using ``galah.atlas_occurrences()``), 
    a common use case is to simply identify which species occur in a specified region, time period, or taxonomic group. 
    This function returns a ``pandas.DataFrame`` with one row per species, and columns giving associated taxonomic information.

    Parameters
    ----------
        taxa : string / list
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.  
        rank : string
            filters, in the form ``field`` ``logical`` ``value`` (e.g. ``"year=2021"``)
        verbose : 
            If ``True``, galah gives you the URLs used to query all the data.  Default to ``False``.

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        galah.atlas_species(taxa="Heleioporus")

    .. program-output:: python -c "import galah; print(galah.atlas_species(taxa=\\\"Heleioporus\\\"))"
    """

    # get configs
    configs = readConfig()

    # first, check if the user has specified a taxa
    if taxa is None:
        raise ValueError("You need to specify a name for this function to work, i.e. \"Heleioporus\"")
    elif type(taxa) is not str and type(taxa) is not list:
        raise ValueError("Only a string or list can be specified for taxa names")

    # call galah_identify (or search_taxa for now?) to do something
    baseURL = get_api_url(column1='api_name', column1value='records_species')

    # raise warning - not sure how to fix it
    if configs['galahSettings']['atlas'] in ["Spain"]:
        print("There have been some issues getting all species when using a genus name.  Instead, either use a species name or anything of family or higher order.")

    # check if filters are specified
    if filters is not None:

        # check the type of variable filters is
        if type(filters) is list or type(filters) is str:

            # change to list for easier looping
            if type(filters) is str:
                filters = [filters]

            # start URL - might need to add + "&" later
            URL = baseURL + "?&fq=%28"

            # loop over filters
            for f in filters:
                URL += galah_filter(f) + "%20AND%20"

            # add final part of URL
            URL = URL[:-len("%20AND%20")] + "%29"

        # else, make sure that the filters is in the following format
        else:
            raise TypeError("filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")
    else:

        URL = baseURL + "?"
    
     # get the taxonConceptID for taxa
    if configs['galahSettings']['atlas'] in ["Australia","Brazil","Spain"]:
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS[configs['galahSettings']['atlas']]][0]
        URL += "&fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&facets={}".format(FACETS_STRINGS[configs['galahSettings']['atlas']])
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
            if depth in json['classification']:
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