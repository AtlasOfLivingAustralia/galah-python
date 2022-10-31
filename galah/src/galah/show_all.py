import requests,os,configparser
import pandas as pd
from pandas import DataFrame

import sys

# read configuration file to get atlas and other specific parameters
def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

'''         
    list_values=None,

    # this one isn't working - replace list_id with something
    ### DEBUG THIS BEFORE SPLIT
    if list_values is not None:
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
        if list_values is True:
            return_array.append(fields)
        else:
            if type(list_values) is str:
                return_array.append(
                    fields.loc[fields['name'].str.contains(list_values, case=True)].sort_values('name',
                                                                                          key=lambda x: x.str.len()))
            else:
                raise ValueError("You can only pass one string to your search parameter")
       
    #--------------------------- 
    profile_values=None,
             
    # check for profile_values (ask Dax if this is what I'm supposed to be getting)
    ### DAX
    if profile_values is not None:
        if len(specific_atlas[specific_atlas['called_by'] == 'show_profile_values'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_profile_values'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_profile_values']))
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_profile_values']['api_url'][index])
        fields = pd.DataFrame.from_dict(response.json())
        if profile_values is True:
            return_array.append(fields)
        else:
            if type(profile_values) is str:
                return_array.append(fields.loc[fields['name'].str.contains(profile_values, case=True)].sort_values('name',
                                                                                                             key=lambda
                                                                                                                 x: x.str.len()))
            else:
                raise ValueError("You can only pass one string to your search parameter")
    
    #---------------------------         
    values=None,
             
    # check for values
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
'''

