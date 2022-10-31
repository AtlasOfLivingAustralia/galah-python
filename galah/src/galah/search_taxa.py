import requests,os,configparser
import pandas as pd

import sys

APIs = {
    'Australia': 'https://namematching-ws.ala.org.au/'
}

def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

'''
taxa
------
This querys the ALA api and returns a dataframe containing the scientific name of the taxa, the authorship, 
taxonConceptID and rank

arguments
---------
taxa: a string or a list of taxa to get the number of counts for 
         (example: "Vulpes vulpes" or ["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])

returns
------- 
dataFrame: a pandas dataframe with the scientific name of the taxa, the authorship, taxonConceptID and rank.

TODO
----
1. Check with Martin
'''
def search_taxa(taxa):

    # first, check if someone actually entered a taxa name
    if taxa is None:
        raise Exception("You need to specify a taxa")

    # set up configs
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig()
    specific_atlas = atlaslist[atlaslist['atlas'] == configs['galahSettings']['atlas']]

    # test to check if ALA is working
    ALA_check = specific_atlas[specific_atlas['called_by'] == 'search_taxa']
    #names_search_single
    index = ALA_check[ALA_check['api_name'] == "names_search_single"].index[0]
    baseURL = ALA_check[ALA_check['api_name'] == "names_search_single"]['api_url'][index]

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
            response = requests.get(URL)

            # get the response
            json = response.json()
            data = dict(
                (k, json[k]) for k in ('scientificName', 'scientificNameAuthorship', 'taxonConceptID', 'rank') if
                k in json)

            tempdf = pd.DataFrame(data,index=[1])
            dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

        # return dataFrame with all data
        return dataFrame

    # else, let the user know that the taxa argument can only be a string or a lsit
    else:
        raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: search_taxa(\"Vulpes vulpes\")"
                        "\n         search_taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")