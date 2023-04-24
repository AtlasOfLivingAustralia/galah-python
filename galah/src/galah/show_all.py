import requests,os
import pandas as pd

from .get_api_url import get_api_url
from .get_api_url import readConfig

'''
function is meant to show all values for possible query fields - they are defined as a boolean variable so you can see
the large list of all the potential variables to add to your atlas query.
'''
def show_all(assertions=False,
             atlases=False,
             apis=False,
             collection=False,
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
    The living atlases store a huge amount of information, above and beyond the occurrence records that are their main output. 
    In galah, one way that users can investigate this information is by showing all the available options or categories for the 
    type of information they are interested in. ``show_all()`` is a helper function that can display multiple types of information, 
    displaying all valid options for the information specified.

    Parameters
    ----------
        assertions : logical
            Show results of data quality checks run by each atlas  
        atlases : logical
            Show what atlases are available
        apis : logical
            Show what APIs & functions are available for each atlas
        collection : logical
            Show the specific collections within those institutions
        datasets : logical
            Shows all the data groupings within those collections 
        fields : logical
            Show fields that are stored in an atlas
        licences : logical
            Show what copyright licenses are applied to media
        lists : logical
            Show what species lists are available
        profiles : logical
            Show what data profiles are available
        providers : logical
            Show which institutions have provided data
        ranks : logical
            Show valid taxonomic ranks (e.g. Kingdom, Class, Order, etc.)
        reasons : logical
            Show what values are acceptable as 'download reasons' for a specified atlas

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.show_all(datasets=True)

    .. program-output:: python -c "import galah; print(galah.show_all(datasets=True))"
    """

    # get configurations for different atlases
    configs = readConfig()

    # set up the option for getting back multiple values
    return_array=[]

    # check for assertions boolean
    if type(assertions) is bool and assertions:
        if configs['galahSettings']['atlas'] in ["Australia","Brazil","Spain"]:
            response = requests.get(get_api_url(column1='called_by',column1value='show_all-assertions'))
        else:
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
        '''
         "atlas": ["Australia","Austria","Brazil","Canada","Estonia","France","Guatemala","Portugal","Spain","Sweden","United Kingdom"],
            "institution": ["Atlas of Living Australia","Biodiversitäts-Atlas Österreich","Sistemas de Informações sobre a Biodiversidade Brasileira",
                            "Canadensys", "eElurikkus","Inventaire National du Patrimoine Naturel","Sistema Nacional de Información sobre Diversidad Biológica de Guatemala",
                            "GBIF Portugal","GBIF Spain","Swedish Biodiversity Data Infrastructure","National Biodiversity Network"],
            "acronym": ["ALA","BAO","SiBBr","<NA>","<NA>","INPN","SNIBgt","GBIF.pt","GBIF.es","SBDI","NBN",],
            "url": ["https://www.ala.org.au","https://biodiversityatlas.at","https://sibbr.gov.br","http://www.canadensys.net/",
                    "https://elurikkus.ee","https://inpn.mnhn.fr","https://snib.conap.gob.gt","https://www.gbif.pt",
                    "https://www.gbif.es","https://biodiversitydata.se","https://nbn.org.uk"],
        '''
        data = {
            "atlas": ["Australia","Brazil","Spain"],
            "institution": ["Atlas of Living Australia","Sistemas de Informações sobre a Biodiversidade Brasileira",
                            "GBIF Spain"],
            "acronym": ["ALA","SiBBr","GBIF.es"],
            "url": ["https://www.ala.org.au","https://sibbr.gov.br","https://www.gbif.es"],
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

    # check for collection
    if type(collection) is bool and collection:
        if configs['galahSettings']['atlas'] in ["Australia","Brazil","Spain"]:
            response = requests.get(get_api_url(column1='called_by',column1value='show_all-collections'))
        else:
            response = requests.get(get_api_url(column1='called_by', column1value='show_all_collections'))
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(response.json()))
    elif not collection:
        pass
    else:
        raise ValueError("You can only specify True for collection (default=False)")

    # check for datasets
    if type(datasets) is bool and datasets:
        if configs['galahSettings']['atlas'] in ["Australia","Brazil","Spain"]:
            response = requests.get(get_api_url(column1='called_by',column1value='show_all-datasets'))
        else:
            response = requests.get(get_api_url(column1='called_by', column1value='show_all_datasets'))
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(response.json()))
    elif not datasets:
        pass
    else:
        raise ValueError("You can only specify True for datasets (default=False)")

    # get all fields from the API
    if type(fields) is bool and fields:

        # get all possible fields
        if configs['galahSettings']['atlas'] in ["Australia","Brazil","Spain"]:
            response = requests.get(get_api_url(column1='called_by',column1value='show_all-fields',column2='api_name',column2value='records_fields'))
            fields_values = pd.DataFrame.from_dict(response.json())

            # remove anything with "Contextual" or "Environmental" from the options for Australian atlas
            ### TODO: Check for Spanish and Brazilian atlases
            if configs['galahSettings']['atlas'] in ["Australia","Brazil","Spain"]:
                fields_values = fields_values[~fields_values["classs"].astype(str).str.contains("Contextual|Environmental")]

            # select only the columns titled 'name', 'info', (and) 'infoUrl'
            if configs['galahSettings']['atlas'] in ["Australia","Spain"]:
                fields_select = fields_values[['name', 'info', 'infoUrl']]
                dataFrame = fields_select.rename(columns={"name": "id","info": "description", "infoUrl": "link"})
                dataFrame.insert(loc=2,column="type", value="field")
            elif configs['galahSettings']['atlas'] in ["Austria","Brazil","Canada","Estonia","France","Guatemala","Sweden","United Kingdom"]:
                fields_select = fields_values[['name', 'info']]
                dataFrame = fields_select.rename(columns={"name": "id","info": "description"}) #, inplace=True)
                dataFrame["type"] = "field"
                dataFrame["link"] = ""
        
        else:
            raise ValueError("Atlas {} not taken into account.".format(configs['galahSettings']['atlas']))
        
        # second: get spatial layers
        if configs['galahSettings']['atlas'] in ["Australia","Spain"]:
            # get data from API
            response = requests.get(get_api_url(column1='called_by',column1value='show_all-fields',column2='api_name',column2value='spatial_layers'))
            spatial_values = pd.DataFrame.from_dict(response.json())
            spatial_layers = pd.DataFrame()

            # select only the columns titled 'name', 'info', (and) 'infoUrl'
            if configs['galahSettings']['atlas'] in ["Australia","Spain"]:
                # build layer id from this
                spatial_values["type"].replace("Contextual","cl",inplace=True)
                spatial_values["type"].replace("Environmental","el",inplace=True)
                spatial_layers["id"] =  spatial_values["type"].astype(str) + spatial_values["id"].astype(str)
                # build descriptions from these
                spatial_layers["description"] = spatial_values['displayname'] + " " + spatial_values['description']
                spatial_layers["type"] = "layers"
                spatial_layers["link"] = ""
            elif configs['galahSettings']['atlas'] in ["Austria","Brazil","Canada","Estonia","France","Guatemala","Sweden","United Kingdom"]:
                layers_select = spatial_values[['name', 'info']]
                spatial_layers = layers_select.rename(columns={"name": "id","info": "description"})
                spatial_layers["type"] = "layers"
                spatial_layers["link"] = ""
            else:
                raise ValueError("Atlas {} not taken into account".format(configs['galahSettings']['atlas']))
        
        # Australia has more things than other atlases; take that into account
        if configs['galahSettings']['atlas'] in ["Australia","Spain"]:

            # third: get media
            media_values = pd.DataFrame.from_dict({"id": ["multimedia", "multimediaLicence", "images", "videos", "sounds"], "description": "Media filter field","type": "media","link": ""})

            # fourth: get other fields 
            other_field_values = pd.DataFrame({"id": "qid", "description": "Reference to pre-generated query", "type": "other", "link": ""},index=[0])
        
            # create final dataframe
            return_dataFrame = pd.concat([dataFrame,spatial_layers,media_values,other_field_values],ignore_index=True)

            # reset index
            return_dataFrame.reset_index(drop = True, inplace = True)

            # return final dataframe to user
            return_array.append(return_dataFrame)

        # else: only return fields dataframe
        else:

            # reset index
            dataFrame.reset_index(drop = True, inplace = True)

            # return final thing
            return_array.append(dataFrame)

    elif not fields:
        pass
    else:
        raise ValueError("You can only specify True for fields (default=False)")

    # get all licences from the API
    if type(licences) is bool and licences:
        if configs['galahSettings']['atlas'] in ["Austria","Canada","Estonia","France"]:
            raise ValueError("The {} atlas does not have a list of licences".format(configs['galahSettings']['atlas']))
        elif configs['galahSettings']['atlas'] in ["Australia","Spain"]:
            response = requests.get(get_api_url(column1='called_by',column1value='show_all-licences'))
        elif configs['galahSettings']['atlas'] in ["Brazil"]:
            raise ValueError("Brazil has an API endpoint for licences, but it is empty.")
        else:
            response = requests.get(get_api_url(column1='called_by', column1value='show_all_licences'))
        if response.status_code == 404:
            raise ValueError("The licences URL for the {} atlas is not working.".format(configs['galahSettings']['atlas']))
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
        if  configs['galahSettings']['atlas'] in ["Canada","Estonia","France","Guatemala","Portugal","Sweden"]:
            raise ValueError("The {} atlas does not have a lists API.".format(configs['galahSettings']['atlas']))
        for i,maxoffsets in enumerate(["?max=1000&offset=0","?max=1000&offset=1000","?max=1000&offset=2000"]):
            if configs['galahSettings']['atlas'] in ["Australia","Brazil","Spain"]:
                response = requests.get(get_api_url(column1='called_by',column1value='show_all-lists'))
            else:
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
        if configs['galahSettings']['atlas'] in ["Australia","Spain"]:
            response = requests.get(get_api_url(column1='called_by',column1value='show_all-profiles'))
            json = pd.DataFrame.from_dict(response.json())
            # append data frame with only the column names 'id', 'name', 'shortName' and 'description'
            if configs['galahSettings']['atlas'] in ["Spain"]:
                print("WARNING: The Spanish atlas has data quality profiles, but they are not yet linked to the biocache yet")
            return_array.append(json[['id','name','shortName','description']])
        else:
            raise ValueError("Only the Australian atlas has data quality profiles you can use.")
    elif not profiles:
        pass
    else:
        raise ValueError("You can only specify True for profiles (default=False)")

    # get all providers from the API
    if type(providers) is bool and providers:
        if configs['galahSettings']['atlas'] in ["Australia","Brazil","Spain"]:
            response = requests.get(get_api_url(column1='called_by',column1value='show_all-providers'))
        else:
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
        if configs["galahSettings"]["ranks"] == "all":
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
            # add this in with configuration file
            # short ranks dictionary
        elif configs["galahSettings"]["ranks"] == "gbif":
            gbif_ranks = {
                'id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                'name': ["kingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies", "infraspecific"]
            }
        else:
            raise ValueError("For ranks, you can only have two values currently:\n\nall: all possible ranks\ngbif: only the nine major ranks\n")
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(all_ranks))
    elif not ranks:
        pass
    else:
        raise ValueError("You can only specify True for ranks (default=False)")

    # check for reasons
    if type(reasons) is bool and reasons:
        if  configs['galahSettings']['atlas'] in ["Brazil","Estonia","France"]:
            raise ValueError("The {} atlas does not have a reasons API.".format(configs['galahSettings']['atlas']))
        elif configs['galahSettings']['atlas'] in ["Australia","Spain"]:
            response = requests.get(get_api_url(column1='called_by',column1value='show_all-reasons'))
        else:
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