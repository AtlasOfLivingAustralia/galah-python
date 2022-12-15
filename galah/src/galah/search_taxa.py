import requests,os,configparser
import pandas as pd

import sys

from .get_api_url import get_api_url
from .get_api_url import readConfig

def search_taxa(taxa):
    """
    Used for getting the taxonConceptID for querying the Atlas.  To get a table with the taxon concept ID, type

    .. prompt:: python

        import galah
        galah.search_taxa(taxa="Vulpes vulpes")

    which returns

    .. program-output:: python3 -c "import galah; print(galah.search_taxa(taxa=\\\"Vulpes vulpes\\\"))"
    """

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
            #URL = baseURL+"q={}".format("%20".join(name.split(" ")))
            # ***Brazil
            if configs['galahSettings']['atlas'] in ["Australia","Austria","Brazil","Canada","Estonia","France","Guatemala",
                                                     "Portugal","Sweden","Spain","United Kingdom"]:
                URL = baseURL.replace("{name}","%20".join(name.split(" ")))
            else:
                raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))
            response = requests.get(URL)
            #print(URL)
            #sys.exit()

            # get the response
            json = response.json()
            #for entry in json:
            #    print(json[entry])
            #sys.exit()
            #print(json)
            #sys.exit()
            #sys.exit()
            # this is for atlas for Australia
            if configs['galahSettings']['atlas'] in ["Australia"]:
                data = dict(
                    (k, json[k]) for k in ('scientificName', 'scientificNameAuthorship', 'taxonConceptID', 'rank') if
                    k in json)
            # or configs['galahSettings']['atlas'] == "Brazil":
            elif configs['galahSettings']['atlas'] in ["Austria","Estonia","Guatemala","Sweden","United Kingdom"]:
                data = dict(
                    (k, json['searchResults']['results'][0][k]) for k in ('scientificName', 'scientificNameAuthorship', 'guid', 'rank') if
                    k in json['searchResults']['results'][0])
            elif configs['galahSettings']['atlas'] in ["Brazil"]:
                data = dict(
                    (k, json['searchResults']['results'][0][k]) for k in ('scientificName', 'scientificNameAuthorship', 'speciesGuid', 'rank') if
                    k in json['searchResults']['results'][0])
            elif configs['galahSettings']['atlas'] in ["Canada","France","Portugal"]:
                data = dict(
                    (k, json[k]) for k in ('scientificName', 'scientificNameAuthorship', 'usageKey', 'rank') if
                    k in json)
            else:
                raise ValueError("The atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

            tempdf = pd.DataFrame(data,index=[1])
            dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

        # return dataFrame with all data
        return dataFrame

    # else, let the user know that the taxa argument can only be a string or a lsit
    else:
        raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: search_taxa(\"Vulpes vulpes\")"
                        "\n         search_taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")