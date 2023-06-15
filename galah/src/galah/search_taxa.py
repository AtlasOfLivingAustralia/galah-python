import requests
import pandas as pd
import urllib

from .get_api_url import get_api_url,readConfig
from .common_dictionaries import SEARCH_TAXA_ENTRIES,SEARCH_TAXA_FIELDS,TAXONCONCEPT_NAMES,VERNACULAR_NAMES,atlases

def search_taxa(taxa=None,
                identifiers=None,
                specific_epithet=None,
                scientific_name=None,
                verbose=False):
    """
    Look up taxonomic names before downloading data from the ALA, using ``atlas_occurrences()``, ``atlas_species()`` or 
    ``atlas_counts()``. Taxon information returned by ``search_taxa()`` may be passed to the ``taxa`` argument of ``atlas`` 
    functions. 
    
    ``search_taxa()`` allows users to disambiguate homonyms (i.e. where the same name refers to taxa in different 
    clades) prior to downloading data.

    Parameters
    ----------
        taxa : string
            one or more scientific names to search.  

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.search_taxa(taxa="Vulpes vulpes")

    .. program-output:: python -c "import galah; print(galah.search_taxa(taxa=\\\"Vulpes vulpes\\\"))"
    """

    # get configuration
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas']

    if identifiers is not None or specific_epithet is not None:
        if "specificEpithet" not in specific_epithet:
            raise ValueError("you need to include a search term titled \"specificEpithet\"")
        if identifiers is not None:
            baseURL = get_api_url(column1='called_by',column1value='search_identifiers',column2='api_name',column2value='names_lookup')
            URL = baseURL + "?taxonID=" + urllib.parse.quote(identifiers)
        elif specific_epithet is not None:
            baseURL = get_api_url(column1='called_by',column1value='search_taxa',column2='api_name',column2value='names_search_multiple')
            URL = baseURL + "?" + "&".join(specific_epithet)
        else:
            raise ValueError("Something isn't right with identifiers or specific_epithet:\nidentifiers: {}\nspecific_epithet: {}\n".format(identifiers,specific_epithet))
        response = requests.get(URL)
        response_json = response.json()
        data={}
        for entry in response_json:
            if entry in SEARCH_TAXA_FIELDS[atlas]:
                if type(response_json[entry]) is str:
                    data[entry] = response_json[entry]
                elif type(response_json[entry]) is list:
                    data[entry] = ", ".join(response_json[entry])
                else:
                    raise ValueError("The type of variable for entry {} is {}".format(entry,type(response_json[entry])))
        return pd.DataFrame(data,index=[0])

    if scientific_name is not None:
        baseURL = get_api_url(column1='called_by',column1value='search_taxa',column2='api_name',column2value='names_search_multiple')
        if "scientificName" not in scientific_name:
            raise ValueError("you need to specify ")
        if type(scientific_name) is not dict:
            raise ValueError("You need to pass a dictionary value to scientific_name")
        lens = map(len,scientific_name.values())
        len_dict = list(set(list(lens)))
        if len(len_dict) != 1:
            raise ValueError("All of your dictionary values need to be the same length")
        df = pd.DataFrame()
        for i in range(len_dict[0]):
            URL = baseURL + "?" + "&".join(["=".join([key,urllib.parse.quote(scientific_name[key][i])]) for key in scientific_name])
            response = requests.get(URL)
            response_json = response.json()
            data={}
            for entry in response_json:
                if entry in SEARCH_TAXA_FIELDS[atlas]:
                    if type(response_json[entry]) is str:
                        data[entry] = response_json[entry]
                    elif type(response_json[entry]) is list:
                        data[entry] = ", ".join(response_json[entry])
                    else:
                        raise ValueError("The type of variable for entry {} is {}".format(entry,type(response_json[entry])))
            df = pd.concat([df,pd.DataFrame(data,index=[0])])
        return df

    # first, check if someone actually entered a taxa name
    if taxa is None:
        raise Exception("You need to specify one of the following:\n\ntaxa\nidentifiers\nspecific_epithet\nscientific_name\n")

    # get base URL for querying
    baseURL = get_api_url(column1='called_by',column1value='search_taxa',column2='api_name',column2value='names_search_single')

    # third, add fq=<search term> and converting it to URL
    if type(taxa) is list or type(taxa) is str:

        # convert to list for easy looping
        if type(taxa) is str:
            taxa=[taxa]

        # create an empty dataframe
        dataFrame = pd.DataFrame()

        # currently only return information above kingdom
        for name in taxa:

            # create URL, get result and concatenate result onto dataFrame
            # make sure all the atlases are checked
            if atlas in atlases:
                URL = baseURL.replace("{name}","%20".join(name.split(" ")))
            else:
                raise ValueError("Atlas {} is not taken into account".format(atlas))
            
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))
        
            # get the response
            response = requests.get(URL)
            response_json = response.json()

            # France was here
            if atlas in ["Sweden"]: # "Austria"
                raw_data = [] #None
                if SEARCH_TAXA_ENTRIES[atlas][0] in response_json:
                    for item in response_json[SEARCH_TAXA_ENTRIES[atlas][0]][SEARCH_TAXA_ENTRIES[atlas][1]]:
                        if name.lower() in item['scientificName'].lower():
                            raw_data = item
                            break
                if raw_data is None:
                    continue
            # still not sure about France but we shall see...
            elif atlas in ["Austria","Brazil","France", "Guatemala"]:
                raw_data = None
                if SEARCH_TAXA_ENTRIES[atlas][0] in response_json:
                    for item in response_json[SEARCH_TAXA_ENTRIES[atlas][0]][SEARCH_TAXA_ENTRIES[atlas][1]]:
                        if name.lower() == item['scientificName'].lower():
                            raw_data = item
                            break
                if raw_data is None:
                    continue
            elif atlas in ["Australia","Global","GBIF","Spain"]:
                raw_data = response_json
                if atlas in ["Global","GBIF"]:
                    response_vernacular = requests.get("https://api.gbif.org/v1/species/{}/vernacularNames".format(raw_data[TAXONCONCEPT_NAMES[atlas]["guid"]]))
                    array_vernacular = response_vernacular.json()['results']
            else:
                raise ValueError("The atlas {} is not taken into account".format(atlas))

            # check to see if the taxa was successfully returned
            if atlas in ["Australia","Spain"] and not response_json['success']:
                continue
            else:
                data={}
                for item in raw_data: 
                    if item in SEARCH_TAXA_FIELDS[atlas]:
                        data[item] = raw_data[item] 
                if atlas in ["Global","GBIF"]:
                    vernacular_name=""
                    for item in array_vernacular:
                        for key in item.keys():
                            if key in SEARCH_TAXA_FIELDS[atlas]:
                                vernacular_name += item[key] + ", "
                    vernacular_name = vernacular_name[:-2]
                    data[VERNACULAR_NAMES[atlas][1]] = vernacular_name

            # add every instance of 
            tempdf = pd.DataFrame(data,index=[1])
            dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

        # return dataFrame with all data
        return dataFrame

    # else, let the user know that the taxa argument can only be a string or a lsit
    else:
        raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: search_taxa(\"Vulpes vulpes\")"
                        "\n         search_taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")