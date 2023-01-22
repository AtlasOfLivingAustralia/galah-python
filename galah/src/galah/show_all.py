import requests,os
import pandas as pd

from .get_api_url import get_api_url
from .get_api_url import readConfig

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
    """
    Used for getting various amounts of information about the chosen atlas you want to
    get occurrences from.

    To find out what datasets are in your atlas, type

    .. prompt:: python

        import galah
        galah.show_all(datasets=True)

    which returns

    .. program-output:: python3 -c "import galah; print(galah.show_all(datasets=True))"
    """

    # get configurations for different atlases
    configs = readConfig()

    # set up the option for getting back multiple values
    return_array=[]

    # check for assertions boolean
    if type(assertions) is bool and assertions:
        response = requests.get(get_api_url(column1='called_by',column1value='show_all_assertions'))
        # create a dataFrame from the response
        json = pd.DataFrame.from_dict(response.json())
        # set default value for the 'type' column
        json['type'] = assertions
        # append this data frame to the return_array
        return_array.append(json[['name','description','category','type']])
    elif not assertions:
        pass
    else:
        raise ValueError("You can only specify True for assertions (default=False)")

    # return all the atlases you can query
    if type(atlases) is bool and atlases:
        # dictionary of all atlases galah currently supports
        data = {
            "atlas": ["Australia","Austria","Brazil","Canada","Estonia","France","Guatemala","Portugal","Spain","Sweden","United Kingdom"],
            "institution": ["Atlas of Living Australia","Biodiversitäts-Atlas Österreich","Sistemas de Informações sobre a Biodiversidade Brasileira",
                            "Canadensys", "eElurikkus","Inventaire National du Patrimoine Naturel","Sistema Nacional de Información sobre Diversidad Biológica de Guatemala",
                            "GBIF Portugal","GBIF Spain","Swedish Biodiversity Data Infrastructure","National Biodiversity Network"],
            "acronym": ["ALA","BAO","SiBBr","<NA>","<NA>","INPN","SNIBgt","GBIF.pt","GBIF.es","SBDI","NBN",],
            "url": ["https://www.ala.org.au","https://biodiversityatlas.at","https://sibbr.gov.br","http://www.canadensys.net/",
                    "https://elurikkus.ee","https://inpn.mnhn.fr","https://snib.conap.gob.gt","https://www.gbif.pt",
                    "https://www.gbif.es","https://biodiversitydata.se","https://nbn.org.uk"],
        }
        # append this data frame to the return_array
        return_array.append(pd.DataFrame.from_dict(data))
    elif not atlases:
        pass
    else:
        raise ValueError("You can only specify True for atlases (default=False)")

    # return all the possible apis you could query
    if type(apis) is bool and apis:
        # append the full atlaslist to return_array
        atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
        atlaslist = pd.read_csv(atlasfile)
        return_array.append(atlaslist)
    elif not apis:
        pass
    else:
        raise ValueError("You can only specify True for apis (default=False)")

    # check for collections
    if type(collections) is bool and collections:
        response = requests.get(get_api_url(column1='called_by', column1value='show_all_collections'))
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(response.json()))
    elif not collections:
        pass
    else:
        raise ValueError("You can only specify True for collections (default=False)")

    # check for datasets
    if type(datasets) is bool and datasets:
        response = requests.get(get_api_url(column1='called_by', column1value='show_all_datasets'))
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(response.json()))
    elif not datasets:
        pass
    else:
        raise ValueError("You can only specify True for datasets (default=False)")

    # get all fields from the API
    if type(fields) is bool and fields:
        # query the API for fields
        response = requests.get(get_api_url(column1='called_by',column1value='show_all_fields',column2='api_name',column2value='records_fields'))
        # get data frame from response
        fields_values = pd.DataFrame.from_dict(response.json())
        # select only the columns titled 'name', 'info', 'infoUrl'
        if configs['galahSettings']['atlas'] in ["Australia"]:
            dataFrame = fields_values[['name', 'info', 'infoUrl']]
        elif configs['galahSettings']['atlas'] in ["Austria","Brazil","Canada","Estonia","France","Guatemala","Sweden","United Kingdom"]:
            dataFrame = fields_values[['name', 'info']]
        else:
            raise ValueError("Atlas {} not taken into account".format(configs['galahSettings']['atlas']))
        # create empty array for types to add to data frame
        layer_types = []
        # loop over data frame
        for i in dataFrame['name']:
            # if characters from 2 to the end of the string are digits, then it is a layer.  Otherwise, it's a field
            if i[2:].isdigit():
                layer_types.append("layer")
            else:
                layer_types.append("fields")
        if configs['galahSettings']['atlas'] in ["Australia"]:
            # add the types array as another column to the data frame
            dataFrame.insert(loc=3, column='type', value=layer_types)
        elif configs['galahSettings']['atlas'] in ["Austria","Brazil","Canada","Estonia","France","Guatemala","Sweden","United Kingdom"]:
            dataFrame.insert(loc=2, column='type', value=layer_types)
        else:
            raise ValueError("Atlas {} not taken into account".format(configs['galahSettings']['atlas']))
        # append the data frame sorted by type first, then name
        return_array.append(dataFrame.sort_values(['type','name']).reset_index(drop=True))
    elif not fields:
        pass
    else:
        raise ValueError("You can only specify True for fields (default=False)")

    # get all licences from the API
    if type(licences) is bool and licences:
        if configs['galahSettings']['atlas'] in ["Austria","Brazil","Canada","Estonia","France"]:
            raise ValueError("The {} atlas does not have a list of licences".format(configs['galahSettings']['atlas']))
        response = requests.get(get_api_url(column1='called_by', column1value='show_all_licences'))
        if response.status_code == 404:
            raise ValueError("The licences URL for the {} is not working.".format(configs['galahSettings']['atlas']))
        # create a data frame from the API response
        json = pd.DataFrame.from_dict(response.json())
        # append data frame with only the column names 'id', 'name', 'acronym' and 'url'
        return_array.append(json[['id','name','acronym','url']])
    elif not licences:
        pass
    else:
        raise ValueError("You can only specify True for licences (default=False)")

    # get all lists from the API
    if type(lists) is bool and lists:
        if  configs['galahSettings']['atlas'] in ["Canada","Estonia","France","Guatemala","Portugal","Spain","Sweden"]:
            raise ValueError("The {} atlas does not have a lists API.".format(configs['galahSettings']['atlas']))
        for i,maxoffsets in enumerate(["?max=1000&offset=0","?max=1000&offset=1000","?max=1000&offset=2000"]):
            response = requests.get(
                "{}{}".format(get_api_url(column1='called_by', column1value='show_all_lists'),maxoffsets))
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
    elif not lists:
        pass
    else:
        raise ValueError("You can only specify True for lists (default=False)")

    # get all profiles from the API
    if type(profiles) is bool and profiles:
        if configs['galahSettings']['atlas'] == "Australia":
            response = requests.get(get_api_url(column1='called_by', column1value='show_all_profiles'))
            # create a data frame from the API response
            json = pd.DataFrame.from_dict(response.json())
            # append data frame with only the column names 'id', 'name', 'shortName' and 'description'
            return_array.append(json[['id','name','shortName','description']])
        else:
            raise ValueError("Only the Australian atlas has data quality profiles.")
    elif not profiles:
        pass
    else:
        raise ValueError("You can only specify True for profiles (default=False)")

    # get all providers from the API
    if type(providers) is bool and providers:
        response = requests.get(get_api_url(column1='called_by', column1value='show_all_providers'))
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(response.json()))
    elif not providers:
        pass
    else:
        raise ValueError("You can only specify True for providers (default=False)")

    # get all ranks from the API
    if type(ranks) is bool and ranks:
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
    elif not ranks:
        pass
    else:
        raise ValueError("You can only specify True for ranks (default=False)")

    # check for reasons
    if type(reasons) is bool and reasons:
        if  configs['galahSettings']['atlas'] in ["Brazil","Estonia","France"]:
            raise ValueError("The {} atlas does not have a lists API.".format(configs['galahSettings']['atlas']))
        response = requests.get(get_api_url(column1='called_by', column1value='show_all_reasons'))
        # create a data frame from the API response
        json = pd.DataFrame.from_dict(response.json())
        # append data frame with only the column names 'id', 'name', sort values by 'id', and renumber indices
        return_array.append(json[['id','name']].sort_values('id').reset_index(drop=True))
    elif not reasons:
        pass
    else:
        raise ValueError("You can only specify True for reasons (default=False)")

    # if there is only a singular data frame in the return_array, return only this; otherwise, return list
    if len(return_array) == 1:
        return return_array[0]
    return return_array