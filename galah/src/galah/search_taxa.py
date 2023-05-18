import requests
import pandas as pd

from .get_api_url import get_api_url,readConfig
from .common_dictionaries import ATLAS_KEYWORDS,ATLAS_COMMON_NAMES,SEARCH_TAXA_ENTRIES,SEARCH_TAXA_FIELDS,atlases

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

    # get atlas
    atlas = configs['galahSettings']['atlas']

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
            if atlas in atlases:
                URL = baseURL.replace("{name}","%20".join(name.split(" ")))
            else:
                raise ValueError("Atlas {} is not taken into account".format(atlas))
            response = requests.get(URL)

            # get the response
            response_json = response.json()
            
            # France was here
            if atlas in ["Austria","Sweden"]:
                raw_data = [] #None
                if SEARCH_TAXA_ENTRIES[atlas][0] in response_json:
                    for item in response_json[SEARCH_TAXA_ENTRIES[atlas][0]][SEARCH_TAXA_ENTRIES[atlas][1]]:
                        if name.lower() in item['scientificName'].lower():
                            raw_data = item
                            break
                if raw_data is None:
                    continue
            # still not sure about France but we shall see...
            elif atlas in ["Brazil","France", "Guatemala"]:
                raw_data = None
                if SEARCH_TAXA_ENTRIES[atlas][0] in response_json:
                    for item in response_json[SEARCH_TAXA_ENTRIES[atlas][0]][SEARCH_TAXA_ENTRIES[atlas][1]]:
                        if name.lower() == item['scientificName'].lower():
                            raw_data = item
                            break
                if raw_data is None:
                    continue
            elif atlas in ["Australia","Global","GBIF","Spain"]:
                raw_data = response_json
            else:
                raise ValueError("The atlas {} is not taken into account".format(atlas))

            # check to see if the taxa was successfully returned
            if atlas in ["Australia","Spain"] and not response_json['success']:
                continue
            else:
                data={}
                for item in raw_data: 
                    if item in SEARCH_TAXA_FIELDS[atlas]:
                        #print(item)
                        #print(raw_data[item])
                        #print()
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