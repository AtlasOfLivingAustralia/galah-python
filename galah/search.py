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

'''
taxa()

This querys the ALA api and returns a dataframe containing the scientific name of the species, 
the authorship, taxonConceptID and rank.

TODO: return all fields associated with the query

ARGS:
species: either a string or a list containing species names

RETURNS:
dataFrame with the scientific name of the species, the authorship, taxonConceptID and rank.
'''
def taxa(species):
    # first, check if someone actually entered a species name
    if species is None:
        raise Exception("You need to specify a species")

    # first, check which API I am searching (LATER)
    baseURL = APIs['Australia']

    # second, add api/search
    baseURL += 'api/search?'

    # third, add fq=<search term> and converting it to URL
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
'''
showAllFields()

This function returns all possible fields to filter yoru query by

Takes no arguments

RETURNS:
dataFrame: a data frame with the name, description, dataType and infoUrl for each query possibility
'''
def showAllFields():
    # fq=(filter) ???
    # go through
    response = requests.get("https://biocache-ws.ala.org.au/ws/index/fields")
    fields=pd.DataFrame.from_dict(response.json())
    dataFrame = fields[['name','description','dataType','infoUrl']]
    # change the column names
    #newDataFrame.rename(columns = {'name':'id','dataType':'type','infoUrl':'link'})
    return dataFrame

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
