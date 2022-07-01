'''
This is a collection of the filtering functions available on galah
'''

import requests,sys
import pandas as pd

'''
Function comments here

arguments: one or more scientific names (search=True) or taxonomic identifiers
               (search=False)
'''
APIs = {
    'Australia': 'https://namematching-ws.ala.org.au/'
}

def taxa(species):
    # first, check if someone actually entered a species name
    if species is None:
        raise Exception("You need to specify a species")
        sys.exit()

    # first, check which API I am searching (LATER)
    baseURL = APIs['Australia']

    # second, add api/search
    baseURL += 'api/search?'

    # third, add ?q=<search term> (replace spaces with %20)
    # check if there is one or multiple species listed.  If there is only one, then use the first loop.
    if type(species) == str:
        # only have one species, getting one response
        baseURL += "q={}".format("%20".join(species.split(" ")))
        response = requests.get(baseURL)
        json = response.json()
        # categories to get: scientificName, scientificNameAuthorship, taxonConceptID, rank
        data = dict((k,json[k]) for k in ('scientificName','scientificNameAuthorship','taxonConceptID','rank') if k in json)
        dataFrame = pd.DataFrame(data,index=[1])
        return(dataFrame)
    elif type(species) == list:
        # have multiple species - use this loop
        dataFrame = pd.DataFrame()
        # currently only return information above kingdom
        # TODO: return all information (very much later)
        for name in species:
            URL = baseURL+"q={}".format("%20".join(name.split(" ")))
            response = requests.get(URL)
            json = response.json()
            data = dict(
                (k, json[k]) for k in ('scientificName', 'scientificNameAuthorship', 'taxonConceptID', 'rank') if
                k in json)
            tempdf = pd.DataFrame(data,index=[1])
            dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)
        return (dataFrame)
    else:
        # the user has not used it correctly - let them know how to use it
        raise TypeError("The species argument can only be a string or a list."
                        "\nExample: species.taxa(\"Vulpes vulpes\")"
                        "\n         species.taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")

'''
def identifiers():
    # pseudocode here

def fields():
    # pseudocode here
'''
def showAllFields():
    # pseudocode here
    # this URL returns all fields - Amanda to program this
    # fq=(filter) ???
    response = requests.get("https://biocache-ws.ala.org.au/ws/index/fields")
    test=pd.DataFrame.from_dict(response.json())
    print(list(test['name']))

'''
def fieldValues():
    # pseudocode here

def profileAttributes():
    # pseudocode here
    
def showAllProfiles():
    # pseudocode here
    
def showAllAtlases():
    # pseudocode here
    
def showAllRanks():
    # pseudocode here
'''
