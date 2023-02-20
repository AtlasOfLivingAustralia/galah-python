import requests,urllib.parse,os
import pandas as pd

from .search_taxa import search_taxa
from .get_api_url import get_api_url
from .get_api_url import readConfig

import sys

ATLAS_KEYWORDS = {
    "Australia": "taxonConceptID",
    "Austria": "guid",
    "Brazil": "guid", 
    "Canada": "usageKey",
    "Estonia": "guid",
    "France": "usageKey",
    "Guatemala": "guid",
    "Portugal": "usageKey",
    "Spain": "taxonConceptID",
    "Sweden": "guid",
    "United Kingdom": "guid",
}

VERNACULAR_NAMES = {
    "Australia": ["commonNames","nameString"],
    "Austria": "",
    "Brazil": ["commonNames","nameString"], 
    "Canada": "",
    "Estonia": "",
    "France": "",
    "Guatemala": "",
    "Portugal": "",
    "Spain": "",
    "Sweden": "",
    "United Kingdom": "",
}


# this function looks for all species with the associated name
### TODO: comment
def atlas_species(taxa=None,rank="species",verbose=False):
    """
    Used for getting occurrence data for your species.  To get occurrences for

    To know how many total records are in your chosen atlas, type

    .. prompt:: python

        import galah
        galah.atlas_species(taxa="Heleioporus")

    which returns

    .. program-output:: python -c "import galah; print(galah.atlas_species(taxa=\\\"Heleioporus\\\"))"
    """

    # get configs
    configs = readConfig()

    # first, check if the user has specified a taxa
    if taxa is None:
        return ValueError("You need to specify a species name for this function to work, i.e. \"Heleioporus\"")
    elif type(taxa) is not str:
        return ValueError("You can only specify one species name for this function so far, i.e. \"Heleioporus\"")

    # call galah_identify (or search_taxa for now?) to do something
    baseURL = get_api_url(column1='api_name',column1value='species_children')

    # get the taxonConceptID for taxa
    if configs['galahSettings']['atlas'] in ["Australia"]:
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS[configs['galahSettings']['atlas']]][0]
        URL = baseURL.replace("{id}", taxonConceptID)  # + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
    elif configs['galahSettings']['atlas'] in ["Spain"]: #### TODO
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS[configs['galahSettings']['atlas']]][0]
        URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
    elif configs['galahSettings']['atlas'] in ["Brazil"]:
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS[configs['galahSettings']['atlas']]][0]
        URL = baseURL + urllib.parse.quote(taxonConceptID) #+ "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
    else:
        raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

    # check to see if user wants the query URL
    if verbose:
        print("URL for querying:\n\n{}\n".format(URL))

    # get url and print response
    response = requests.get(URL)
    # need to get species, author and
    json = response.json()
    data_dict = {"species": [], "author": [], "species_guid": [], "kingdom": [],"phylum": [],
                 "class": [],"order": [],"family": [], "vernacular_name": []}
    for j in json:
        if j['rank'] == "species":
            data_dict['species'].append(j['name'])
            data_dict['author'].append(j['author'])
            data_dict['species_guid'].append(j['guid'])

    # species_lookup
    baseURL = get_api_url(column1='api_name', column1value='species_lookup')
    #print(baseURL)

    # get all the taxonomic information for every species ID
    for species_guid in data_dict["species_guid"]:
        
        # check for atlas
        if configs['galahSettings']['atlas'] in ["Brazil","Spain"]:
            URL = baseURL + "/" + urllib.parse.quote(species_guid)
        elif configs['galahSettings']['atlas'] in ["Australia"]:
            URL = baseURL.replace("{id}", species_guid)
        else:
            raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

        # get response from the API
        response = requests.get(URL)
        json = response.json()

        # get taxonomic information
        for depth in ['kingdom','phylum','class','order','family']:
            data_dict[depth].append(json['classification'][depth].lower().capitalize())

        # get common names (vernacular names)
        if json[VERNACULAR_NAMES[configs['galahSettings']['atlas']][0]]:
            data_dict["vernacular_name"].append(
                json[VERNACULAR_NAMES[configs['galahSettings']['atlas']][0]][0][VERNACULAR_NAMES[configs['galahSettings']['atlas']][1]])
        else:
            data_dict["vernacular_name"].append("")

    # return data as a pandas dataframe
    return pd.DataFrame.from_dict(data_dict)
    '''
    # search taxonomic trees
    # get the taxonConceptID for taxa
    if configs['galahSettings']['atlas'] in ["Australia"]:
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS["Australia"]][0]
        URL = baseURL.replace("{id}", taxonConceptID)  # + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
    elif configs['galahSettings']['atlas'] in ["Spain"]: ### needs to be redone
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS["Spain"]][0]
        URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
    elif configs['galahSettings']['atlas'] in ["Brazil"]:
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS["Brazil"]][0]
        URL = baseURL + "/" + urllib.parse.quote(taxonConceptID)  # + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
    else:
        raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

    # check to see if user wants the query URL
    if verbose:
        print("URL for querying:\n\n{}\n".format(URL))

    # now get all of the taxonomic classifications
    response = requests.get(URL)
    json = response.json()
    for i,depth in enumerate(['kingdom','phylum','class','order','family']):
        dataFrame.insert(loc=i, column=depth, value=json['classification'][depth].lower().capitalize())

    # lastly, get vernacular names
    # vernacular names not working for: Austria,
    #vernacular_AU = 'species_guid'
    vernacular_names = []
    # doesn't appear to exist for Austria but will double check
    if configs['galahSettings']['atlas'] in ["Australia"]:
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
                raise ValueError("This URL is not working: {}".format(url))

        # add value to data frame
        dataFrame.insert(loc=dataFrame.shape[1], column='vernacular_names', value=vernacular_names)

elif :
    # get all of the taxonomic information
    # species_lookup
    baseURL = get_api_url(column1='api_name', column1value='species_lookup')
    '''
    # return the dataFrame
    return dataFrame