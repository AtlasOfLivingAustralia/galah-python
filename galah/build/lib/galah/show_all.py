import os
import pandas as pd

from .get_api_url import readConfig
from .common_dictionaries import atlases as ATLASES
from .common_functions import get_response_show_all
from .version import __version__

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
             verbose=False
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

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.show_all(datasets=True))"
    """

    # get configurations for different atlases
    configs = readConfig()

    atlas = configs['galahSettings']['atlas']

    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # set up the option for getting back multiple values
    return_array=[]

    # check for assertions boolean
    if type(assertions) is bool and assertions:

        # set returned to False for GBIF
        returned = False

        # then check for GBIF atlas
        if atlas in ["Global","GBIF"]:
            json = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gbif_assertions.csv'))
            json.reset_index(drop=True,inplace=True)
            return_array.append(json)
            returned = True
        elif atlas in ATLASES:
            response = get_response_show_all(column1='called_by',column1value='show_all-assertions',atlas=atlas,headers=headers,verbose=verbose)
        else:
            raise ValueError("Atlas {} not taken into account in galah for assertions.".format(atlas))

        # if the response hasn't been added to the return array, add it here 
        if not returned:

            # get the response in a data frame
            df = pd.DataFrame.from_dict(response.json())

            # set default value for the 'type' column
            df['type'] = assertions

            # append this data frame to the return_array
            return_array.append(df[['name','description','category','type']])
    
    # else, pass 
    elif not assertions:
        pass

    # else, there is an incorrect argument for assertions
    else:
        raise ValueError("You can only specify True for assertions (default=False)")


    # return all the atlases you can query
    if type(atlases) is bool and atlases:

        # dictionary of all atlases galah currently supports
        '''
         "atlas": ["Canada","Estonia","Guatemala","Portugal","Sweden","United Kingdom"],
            "institution": ["Canadensys", "eElurikkus","Sistema Nacional de Información sobre Diversidad Biológica de Guatemala",
                            "GBIF Portugal","Swedish Biodiversity Data Infrastructure","National Biodiversity Network"],
            "acronym": ["<NA>","<NA>","SNIBgt","GBIF.pt","SBDI","NBN",],
            "url": ["http://www.canadensys.net/",
                    "https://elurikkus.ee","https://snib.conap.gob.gt","https://www.gbif.pt",
                    "https://biodiversitydata.se","https://nbn.org.uk"],
        '''

        # data of all the atlases galah currently supports
        data = {
            "atlas": ["Australia","Austria","Brazil","France","Global","Spain"],
            "institution": ["Atlas of Living Australia","Biodiversitäts-Atlas Österreich","Sistemas de Informações sobre a Biodiversidade Brasileira",
                            "Inventaire National du Patrimoine Naturel","Global Biodiversity Information Facility", "GBIF Spain"],
            "acronym": ["ALA","BAO","SiBBr","INPN","GBIF","GBIF.es"],
            "url": ["https://www.ala.org.au","https://biodiversityatlas.at","https://sibbr.gov.br","https://inpn.mnhn.fr","https://gbif.org",
                    "https://www.gbif.es"],
        }

        # append this data frame to the return_array
        return_array.append(pd.DataFrame.from_dict(data))

    # else, user doesn't want atlases
    elif not atlases:
        pass

    # else, user has input something incorrectly
    else:
        raise ValueError("You can only specify True for atlases (default=False)")


    # return all the possible apis you could query
    if type(apis) is bool and apis:

        # append the full atlaslist to return_array
        atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
        atlaslist = pd.read_csv(atlasfile)
        
        # at this atlas list to return array
        return_array.append(atlaslist)
    
    # else, user doesn't want apis
    elif not apis:
        pass
    
    # else, user has input something incorrectly 
    else:
        raise ValueError("You can only specify True for apis (default=False)")


    # check for collection
    if type(collection) is bool and collection:

        # first check for ALA API key
        if atlas in ["Global","GBIF"]:
            raise ValueError("{} atlas does not have a list of collections".format(atlas))
        elif atlas in ATLASES:
            response = get_response_show_all(column1='called_by',column1value='show_all-collections',atlas=atlas,headers=headers,verbose=verbose)
        else:
            raise ValueError("Atlas {} not taken into account in galah for collections.".format(atlas))
        
        # append data frame to return_array
        return_array.append(pd.DataFrame.from_dict(response.json()))

    # user doesn't want collections
    elif not collection:
        pass

    # user has input something incorrectly
    else:
        raise ValueError("You can only specify True for collection (default=False)")


    # check for datasets
    if type(datasets) is bool and datasets:

        if atlas in ["Global","GBIF"]:
            response = get_response_show_all(column1='called_by',column1value='show_all-datasets',atlas=atlas,headers=headers,verbose=verbose)
            datasets_list = pd.DataFrame.from_dict(response.json()['results'])
        elif atlas in ATLASES:
            response = get_response_show_all(column1='called_by',column1value='show_all-datasets',atlas=atlas,headers=headers,verbose=verbose)
            datasets_list = pd.DataFrame.from_dict(response.json())
        else:
            raise ValueError("Atlas {} not taken into account in galah for datasets.".format(atlas))

        # append data frame to return_array
        return_array.append(datasets_list)

    # user doesn't want datasets
    elif not datasets:
        pass

    # user has input something incorrectly
    else:
        raise ValueError("You can only specify True for datasets (default=False)")


    # get all fields from the API
    if type(fields) is bool and fields:

        # get all possible fields
        if atlas not in ["Global","GBIF"]:
            
            # get data from API
            response = get_response_show_all(column1='called_by',column1value='show_all-fields',column2='api_name',column2value='records_fields',atlas=atlas,headers=headers,verbose=verbose)

            # get fields values in a table
            fields_values = pd.DataFrame.from_dict(response.json())

            # remove anything with "Contextual" or "Environmental" from the options for Australian atlas
            if atlas in ["Australia","Brazil","Spain"]:
                fields_values = fields_values[~fields_values["classs"].astype(str).str.contains("Contextual|Environmental")]

            # select only the columns titled 'name', 'info', (and) 'infoUrl'
            if atlas in ["Australia","Spain"]:
                fields_select = fields_values[['name', 'info', 'infoUrl']]
                dataFrame = fields_select.rename(columns={"name": "id","info": "description", "infoUrl": "link"})
                dataFrame.insert(loc=2,column="type", value="field")
            elif atlas in ["Austria","Brazil","Canada","Estonia","France","Guatemala","Sweden","United Kingdom"]:
                fields_select = fields_values[['name', 'info']]
                dataFrame = fields_select.rename(columns={"name": "id","info": "description"}) #, inplace=True)
                dataFrame["type"] = "field"
                dataFrame["link"] = ""

        # check if atlas is GBIF
        elif atlas in ["Global","GBIF"]:
            dataFrame = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gbif_fields.csv'))
        
        # else, atlas not taken into account
        else:
            raise ValueError("Atlas {} not taken into account for fields.".format(atlas))
        
        # second: get spatial layers
        if atlas in ["Australia","Spain"]:
            
            # get data from API
            response = get_response_show_all(column1='called_by',column1value='show_all-fields',column2='api_name',column2value='spatial_layers',atlas=atlas,headers=headers,verbose=verbose)
            
            # process data
            spatial_values = pd.DataFrame.from_dict(response.json())
            spatial_layers = pd.DataFrame()

            # select only the columns titled 'name', 'info', (and) 'infoUrl'
            if atlas in ["Australia","Spain"]:

                # build layer id from this
                spatial_values.loc[spatial_values["type"] == "Contextual","type"] = "cl"
                spatial_values.loc[spatial_values["type"] == "Environmental","type"] = "el"
                spatial_layers["id"] =  spatial_values["type"].astype(str) + spatial_values["id"].astype(str)
                
                # build descriptions from these
                spatial_layers["description"] = spatial_values['displayname'] + " " + spatial_values['description']
                spatial_layers["type"] = "layers"
                spatial_layers["link"] = ""

            # look only into these atlases 
            elif atlas in ["Austria","Brazil","France"]:
                layers_select = spatial_values[['name', 'info']]
                spatial_layers = layers_select.rename(columns={"name": "id","info": "description"})
                spatial_layers["type"] = "layers"
                spatial_layers["link"] = ""

            # else, need to add another atlas
            else:
                raise ValueError("Atlas {} not taken into account for fields".format(atlas))
        
        # Australia has more things than other atlases; take that into account
        if atlas in ["Australia","Spain"]:

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

    # user doesn't want fields
    elif not fields:
        pass

    # else, user input something incorrectly
    else:
        raise ValueError("You can only specify True for fields (default=False)")


    # get all licences from the API
    if type(licences) is bool and licences:

        # check for atlases that don't have licences
        if atlas in ["France","Global","GBIF"]:
            raise ValueError("The {} atlas does not have a list of licences".format(atlas))
        
        # check for atlases that have an endpoint but no data
        elif atlas in ["Austria","Brazil"]:
            raise ValueError("{} has an API endpoint for licences, but it is empty.".format(atlas))
        
        elif atlas not in ATLASES:
            raise ValueError("Atlas {} not taken into account for licences.".format(atlas))
        
        # otherwise, do default call
        else:

            response = get_response_show_all(column1='called_by',column1value='show_all-licences',atlas=atlas,headers=headers,verbose=verbose)
            
        # check to see if this URL is not working
        if response.status_code == 404:
            raise ValueError("The licences URL for the {} atlas is not working.".format(atlas))
        
        # create a data frame from the API response
        json = pd.DataFrame.from_dict(response.json())
        
        # append data frame with only the column names 'id', 'name', 'acronym' and 'url'
        return_array.append(json[['id','name','acronym','url']])
    
    # user doesn't want licences
    elif not licences:
        pass

    # user has input something incorrectly
    else:
        raise ValueError("You can only specify True for licences (default=False)")


    # get all lists from the API
    if type(lists) is bool and lists:
        
        # first, check for APIs that do not have lists
        if  atlas in ["France","GBIF","Global"]:
            raise ValueError("The {} atlas does not have a lists API.".format(atlas))
        
        # then, look for lists and set offsets
        if atlas in ATLASES:
            response = get_response_show_all(column1='called_by',column1value='show_all-lists',atlas=atlas,headers=headers,max_entries=-1,offset=0,verbose=verbose)
        else:
            raise ValueError("Atlas {} not taken into account for lists.".format(atlas))
            
        # get all the lists from 
        df = pd.DataFrame.from_dict(response.json()['lists'])

        if 'dataResourceUid' in df:
            df = df.rename(columns={'dataResourceUid': 'species_list_uid'})
        
        # append data frame to return_array
        return_array.append(df)

    # user doesn't want lists
    elif not lists:
        pass

    # user input something incorrectly
    else:
        raise ValueError("You can only specify True for lists (default=False)")


    # get all profiles from the API
    if type(profiles) is bool and profiles:

        # check for only aPIs that have data quality profiles
        if atlas in ["Australia","Spain"]:

            # get data
            response = get_response_show_all(column1='called_by',column1value='show_all-profiles',atlas=atlas,headers=headers,verbose=verbose)

            # create dataframe
            df = pd.DataFrame.from_dict(response.json())

            # append data frame with only the column names 'id', 'name', 'shortName' and 'description'
            if atlas in ["Spain"]:
                print("WARNING: The Spanish atlas has data quality profiles, but they are not yet linked to the biocache yet")
            
            # return data frame
            return_array.append(df[['id','name','shortName','description']])
        
        # else, raise value error
        else:
            raise ValueError("Only the Australian atlas has data quality profiles you can use.")
        
    # user doesn't want profiles
    elif not profiles:
        pass

    # user has input someting incorrectly
    else:
        raise ValueError("You can only specify True for profiles (default=False)")

    # get all providers from the API
    if type(providers) is bool and providers:
           
        # raise an exception specific to France, as their providers are empty
        if atlas in ["France"]:
            raise ValueError("{} has an API endpoint for providers, but it is empty.".format(atlas))
    
        # check for atlases with providers
        elif atlas in ATLASES:

            # get data
            response = get_response_show_all(column1='called_by',column1value='show_all-providers',atlas=atlas,headers=headers,verbose=verbose)
            
            # make data frame
            if atlas in ["Global","GBIF"]:
                providers_list = pd.DataFrame.from_dict(response.json()['results'])
            else:
                providers_list = pd.DataFrame.from_dict(response.json())
        
        # else, do default call
        else:
            raise ValueError("Atlas {} not taken into account for show_all_lists.".format(atlas))

        # append data frame to return_array
        return_array.append(providers_list)

    # user does nto want providers
    elif not providers:
        pass

    # user input something incorrectly
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
            return_array.append(pd.DataFrame.from_dict(all_ranks))
        
        # check for reduced ranks
        elif configs["galahSettings"]["ranks"] == "gbif":
            gbif_ranks = {
                'id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                'name': ["kingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies", "infraspecific"]
            }
            return_array.append(pd.DataFrame.from_dict(gbif_ranks))
        else:
            raise ValueError("For ranks, you can only have two values currently:\n\nall: all possible ranks\ngbif: only the nine major ranks\n")
        
    # user does not want ranks 
    elif not ranks:
        pass

    # user input something incorrectly
    else:
        raise ValueError("You can only specify True for ranks (default=False)")

    # check for reasons
    if type(reasons) is bool and reasons:

        # check for atlases that don't have a reasons API
        if  atlas in ["Brazil","France","Global","GBIF",]:
            raise ValueError("The {} atlas does not have a reasons API.".format(atlas))
        
        # check for ones that do
        elif atlas in ATLASES:

            # get data
            response = get_response_show_all(column1='called_by',column1value='show_all-reasons',atlas=atlas,headers=headers,verbose=verbose)
            
        # else, do default call
        else:
            raise ValueError("Atlas {} not taken into account for show_all_lists.".format(atlas))
        
        # create a data frame from the API response
        json = pd.DataFrame.from_dict(response.json())

        # append data frame with only the column names 'id', 'name', sort values by 'id', and renumber indices
        return_array.append(json[['id','name']].sort_values('id').reset_index(drop=True))

    # user does not want reasons
    elif not reasons:
        pass

    # user input something incorrectly
    else:
        raise ValueError("You can only specify True for reasons (default=False)")

    # if there is only a singular data frame in the return_array, return only this; otherwise, return list
    if len(return_array) == 1:
        return return_array[0]
    return return_array