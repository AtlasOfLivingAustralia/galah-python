import requests,os,configparser
import pandas as pd

from .get_api_url import get_api_url

import sys

# comment on what this function does later
def show_values(field=None):

    if field is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field=\"basisOfRecord\"")
    elif type(field) is not str:
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field=\"basisOfRecord\"")

    # get base URL for querying
    baseURL = get_api_url(column1='api_name',column1value='records_facets')

    # add the field
    #+ "?facets="
    URL = baseURL + "?facets=" + field

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