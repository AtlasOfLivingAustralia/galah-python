import requests,urllib.parse
import pandas as pd

from .search_taxa import search_taxa
from .get_api_url import get_api_url,readConfig
from .galah_filter import galah_filter
from .common_dictionaries import ATLAS_KEYWORDS,DEPTH_STRINGS,FACETS_STRINGS,TAXONCONCEPT_NAMES,VERNACULAR_NAMES

import sys

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

            if configs['galahSettings']['atlas'] in ["Global","GBIF"]:

                URL = baseURL

                for f in filters:
                    URL += "&{}".format(f)

            else:

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
    if configs['galahSettings']['atlas'] in ["Australia","Austria","Brazil","Global","GBIF","Spain"]:
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
    # names_search_single is for APIs without namematching service
    if configs['galahSettings']['atlas'] in ["Austria"]:
        baseURL = get_api_url(column1='api_name', column1value='names_search_single')
    else:
        baseURL = get_api_url(column1='api_name', column1value='species_lookup')

    # get all the taxonomic information for every species ID
    for species_guid in all_ids:
        
        # check for atlas
        if configs['galahSettings']['atlas'] in ["Brazil","Spain"]: # try this
            URL = baseURL + "/" + urllib.parse.quote(species_guid)
        elif configs['galahSettings']['atlas'] in ["Australia"]:
            URL = baseURL.replace("{id}", urllib.parse.quote(species_guid))
        elif configs['galahSettings']['atlas'] in ["Austria"]:
            URL = baseURL.replace("{name}", urllib.parse.quote(species_guid))
        else:
            raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

        # check to see if user wants the query URL
        if verbose:
            print("URL for querying:\n\n{}\n".format(URL))

        # get response from the API
        response = requests.get(URL)
        json = response.json()
        
        # set up arrays to loop over for different atlases
        if configs["galahSettings"]["atlas"] in ["Austria"]:
            array_depth = json[DEPTH_STRINGS[configs['galahSettings']['atlas']]]['results'][0]
            array_others = json[DEPTH_STRINGS[configs['galahSettings']['atlas']]]['results'][0]
            array_vernacular = json[DEPTH_STRINGS[configs['galahSettings']['atlas']]]['results'][0]
        else:
            array_depth = json[DEPTH_STRINGS[configs['galahSettings']['atlas']]]
            array_others = json['taxonConcept']
            array_vernacular = json[VERNACULAR_NAMES[configs['galahSettings']['atlas']][0]][0]

        # first check for higher orders
        for depth in ['kingdom','phylum','class','order','family']:
            if depth in array_depth:
                data_dict[depth].append(array_depth[depth].lower().capitalize())
            else:
                data_dict[depth].append("")

        # now look for species and author
        for others in ['species','author','species_guid']:
            # if others in array_others:
            if array_others:
                data_dict[others].append(
                    array_others[TAXONCONCEPT_NAMES[configs["galahSettings"]["atlas"]][others]].lower().capitalize())
            else:
                data_dict[others].append("")

        # get common names (vernacular names)
        if array_vernacular:
            data_dict["vernacular_name"].append(array_vernacular[VERNACULAR_NAMES[configs['galahSettings']['atlas']][1]])
        else:
            data_dict["vernacular_name"].append("")

    # return data as a pandas dataframe
    return pd.DataFrame.from_dict(data_dict)