'''
function is meant to show all values for possible query fields - they are defined as a boolean variable so you can see
the large list of all the potential variables to add to your atlas query.
'''
def show_all(assertions=False,
             atlases=False,
             apis=False,
             collections=False,
             datasets=False,
             fields=False,
             licences=False,
             lists=False,
             profiles=False,
             providers=False,
             ranks=False,
             reasons=False,
             ):

    # configure which atlas you are looking at
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig()
    specific_atlas = atlaslist[atlaslist['atlas'] == configs['galahSettings']['atlas']]

    # set up the option for getting back multiple values
    return_array=[]

    # check for assertions boolean
    if assertions:
        # check to see if there are multiple assertion URLs
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_assertions'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_assertions'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_assertions']))
        # query the API for assertions
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_assertions']['api_url'][index])
        # create a dataFrame from the response
        json = pd.DataFrame.from_dict(response.json())
        # set default value for the 'type' column
        json['type'] = assertions
        # append this data frame to the return_array
        return_array.append(json[['name','description','category','type']])

    # return all the atlases you can query
    if atlases:
        # dictionary of all atlases galah currently supports
        data = {
            "atlas": ["Australia","Austria","Brazil","Estonia","France","Guatemala","Portugal","Spain","Sweden","United Kingdom"],
            "institution": ["Atlas of Living Australia","Biodiversitäts-Atlas Österreich","Sistemas de Informações sobre a Biodiversidade Brasileira",
                            "eElurikkus","Inventaire National du Patrimoine Naturel","Sistema Nacional de Información sobre Diversidad Biológica de Guatemala",
                            "GBIF Portugal","GBIF Spain","Swedish Biodiversity Data Infrastructure","National Biodiversity Network"],
            "acronym": ["ALA","BAO","SiBBr","<NA>","INPN","SNIBgt","GBIF.pt","GBIF.es","SBDI","NBN",],
            "url": ["https://www.ala.org.au","https://biodiversityatlas.at","https://sibbr.gov.br","https://elurikkus.ee",
                    "https://inpn.mnhn.fr","https://snib.conap.gob.gt","https://www.gbif.pt","https://www.gbif.es",
                    "https://biodiversitydata.se","https://nbn.org.uk"],
        }
        # append this data frame to the return_array
        return_array.append(pd.DataFrame.from_dict(data))

    # return all the possible apis you could query
    if apis:
        # append the full atlaslist to return_array
        return_array.append(atlaslist)

    # check for collections
    if collections:
        # check to see if there are multiple collection URLs
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_collections'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_collections'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(specific_atlas[specific_atlas['called_by'] == 'show_all_collections']))
        # get response from collections API query
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_collections']['api_url'][index])
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(response.json()))

    # check for datasets
    if datasets:
        # check to see if there are multiple dataset URLs
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_datasets'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_datasets'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(specific_atlas[specific_atlas['called_by'] == 'show_all_datasets']))
        # get response from collections API query
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_datasets']['api_url'][index])
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(response.json()))

    # get all fields from the API
    if fields:
        # check for URLs containing fields (there are two)
        fields_URLS = specific_atlas[specific_atlas['called_by'] == 'show_all_fields']
        # get the index of the api that contains fields, and doesn't deal with the spatial portal
        index = fields_URLS[fields_URLS['api_name'] == "records_fields"].index[0]
        # get response from fields API query
        response = requests.get(fields_URLS[fields_URLS['api_name'] == "records_fields"]['api_url'][index])
        # get data frame from response
        fields_values = pd.DataFrame.from_dict(response.json())
        # select only the columns titled 'name', 'info', 'infoUrl'
        dataFrame = fields_values[['name', 'info', 'infoUrl']]
        # create empty array for types to add to data frame
        types = []
        # loop over data frame
        for i in dataFrame['name']:
            # if characters from 2 to the end of the string are digits, then it is a layer.  Otherwise, it's a field
            if i[2:].isdigit():
                types.append("layer")
            else:
                types.append("fields")
        # add the types array as another column to the data frame
        dataFrame.insert(loc=3,column='type',value=types)
        # append the data frame sorted by type first, then name
        return_array.append(dataFrame.sort_values(['type','name']).reset_index(drop=True))

    # get all licences from the API
    if licences:
        # check to see if there are multiple licences URLs
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_licences'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_licences'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_licences']))
        # get response from licences API query
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_licences']['api_url'][index])
        # create a data frame from the API response
        json = pd.DataFrame.from_dict(response.json())
        # append data frame with only the column names 'id', 'name', 'acronym' and 'url'
        return_array.append(json[['id','name','acronym','url']])

    # get all lists from the API
    if lists:
        # check to see if there are multiple lists URLs
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_lists'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_lists'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_lists']))
        # add offsets to get all the lists from the api - loop over the 3 listed offsets
        # 1. query the API for the data
        # 2. if this is the first offset, then create a new data frame from the data
        #    if this is not the first offset, concatenate the new data frame onto the old one
        for i,maxoffsets in enumerate(["?max=1000&offset=0","?max=1000&offset=1000","?max=1000&offset=2000"]):
            response = requests.get(
                "{}{}".format(specific_atlas[specific_atlas['called_by'] == 'show_all_lists']['api_url'][index],maxoffsets))
            if i == 0:
                json = pd.DataFrame.from_dict(response.json())
            else:
                json = pd.concat([json,pd.DataFrame.from_dict(response.json())], ignore_index=True)
        # loop over the dictionaries in the 'list' column to get the actual list parameters
        #    if this is the first list, create a new dataframe
        #    if it is not the first list, concatenate a new data frame onto the old data frame
        for i,l in enumerate(json['lists']):
            if i == 0:
                df = pd.DataFrame(l,index=[0])
            else:
                df = pd.concat([df, pd.DataFrame(l,index=[0])], ignore_index=True)
        # append data frame to return_array
        return_array.append(df)

    # get all profiles from the API
    if profiles:
        # check to see if there are multiple lists URLs
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_profiles'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_profiles'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_profiles']))
        # get response from profiles API query
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_profiles']['api_url'][index])
        # create a data frame from the API response
        json = pd.DataFrame.from_dict(response.json())
        # append data frame with only the column names 'id', 'name', 'shortName' and 'description'
        return_array.append(json[['id','name','shortName','description']])

    # get all providers from the API
    if providers:
        # check to see if there are multiple lists URLs
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_providers'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_providers'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(specific_atlas[specific_atlas['called_by'] == 'show_all_providers']))
        # get response from providers API query
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_providers']['api_url'][index])
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(response.json()))

    # get all ranks from the API
    if ranks:
        # extended ranks dictionary
        all_ranks = {
            'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
                55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
            'name': ['root',"superkingdom", "kingdom", "subkingdom", "superphylum", "phylum", "subphylum", "superclass",
                     "class", "subclass", "infraclass", "subinfraclass", "superdivison zoology", "division zoology",
                     "subdivision zoology", "supercohort", "cohort", "subcohort", "superorder", "order", "suborder",
                     "infraorder", "parvorder", "superseries zoology", "series zoology", "subseries zoology",
                     "supersection zoology", "section zoology", "subsection zoology", "superfamily", "family",
                     "subfamily", "infrafamily", "supertribe", "tribe", "subtribe", "supergenus", "genus group",
                     "genus", "nothogenus", "subgenus", "supersection botany", "section botany", "subsection botany",
                     "superseries botany", "series botany", "subseries botany", "species group", "superspecies",
                     "species subgroup", "species", "nothospecies", "holomorph", "anamorph", "teleomorph", "subspecies",
                     "nothosubspecies", "infraspecies", "variety", "nothovariety", "subvariety", "form", "nothoform",
                     "subform", "biovar", "serovar", "cultivar", "pathovar", "infraspecific"]
        }
        '''
        # add this in with configuration file
        # short ranks dictionary
        global_ranks = {
            'id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'name': ["kingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies", "infraspecific"]
        }
        '''
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(all_ranks))

    # check for reasons
    if reasons:
        # check to see if there are multiple lists URLs
        if len(specific_atlas[specific_atlas['called_by'] == 'show_all_reasons'].index) == 1:
            index = specific_atlas[specific_atlas['called_by'] == 'show_all_reasons'].index[0]
        else:
            raise ValueError("another case of usage - need to add more code\n\n{}".format(
                specific_atlas[specific_atlas['called_by'] == 'show_all_reasons']))
        # get response from response API query
        response = requests.get(specific_atlas[specific_atlas['called_by'] == 'show_all_reasons']['api_url'][index])
        # create a data frame from the API response
        json = pd.DataFrame.from_dict(response.json())
        # append data frame with only the column names 'id', 'name', sort values by 'id', and renumber indices
        return_array.append(json[['id','name']].sort_values('id').reset_index(drop=True))

    # if there is only a singular data frame in the return_array, return only this; otherwise, return list
    if len(return_array) == 1:
        return return_array[0]
    return return_array