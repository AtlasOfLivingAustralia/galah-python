import requests,os,configparser
import pandas as pd

import sys

# read configuration file to get atlas and other specific parameters
def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

# see if it can return multiple values
def show_all(collections=False,
             datasets=False,
             providers=False,
             values=None,
             profiles=False,
             profile_values=False,
             licenses=False,
             lists=False,
             list_values=False,
             reasons=False,
             assertions=False,
             fields=False,
             ):

    # configure which atlas you are looking at
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
    atlases = pd.read_csv(atlasfile)
    configs = readConfig()
    specific_atlas = atlases[atlases['atlas'] == configs['galahSettings']['atlas']]

    return_array=[]

    # catch all function for showing all options
    # get all fields from the API
    if fields:
        # make sure this is ok for future
        fields_URLS = specific_atlas[specific_atlas['called_by'] == 'show_all_fields']
        index = fields_URLS[fields_URLS['api_name'] == "records_fields"].index[0]
        response = requests.get(fields_URLS[fields_URLS['api_name'] == "records_fields"]['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())

        # only return the columns below
        # TODO: make sure that this matches the R version of galah
        dataFrame = fields[['name', 'description', 'dataType', 'infoUrl']]
        return_array.append(dataFrame)

    # check for collections
    # TODO: add option to query by word
    # df.loc[df['called_by'].str.contains('assert',case=True)]
    if collections:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_collections'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_collections'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(specific_atlas[specific_atlas['called_by'] == 'show_all_collections']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_collections']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # check for datasets
    # TODO: add option to query by word
    # df.loc[df['called_by'].str.contains('assert',case=True)]
    if datasets:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_datasets'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_datasets'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(specific_atlas[specific_atlas['called_by'] == 'show_all_datasets']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_datasets']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # check for datasets
    # TODO: add option to query by word
    # df.loc[df['called_by'].str.contains('assert',case=True)]
    if providers:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_providers'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_providers'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(specific_atlas[specific_atlas['called_by'] == 'show_all_providers']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_providers']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # TODO: add possiblity for multiple values
    if values is not None:
        if values is True:
            raise ValueError("You need to specify what value you want to query.  For a list of possible queries, run"
                  "\n\ngalah.show_all(fields=True)\n")
        else:
            if len(specific_atlas.loc[specific_atlas['called_by'].str.contains('show_field_values',case=True)].index) == 1:
                index = specific_atlas.loc[specific_atlas['called_by'].str.contains('show_field_values',case=True)].index[0]
            else:
                # show_all_values is not listed
                print(specific_atlas[specific_atlas['called_by'] == 'show_field_values'])
                raise ValueError("another case of usage - need to add more code\n\n{}".format(specific_atlas[specific_atlas['called_by'] == 'show_all_values']))
            response = requests.get("{}?facets={}".format(str(specific_atlas.loc[specific_atlas['called_by'].str.contains('show_field_values',case=True)]['api_url'][index]),values))
            json = response.json()
            dataFrame = pd.DataFrame()
            for i, entry in enumerate(json[0]['fieldResult']):
                tempdf = pd.DataFrame([entry['i18nCode'].split('.')], columns=['field', 'category'])
                dataFrame = pd.concat([dataFrame, tempdf], ignore_index=True)
            return_array.append(dataFrame)

    # check for datasets
    # TODO: add option to query by word
    # df.loc[df['called_by'].str.contains('assert',case=True)]
    if profiles:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_profiles'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_profiles'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_profiles']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_profiles']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # check for datasets
    # TODO: add option to query by word
    # df.loc[df['called_by'].str.contains('assert',case=True)]
    if profile_values:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_profile_values'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_profile_values'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_profile_values']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_profile_values']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # check for datasets
    # TODO: add option to query by word
    # df.loc[df['called_by'].str.contains('assert',case=True)]
    if licenses:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_licences'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_licences'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_licences']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_licences']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # check for datasets
    # TODO: add option to query by word
    # df.loc[df['called_by'].str.contains('assert',case=True)]
    if lists:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_lists'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_lists'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_lists']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_lists']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # this one isn't working - replace list_id with something
    if list_values:
        print(specific_atlas[specific_atlas['called_by'] == 'show_list_values'].index)
        if len(specific_atlas[specific_atlas['called_by'] == 'show_list_values'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_list_values'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_list_values']))
        print(specific_atlas[specific_atlas['called_by'] == 'show_list_values']['api_url'][index])
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_list_values']['api_url'][index])
        print(response.json())
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # check for datasets
    # TODO: add option to query by word
    # df.loc[df['called_by'].str.contains('assert',case=True)]
    if reasons:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_reasons'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_reasons'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_reasons']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_reasons']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # check for datasets
    # TODO: add option to query by word
    # df.loc[df['called_by'].str.contains('assert',case=True)]
    if assertions:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_assertions'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_assertions'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_assertions']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_assertions']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        return_array.append(fields)

    # return variables
    if len(return_array) == 1:
        return return_array[0]
    return return_array