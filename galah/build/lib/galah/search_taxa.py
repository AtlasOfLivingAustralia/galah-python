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

ATLAS_COMMON_NAMES = {
    "Australia": "vernacularName",
    "Austria": "",
    "Brazil": "commonName",
    "Canada": "",
    "Estonia": "",
    "France": "",
    "Guatemala": "",
    "Portugal": "",
    "Spain": "vernacularName",
    "Sweden": "",
    "United Kingdom": "",
}

atlases = ["Australia","Austria","Brazil","Canada","Estonia","France","Guatemala","Portugal","Sweden","Spain","United Kingdom"]

def search_taxa(taxa):
    """
    Look up taxonomic names before downloading data from the ALA, using ``atlas_occurrences()``, ``atlas_species()`` or 
    ``atlas_counts()``. Taxon information returned by ``search_taxa()`` may be passed to the ``taxa`` argument of ``atlas`` 
    functions. 
    
    ``search_taxa()`` allows users to disambiguate homonyms (i.e. where the same name refers to taxa in different 
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
            if configs['galahSettings']['atlas'] in ["Brazil"]:
                raw_data = None
                for i,item in enumerate(json['searchResults']['results']):
                    if item['scientificName'].lower() == name.lower():
                        raw_data = json['searchResults']['results'][i]
                if raw_data is None:
                    continue # return pd.DataFrame()
            elif configs['galahSettings']['atlas'] in ["Australia","Spain"]:
                raw_data = json
            else:
                raise ValueError("The atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

            # check to see if the taxa was successfully returned
            if configs['galahSettings']['atlas'] in ["Australia","Spain"] and not json['success']:
                continue
            else:
                data={}
                for item in raw_data: 
                    if item in ['scientificName', 'scientificNameAuthorship', ATLAS_KEYWORDS[configs['galahSettings']['atlas']],
                                'rank', 'match_type','kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'issues', 
                                ATLAS_COMMON_NAMES[configs['galahSettings']['atlas']]]:
                        data[item] = raw_data[item] 

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