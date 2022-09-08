import requests
import pandas as pd

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
def show_all_fields():

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