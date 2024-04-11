import requests
import pandas as pd
import urllib

from .get_api_url import get_api_url,readConfig
from .common_dictionaries import SEARCH_TAXA_ENTRIES,SEARCH_TAXA_FIELDS,TAXONCONCEPT_NAMES,VERNACULAR_NAMES,atlases
from .version import __version__

# testing
import json

# debugging
import sys

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
        identifiers : string / list
            one or more taxonomic identifiers (such as guid or taxonConceptID) to search.  
        specific_epithet : list
            search taxonomic levels by using the argument "specificEpithet".
        scientific_name : dictionary
            search taxonomic levels by using the argument "scientificName".   
        verbose : logical
            If ``True``, galah gives more information like URLs of your queries. Defaults to ``False``

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    Get taxonomic identifiers for "Vulpes vulpes"

    .. prompt:: python

        import galah
        galah.search_taxa(taxa="Vulpes vulpes")

    .. program-output:: python -c "import galah; print(galah.search_taxa(taxa=\\\"Vulpes vulpes\\\"))"

    Get the species name from a taxonomic identifier

    .. prompt:: python

        import galah
        galah.search_taxa(identifiers="https://id.biodiversity.org.au/node/apni/2914510")

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.search_taxa(identifiers=\\\"https://id.biodiversity.org.au/node/apni/2914510\\\"))"

    Search taxonomic levels by using the key word "specificEpithet"

    .. prompt:: python

        import galah
        galah.search_taxa(specific_epithet=["class=aves","family=pardalotidae","genus=pardalotus","specificEpithet=punctatus"])

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.search_taxa(specific_epithet=[\\\"class=aves\\\",\\\"family=pardalotidae\\\",\\\"genus=pardalotus\\\",\\\"specificEpithet=punctatus\\\"]))"
    
    Search taxonomic levels by using the key word "scientificName"

    .. prompt:: python

        import galah
        galah.search_taxa(scientific_name={"family": ["pardalotidae","maluridae"],"scientificName": ["pardolatus striatus","malurus cyaneus"]})

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.search_taxa(scientific_name={\\\"family\\\": [\\\"pardalotidae\\\",\\\"maluridae\\\"],\\\"scientificName\\\": [\\\"pardolatus striatus\\\",\\\"malurus cyaneus\\\"]}))"
    """

    # get configuration
    configs = readConfig()

    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # get atlas
    atlas = configs['galahSettings']['atlas']

    # check for identifiers or specific epithets
    if identifiers is not None or specific_epithet is not None:

        # first, check if the atlas is Australian; if not, functionality not supported (yet?)
        if atlas in ["Australia","ALA"]:

            # check for specific epithet
            if specific_epithet is not None:

                # if keyword is not correct, raise error
                if not any("specificEpithet" in se for se in specific_epithet):
                    raise ValueError("you need to include a search term titled \"specificEpithet\"")
                
                # if keyword correct, add to URL
                else:
                    baseURL,method = get_api_url(column1='called_by',column1value='search_taxa',column2='api_name',column2value='names_search_multiple')
                    URL = baseURL + "?" + "&".join(specific_epithet)        
            
            # check for identifiers from user
            elif identifiers is not None:
                baseURL, method = get_api_url(column1='called_by',column1value='search_identifiers',column2='api_name',column2value='names_lookup')
                URL = baseURL + "?taxonID=" + urllib.parse.quote(identifiers)
                
            # else, something wasn't put into the argyments correctly
            else:
                raise ValueError("Something isn't right with identifiers or specific_epithet:\nidentifiers: {}\nspecific_epithet: {}\n".format(identifiers,specific_epithet))
        else:
            raise ValueError("identifiers and specific_epithet are only available for the Australian atlas.")
        
        # check to see if the user wants the querying URL
        if verbose:
            print("\nURL being queried:\n\n{}\n".format(URL))

        # get response from URL
        response = requests.request(method,URL,headers=headers)
        
        # get response in form of json
        response_json = response.json()

        # initialise data dictionary
        data={}

        # check for relevant data in response
        for entry in response_json:
            if entry in SEARCH_TAXA_FIELDS[atlas]:
                if type(response_json[entry]) is str:
                    data[entry] = response_json[entry]
                elif type(response_json[entry]) is list:
                    data[entry] = ", ".join(response_json[entry])
                else:
                    raise ValueError("The type of variable for entry {} is {}".format(entry,type(response_json[entry])))
        
        # return data frame with all information
        return pd.DataFrame(data,index=[0])

    # check to see if scientific name was an argument
    if scientific_name is not None:

        # check if they are in the Australian atlas
        if atlas in ["Australia","ALA"]:
            
            # get base URL before adding anything onto it 
            baseURL, method = get_api_url(column1='called_by',column1value='search_taxa',column2='api_name',column2value='names_search_multiple')
            # check to see if the correct information and type of variables is available
            if not any("scientificName" in sn for sn in list(scientific_name.keys())):
                raise ValueError("you need to include a search term titled \"scientificName\"")
            elif type(scientific_name) is not dict:
                raise ValueError("You need to pass a dictionary value to scientific_name")
            
            # get length of the arrays in the dictionary
            lens = map(len,scientific_name.values())
            len_dict = list(set(list(lens)))

            # throw error if dictionary values are not the same length
            if len(len_dict) != 1:
                raise ValueError("All of your dictionary values need to be the same length")
            
            # initialise empty data frame 
            df = pd.DataFrame()

            # loop over all entries in scientific name dictionary and concatenate them to data frame
            for i in range(len_dict[0]):
                URL = baseURL + "?" + "&".join(["=".join([key,urllib.parse.quote(scientific_name[key][i])]) for key in scientific_name])
                response = requests.request(method,URL)
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
            
            # return data frame
            return df
        
        # else, throw error saying this is only avaiable for Australian atlas (now)
        else:
            raise ValueError("scientific_name is only available for the Australian atlas.")

    # first, check if someone actually entered a taxa name
    if taxa is None:
        raise Exception("You need to specify one of the following:\n\ntaxa\nidentifiers\nspecific_epithet\nscientific_name\n")

    # third, add fq=<search term> and converting it to URL
    if type(taxa) is list or type(taxa) is str:

        # convert to list for easy looping
        if type(taxa) is str:
            taxa=[taxa]

        # create an empty dataframe
        dataFrame = pd.DataFrame()

        if atlas in ["Australia"] and len(taxa) > 10:

            baseURL, method = get_api_url(column1='called_by',column1value='atlas_species',column2='api_name',column2value='names_search_bulk_species')
            payload = {"vernacular":"true", "names": [], "issues": "true"}
            payload["names"] = taxa #[" OR ".join("lsid:{}".format(id) for id in taxa)]
            species_list_test = requests.request(method,baseURL,data=json.dumps(payload))
            #print(species_list_test.text)
            species_list_json = species_list_test.json()
            species_list_dataframe = pd.DataFrame(species_list_json)
            species_list_rename = species_list_dataframe.rename(columns={
                'identifier': 'taxonConceptID',
                'classs': 'class',
                'author': 'scientificNameAuthorship',
                'acceptedConceptName': 'scientificName',
                'name': 'species',
                'commonName': 'vernacularName'
            })
            return species_list_rename[['scientificName', 'scientificNameAuthorship', 'taxonConceptID','rank','kingdom', 
                  'phylum', 'class', 'order', 'family', 'genus', 'species','vernacularName']]

        else:
        
            for name in taxa:
                
                # get base URL for querying
                baseURL, method = get_api_url(column1='called_by',column1value='search_taxa',column2='api_name',column2value='names_search_single')

                # create URL, get result and concatenate result onto dataFrame
                # make sure all the atlases are checked
                if atlas in atlases:
                    URL = baseURL.replace("{name}","%20".join(name.split(" ")))
                else:
                    raise ValueError("Atlas {} is not taken into account".format(atlas))
                
                if verbose:
                    print("\nURL being queried:\n\n{}\n".format(URL))
            
                # get the response
                response = requests.request(method=method,url=URL,headers=headers)
                response_json = response.json()

                if atlas in ["Australia","ALA"] and not response_json["success"]:
                    if "homonym" in response_json["issues"]:
                        print("Warning: Search returned multiple taxa due to a homonym issue.")
                        print("Please use the `scientific_name` argument to clarify taxa.")
                        return pd.DataFrame({"search_term": taxa, "issues": response_json["issues"]})

                # check for Austrian, Brazilian, French or Guatemalan atlas
                elif atlas in ["Austria","Brazil","France", "Guatemala","United Kingdom","UK"]: # try UK here
                    raw_data = None
                    if SEARCH_TAXA_ENTRIES[atlas][0] in response_json:
                        for item in response_json[SEARCH_TAXA_ENTRIES[atlas][0]][SEARCH_TAXA_ENTRIES[atlas][1]]:
                            if name.lower() == item['scientificName'].lower():
                                raw_data = item
                                break
                    if raw_data is None:
                        continue
                
                # check for Australian, Global, or Spanish atlas
                elif atlas in ["Australia","Global","GBIF","Spain","Sweden"]: # try Sweden here
                    raw_data = response_json
                    if atlas in ["Global","GBIF"]:
                        response_vernacular = requests.get("https://api.gbif.org/v1/species/{}/vernacularNames".format(raw_data[TAXONCONCEPT_NAMES[atlas]["guid"]]))
                        array_vernacular = response_vernacular.json()['results']
                
                # else, throw an error saying this atlas is not taken into account
                else:
                    raise ValueError("The atlas {} is not taken into account".format(atlas))

                # check to see if the taxa was successfully returned
                if atlas in ["Australia","Spain"] and not response_json['success']:
                    continue

                # process information and put it into a data frame
                else:

                    # initialise dictionary
                    data={}

                    # loop over data
                    for item in raw_data: 
                        if item in SEARCH_TAXA_FIELDS[atlas]:
                            data[item] = raw_data[item] 

                    # check if the atlas is GBIF and get vernacular names accordingly
                    if atlas in ["Global","GBIF"]:
                        vernacular_name=""
                        for item in array_vernacular:
                            for key in item.keys():
                                if key in SEARCH_TAXA_FIELDS[atlas]:
                                    vernacular_name += item[key] + ", "
                        vernacular_name = vernacular_name[:-2]
                        data[VERNACULAR_NAMES[atlas][1]] = vernacular_name

                # add every taxon to dataframe
                tempdf = pd.DataFrame(data,index=[1])
                dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

            # return dataFrame with all data
            return dataFrame

    # else, let the user know that the taxa argument can only be a string or a list
    else:
        raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: search_taxa(\"Vulpes vulpes\")"
                        "\n         search_taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")