import galah,requests,urllib.parse,configparser,os,html
import pandas as pd

from .search_taxa import search_taxa

import sys

def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

# this function looks for all species with the associated name
### TODO: comment
def atlas_species(taxa=None,verbose=False):

    # first, check if the user has specified a taxa
    if taxa is None:
        return ValueError("You need to specify a species name for this function to work, i.e. \"Heleioporus\"")
    elif type(taxa) is not str:
        return ValueError("You can only specify one species name for this function so far, i.e. \"Heleioporus\"")

    # get configuration for atlas to query
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig()
    specific_atlas = atlaslist[atlaslist['atlas'] == configs['galahSettings']['atlas']]

    # call galah_identify (or search_taxa for now?) to do something
    # species_lookup
    media_rows = specific_atlas[specific_atlas['api_name'] == 'species_children']
    index = media_rows[media_rows['api_name'] == "species_children"].index[0]
    baseURL = media_rows[media_rows['api_name'] == 'species_children']['api_url'][index]

    # search taxonomic trees
    taxonConceptID = search_taxa(taxa)['taxonConceptID'][0]
    URL = baseURL.replace("{id}",taxonConceptID) # + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"

    # check to see if user wants the query URL
    if verbose:
        print("URL for querying:\n\n{}\n".format(URL))

    # get url and print response
    response = requests.get(URL)
    # need to get species, author and
    json = response.json()
    temp_dict = {"species": [], "author": [], "species_guid": []}
    for j in json:
        dataFrame = pd.DataFrame(j,index=[0])
        if dataFrame['rank'][0] == "species":
            temp_dict['species'].append(dataFrame['name'][0])
            temp_dict['author'].append(dataFrame['author'][0])
            temp_dict['species_guid'].append(dataFrame['guid'][0])

    # create the dataFrame
    dataFrame = pd.DataFrame.from_dict(temp_dict)

    # get all of the taxonomic information
    # species_lookup
    media_rows = specific_atlas[specific_atlas['api_name'] == 'species_lookup']
    index = media_rows[media_rows['api_name'] == "species_lookup"].index[0]
    baseURL = media_rows[media_rows['api_name'] == 'species_lookup']['api_url'][index]

    # search taxonomic trees
    taxonConceptID = search_taxa(taxa)['taxonConceptID'][0]
    URL = baseURL.replace("{id}",taxonConceptID)

    # check to see if user wants the query URL
    if verbose:
        print("URL for querying:\n\n{}\n".format(URL))

    # now get all of the taxonomic classifications
    response = requests.get(URL)
    json = response.json()
    for i,depth in enumerate(['kingdom','phylum','class','order','family']):
        dataFrame.insert(loc=i, column=depth, value=json['classification'][depth].lower().capitalize())

    # lastly, get vernacular names
    vernacular_names = []
    for url in dataFrame['species_guid']:
        response = requests.get(url)
        if response.status_code == 404:
            new_url = response.url.split(";")[0]
            new_response = requests.get(new_url)
            if new_response.status_code == 200:
                found_common_name=False
                for line in new_response.iter_lines():
                    if found_common_name:
                        common_name = str(line).replace("b'                 <h3>","")
                        common_name = common_name.replace("</h3>'","")
                        vernacular_names.append(common_name)
                        found_common_name=False
                    if "afdCommonNames" in str(line):
                        found_common_name=True
        elif response.status_code == 200:
            found_common_name = False
            for line in response.iter_lines():
                if found_common_name:
                    common_name = str(line).replace("b'                 <h3>", "")
                    common_name = common_name.replace("</h3>'", "")
                    vernacular_names.append(common_name)
                    found_common_name = False
                if "afdCommonNames" in str(line):
                    found_common_name = True
        else:
            raise Error("This URL is not working: {}".format(url))

    # add value to data frame
    dataFrame.insert(loc=dataFrame.shape[1], column='vernacular_names', value=vernacular_names)

    # return the dataFrame
    return dataFrame