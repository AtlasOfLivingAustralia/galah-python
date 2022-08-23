'''
This is a collection of the search functions from the R galah package

Each function has a description of what it does and what its arguments are
'''

import requests,sys
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
def taxa(species):

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

'''
showAllFields
-------------
This function returns all possible fields to use as filters in your query.

arguments
---------
None

returns
------- 
dataFrame: a data frame with the name, description, dataType and infoUrl for each query possibility

TODO
----
1. Check with Martin on datatypes
'''
def showAllFields():

    # get all fields from the API
    response = requests.get("https://biocache-ws.ala.org.au/ws/index/fields")
    fields=pd.DataFrame.from_dict(response.json())

    # only return the columns below
    # TODO: make sure that this matches the R version of galah
    dataFrame = fields[['name','description','dataType','infoUrl']]

    # how to change the column names
    # TODO: determine if this is needed
    #newDataFrame.rename(columns = {'name':'id','dataType':'type','infoUrl':'link'})
    return dataFrame

'''
# search for taxa with taxonomic identifiers
def identifiers():
    # pseudocode here

# returns a data.frame of all fields matching the type specified (columns is id, description, type, link)
# example: search.fields(query,type=["all","fields","layers","assertions","media","other"])
#  query: a search string (not case sensitive) example:
#  type: what type of parameters should be searched?
# returns
def fields(query=None,type=None):
    # pseudocode here
    
# search for valid options of a categorical field
# example: search.fieldValues(field, limit = 20)
#    field: string, field to return the categories for.  Use search_fields
def fieldValues():
    # pseudocode here
'''

'''
showAllValues
-------------
This function returns all possible values for the field query.

arguments
---------
field: the field you want to know valid values for (i.e. basisOfRecord)

returns
------- 
dataFrame: a data frame with the possible values for the field

TODO
----
1. More robust testing
'''
def showAllValues(field):

    # the baseURL before adding the field we want to query
    baseURL="https://biocache-ws.ala.org.au/ws/occurrence/facets?facets="

    # add the field
    URL = baseURL + field

    # query the API
    response = requests.get(URL)
    json = response.json()

    # create empty dataFrame to concatenate results to
    dataFrame = pd.DataFrame()

    # loop over results and create dataFrame
    for i,entry in enumerate(json[0]['fieldResult']):
        tempdf = pd.DataFrame([entry['i18nCode'].split('.')],columns=['field','category'])
        dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

    # return dataFrame
    return dataFrame

'''
def profileAttributes():
    # pseudocode here
    
def showAllProfiles():
    # pseudocode here
    
def showAllAtlases():
    # pseudocode here
    
def showAllRanks():
    # pseudocode here

def showAllReasons():
    # pseudocode here
'''
