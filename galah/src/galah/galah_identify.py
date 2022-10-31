import galah,os,configparser
import pandas as pd

def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

'''
Function comments here

arguments: one or more scientific names (search=True) or taxonomic identifiers
               (search=False)
def galah_identify([arguments here], search=True):
'''
def galah_identify(taxa=None, search=True):

    # check to see if taxa is set to None; if so, throw ValueError
    if taxa is None:
        return ValueError("You need to specify a taxa for this function to work, i.e. \"Heleioporus\"")

    # get config file options
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig()
    specific_atlas = atlaslist[atlaslist['atlas'] == configs['galahSettings']['atlas']]
    print(specific_atlas)

    # download sound, images etc.
    identify_rows = specific_atlas[specific_atlas['called_by'] == 'galah_identify']
    index = identify_rows[identify_rows['called_by'] == "galah_identify"].index[0]
    baseURL = "{}?".format(identify_rows[identify_rows['called_by'] == 'galah_identify']['api_url'][index])
    print(baseURL)

    # taxonID, api_name = names_lookup, called_by = search_identifiers
    # searchByClassification, called_by == search_taxa, api_name = names_search_multiple
    # determine which of the three namematching URLs I need to use

    # use name_search_single for this function

    #if search=True, look for scientific names
    if search:
        n=1
    #if search=False, look for taxonomic names
    else:
        n=1

