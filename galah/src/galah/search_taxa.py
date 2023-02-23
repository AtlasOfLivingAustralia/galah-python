import requests
import pandas as pd

from .get_api_url import get_api_url
from .get_api_url import readConfig

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

atlases = ["Australia","Austria","Brazil","Canada","Estonia","France","Guatemala","Portugal","Sweden","Spain","United Kingdom"]

def search_taxa(taxa):
    """
    Look up taxonomic names before downloading data from the ALA, using ``galah.atlas_occurrences()``, ``galah.atlas_species()`` or 
    ``galah.atlas_counts()``. Taxon information returned by ``galah.search_taxa()`` may be passed to the ``taxa`` argument of `atlas` 
    functions. 
    
    ``galah.search_taxa()`` allows users to disambiguate homonyms (i.e. where the same name refers to taxa in different 
    clades) prior to downloading data.

    Parameters
    ----------
        taxa : string
            one or more scientific names to search.  

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.search_taxa(taxa="Vulpes vulpes")

    .. program-output:: python -c "import galah; print(galah.search_taxa(taxa=\\\"Vulpes vulpes\\\"))"
    """

    # get configuration
    configs = readConfig()

    # first, check if someone actually entered a taxa name
    if taxa is None:
        raise Exception("You need to specify a taxa")

    # get base URL for querying
    baseURL = get_api_url(column1='called_by',column1value='search_taxa',column2='api_name',column2value='names_search_single')

    # third, add fq=<search term> and converting it to URL
    if type(taxa) is list or type(taxa) is str:

        # convert to list for easy looping
        if type(taxa) is str:
            taxa=[taxa]

        # create an empty dataframe
        dataFrame = pd.DataFrame()

        # currently only return information above kingdom
        # TODO: return all information (later)
        for name in taxa:

            # create URL, get result and concatenate result onto dataFrame
            # make sure all the atlases are checked
            if configs['galahSettings']['atlas'] in atlases:
                URL = baseURL.replace("{name}","%20".join(name.split(" ")))
            else:
                raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))
            response = requests.get(URL)

            # get the response
            json = response.json()

            # check to see if the taxa was successfully returned
            # don't think this is the best solution for Austria but this is a first shot
            if configs['galahSettings']['atlas'] in ["Australia","Spain"] and not json['success']:
                continue
            elif configs['galahSettings']['atlas'] in ["Brazil"]:
                data={}
                for item in json['searchResults']['results']:
                    if item['scientificName'].lower() == name.lower():
                        for entry in ['scientificName', 'scientificNameAuthorship', ATLAS_KEYWORDS[configs['galahSettings']['atlas']], 'rank']:
                            data[entry] = item[entry]    
            else:
                # this is for atlas for Australia
                ### TODO: Test Spain
                if configs['galahSettings']['atlas'] in ["Australia","Spain"]:
                    data = dict(
                        (k, json[k]) for k in ('scientificName', 'scientificNameAuthorship', ATLAS_KEYWORDS[configs['galahSettings']['atlas']], 'rank') if
                        k in json)
                else:
                    raise ValueError("The atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

            # add every instance of 
            tempdf = pd.DataFrame(data,index=[1])
            dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

        # return dataFrame with all data
        return dataFrame

    # else, let the user know that the taxa argument can only be a string or a lsit
    else:
        raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: search_taxa(\"Vulpes vulpes\")"
                        "\n         search_taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")