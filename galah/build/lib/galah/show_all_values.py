import requests
import pandas as pd

APIs = {
    'Australia': 'https://namematching-ws.ala.org.au/'
}

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
def show_all_values(field):

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