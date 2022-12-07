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
    #print(configs['galahSettings']['atlas'])

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
            URL = baseURL.replace("{name}","%20".join(name.split(" ")))
            #print(URL)
            response = requests.get(URL)

            # get the response
            json = response.json()
            # this is for atlas for Australia
            if configs['galahSettings']['atlas'] == "Australia":
                data = dict(
                    (k, json[k]) for k in ('scientificName', 'scientificNameAuthorship', 'taxonConceptID', 'rank') if
                    k in json)
            # this is for Austria
            elif configs['galahSettings']['atlas'] == "Austria":
                #print("here")
                #print(json)
                #print(json['searchResults']['results'][0]['id'])
                data = dict(
                    (k, json['searchResults']['results'][0][k]) for k in ('scientificName', 'scientificNameAuthorship', 'id', 'rank') if
                    k in json['searchResults']['results'][0])
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