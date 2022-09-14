import requests
import pandas as pd

APIs = {
    'Australia': 'https://namematching-ws.ala.org.au/'
}

'''
taxa
------
This querys the ALA api and returns a dataframe containing the scientific name of the species, the authorship, 
taxonConceptID and rank

arguments
---------
species: a string or a list of species to get the number of counts for 
         (example: "Vulpes vulpes" or ["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])

returns
------- 
dataFrame: a pandas dataframe with the scientific name of the species, the authorship, taxonConceptID and rank.

TODO
----
1. Check with Martin
'''
def search_taxa(species):

    # first, check if someone actually entered a species name
    if species is None:
        raise Exception("You need to specify a species")

    # first, check which API I am searching (LATER)
    baseURL = APIs['Australia']

    # second, add api/search
    baseURL += 'api/search?'

    # third, add fq=<search term> and converting it to URL
    if type(species) is list or type(species) is str:
        # convert to list for easy looping
        if type(species) is str:
            species=[species]

        # create an empty dataframe
        dataFrame = pd.DataFrame()

        # currently only return information above kingdom
        # TODO: return all information (later)
        for name in species:

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

    # else, let the user know that the species argument can only be a string or a lsit
    else:
        raise TypeError("The species argument can only be a string or a list."
                        "\nExample: species.taxa(\"Vulpes vulpes\")"
                        "\n         species.taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")