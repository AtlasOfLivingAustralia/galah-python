import requests,os,configparser
import pandas as pd

def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

# comment on what this function does later
### TODO: figure out which api I'm querying???
def show_values(field=None):

    print("in show_values")

    if field is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field=\"basisOfRecord\"")
    elif type(field) is not str:
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field=\"basisOfRecord\"")

    # get configuration for atlas to query
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig()
    specific_atlas = atlaslist[atlaslist['atlas'] == configs['galahSettings']['atlas']]

    # call galah_identify (or search_taxa for now?) to do something
    # species_lookup
    media_rows = specific_atlas[specific_atlas['api_name'] == 'records_facets']
    index = media_rows[media_rows['api_name'] == "records_facets"].index[0]
    baseURL = media_rows[media_rows['api_name'] == 'records_facets']['api_url'][index]

    # add the field
    #+ "?facets="
    URL = baseURL + "?facets=" + field

    print(URL)

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