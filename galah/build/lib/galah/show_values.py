import requests,os,configparser
import pandas as pd

from .get_api_url import get_api_url
from .show_all import show_all

import sys

# comment on what this function does later
def show_values(field=None):
    """
    Used for getting the values from a field you want to query.  To see how this is used, type

    .. prompt:: python

        import galah
        galah.show_values(field="basisOfRecord")

    which returns

    .. program-output:: python3 -c "import galah; print(galah.show_values(field=\\\"basisOfRecord\\\"))"
    """

    if field is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field=\"basisOfRecord\"")
    elif type(field) is not str:
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field=\"basisOfRecord\"")

    # get base URL for querying
    baseURL = get_api_url(column1='api_name',column1value='records_facets')

    # add a buttload of checks to make sure that the field they entered actually is something they can query
    ### TODO: talk to Martin about this
    # "field", "profile", "list", "collection", "dataset", "provider")
    #collections,datasets,fields,lists,profiles,providers
    raw_valid_values = show_all(collections=True,datasets=True,fields=True,lists=True,profiles=True,providers=True)
    for i,df in enumerate(raw_valid_values):
        #print(df.columns)
        #print(df.head())
        #if 'listName' in list(df.columns):
        #    print(df['listName'])
        if i == 0:
            if 'listName' in list(df.columns):
                valid_values = df['listName']
            elif 'name' in list(df.columns):
                valid_values = df['name']
            else:
                raise ValueError("Amanda needs to find another name from this list: {}".format(list(df.columns)))
        else:
            if 'listName' in list(df.columns):
                valid_values = pd.concat([valid_values,df['listName']],ignore_index=True)
            elif 'name' in list(df.columns):
                valid_values = pd.concat([valid_values, df['name']], ignore_index=True)
            else:
                raise ValueError("Amanda needs to find another name from this list: {}".format(list(df.columns)))

    # make this a list for easy comparison
    valid_values = list(valid_values)

    if field not in valid_values:
        raise ValueError("{} is not a valid field query.  Use the show_all() function with any of the following set as"
                         "True to show valid values:\n\n"
                         "collections, datasets, fields, lists, profiles, providers\n")

    # add the field
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