import requests
import pandas as pd

APIs = {
    'Australia': 'https://namematching-ws.ala.org.au/'
}

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

    # first, check which API I am searching (LATER)
    baseURL = APIs['Australia']

    # second, add api/search
    baseURL += 'api/search?'

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
            URL = baseURL+"q={}".format("%20".join(name.split(" ")))
            response = requests.get(URL)

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