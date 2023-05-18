import requests,urllib.parse
import pandas as pd

from .search_taxa import search_taxa
from .get_api_url import get_api_url,readConfig
from .common_dictionaries import ATLAS_KEYWORDS,DEPTH_STRINGS,FACETS_STRINGS
from .common_dictionaries import TAXONCONCEPT_NAMES,VERNACULAR_NAMES,ATLAS_SPECIES_FIELDS
from .common_functions import add_filters

import sys

# this function looks for all species with the associated name
def atlas_species(taxa=None,filters=None,verbose=False):
    """
    While there are reasons why users may need to check every record meeting their search criteria (i.e. using ``galah.atlas_occurrences()``), 
    a common use case is to simply identify which species occur in a specified region, time period, or taxonomic group. 
    This function returns a ``pandas.DataFrame`` with one row per species, and columns giving associated taxonomic information.

    Parameters
    ----------
        taxa : string / list
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.  
        rank : string
            filters, in the form ``field`` ``logical`` ``value`` (e.g. ``"year=2021"``)
        verbose : 
            If ``True``, galah gives you the URLs used to query all the data.  Default to ``False``.

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        galah.atlas_species(taxa="Heleioporus")

    .. program-output:: python -c "import galah; print(galah.atlas_species(taxa=\\\"Heleioporus\\\"))"
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas'] 

    # first, check if the user has specified a taxa
    if taxa is None:
        raise ValueError("You need to specify a name for this function to work, i.e. \"Heleioporus\"")
    elif type(taxa) is not str and type(taxa) is not list:
        raise ValueError("Only a string or list can be specified for taxa names")

    # get initial url
    if atlas in ["France"]:
        baseURL = get_api_url(column1='called_by',column1value='search_taxa',column2='api_name',column2value='names_search_single')
        baseURL2 = get_api_url(column1='api_name', column1value='records_species')
        #print(search_taxa(taxa)[ATLAS_KEYWORDS[atlas]][0])
    else:
        baseURL = get_api_url(column1='api_name', column1value='records_species')

    # raise warning - not sure how to fix it
    if atlas in ["Spain"]:
        print("There have been some issues getting all species when using a genus name.  Instead, either use a species name or anything of family or higher order.")

    # check if filters are specified
    if filters is not None:

        # check the type of variable filters is
        if type(filters) is list or type(filters) is str:

            # add filters to URL
            URL = add_filters(URL=URL,atlas=atlas,filters=filters)

        # else, make sure that the filters is in the following format
        else:
            raise TypeError("filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")
    else:

        # get base URL for querying
        URL = baseURL + "?"

        # do a check for France
        if atlas in ["France"]:
            URL2 = baseURL2 + "?"
    
     # get the taxonConceptID for taxa
    if atlas in ["Australia","Austria","Brazil","Global","GBIF","Spain"]:
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS[atlas]][0]
        URL += "&fq=%28lsid%3A" + urllib.parse.quote(str(taxonConceptID)) + "%29&facets={}".format(FACETS_STRINGS[atlas])
    # do a check for subspecies France - do I needthis?
    elif atlas in ["France"]:
        URL = baseURL.replace("{name}",taxa)
        taxonConceptID = search_taxa(taxa)[ATLAS_KEYWORDS[atlas]][0]
        URL2 += "&fq=%28lsid%3A" + urllib.parse.quote(str(taxonConceptID)) + "%29&facets={}".format(FACETS_STRINGS[atlas])
    else:
        raise ValueError("Atlas {} is not taken into account".format(atlas))

    # check to see if user wants the query URL
    if verbose:
        print("URL for querying:\n\n{}\n".format(URL))

    # get url and transform from a text string to a list
    response = requests.get(URL)
    all_ids = []
    # check to see which has more entries?
    if atlas in ["France"]:
        response_json = response.json()
        response2 = requests.get(URL2)
        all_ids2 = response2.text[1:-2].split('"\n"')[1:]
        for entry in response_json[DEPTH_STRINGS[atlas]]['taxa']:
            if taxa.lower() in entry['scientificName'].lower() and taxa.lower() != entry['scientificName'].lower():
                all_ids.append(entry['scientificName'])
        if len(all_ids2) > len(all_ids):
            all_ids = all_ids2
    else:
        all_ids = response.text[1:-2].split('"\n"')[1:]

    # need to get species, author and other things
    temp_data_dict = {"species": [], "author": [], "species_guid": []}
    temp_data_dict2 = {entry:[] for entry in ATLAS_SPECIES_FIELDS[atlas]}
    temp_data_dict3 = {"vernacular_name": []}
    data_dict = temp_data_dict | temp_data_dict2 | temp_data_dict3
    
    # species_lookup for each individual species
    # names_search_single is for APIs without namematching service
    if atlas in ["Austria","France"]:
        baseURL = get_api_url(column1='api_name', column1value='names_search_single')
    else:
        baseURL = get_api_url(column1='api_name', column1value='species_lookup')

    # get all the taxonomic information for every species ID
    for species_guid in all_ids:

        # check for atlas
        if atlas in ["Brazil","Spain"]:
            URL = baseURL + "/" + urllib.parse.quote(species_guid)
        elif atlas in ["Australia"]:
            URL = baseURL.replace("{id}", urllib.parse.quote(species_guid))
        elif atlas in ["Austria","France"]:
            URL = baseURL.replace("{name}", urllib.parse.quote(species_guid))
        else:
            raise ValueError("Atlas {} is not taken into account".format(atlas))

        # check to see if user wants the query URL
        if verbose:
            print("URL for querying:\n\n{}\n".format(URL))

        # get response from the API
        response = requests.get(URL)
        response_json = response.json()
        
        # set up arrays to loop over for different atlases
        if atlas in ["Austria"]:
            array_depth = response_json[DEPTH_STRINGS[atlas]]['results'] 
            array_others = response_json[DEPTH_STRINGS[atlas]]['results'] 
            array_vernacular = response_json[DEPTH_STRINGS[atlas]]['results']
        elif atlas in ["France"]:
            array_depth = response_json[DEPTH_STRINGS[atlas]]['taxa']
            array_others = response_json[DEPTH_STRINGS[atlas]]['taxa']
            array_vernacular = response_json[DEPTH_STRINGS[atlas]]['taxa']
        else:
            array_depth = response_json[DEPTH_STRINGS[atlas]]
            array_others = response_json['taxonConcept']
            if VERNACULAR_NAMES[atlas][0] in response_json:
                if response_json[VERNACULAR_NAMES[atlas][0]]:
                    array_vernacular = response_json[VERNACULAR_NAMES[atlas][0]]
                else:
                    array_vernacular = []
            else:
                array_vernacular = []

        # now look for species and author
        for others in TAXONCONCEPT_NAMES[atlas].keys(): #['species','author','species_guid']:
            if array_others and type(array_others) is list:
                for entry in array_others:
                    if atlas in ["France"] and entry[TAXONCONCEPT_NAMES[atlas]['species']].lower() != species_guid.lower():
                        pass
                    else:
                        if TAXONCONCEPT_NAMES[atlas][others] in entry and entry[TAXONCONCEPT_NAMES[atlas][others]] is not None:
                            if type(entry[TAXONCONCEPT_NAMES[atlas][others]]) is not str:
                                data_dict[others].append(entry[TAXONCONCEPT_NAMES[atlas][others]])
                            elif type(entry[TAXONCONCEPT_NAMES[atlas][others]]) is str:
                                data_dict[others].append(entry[TAXONCONCEPT_NAMES[atlas][others]].lower().capitalize())
                            else:
                                data_dict[others].append("")
                        else:
                            data_dict[others].append("")
            elif type(array_others) is list:
                for entry in array_others:
                    if TAXONCONCEPT_NAMES[atlas][others] in array_others and array_others[TAXONCONCEPT_NAMES[atlas][others]] is not None:
                        if type(entry[others]) is not str: # try this
                            data_dict[others].append(entry[TAXONCONCEPT_NAMES[atlas][others]])
                        elif type(entry[TAXONCONCEPT_NAMES[atlas][others]]) is str:
                            data_dict[others].append(entry[TAXONCONCEPT_NAMES[atlas][others]].lower().capitalize())
                        else:
                            data_dict[others].append("")
                    else:
                        data_dict[others].append("")
            elif type(array_others) is dict:
                if TAXONCONCEPT_NAMES[atlas][others] in array_others and array_others[TAXONCONCEPT_NAMES[atlas][others]] is not None:
                    if type(array_others[TAXONCONCEPT_NAMES[atlas][others]]) is not str: # try this
                        data_dict[others].append(array_others[TAXONCONCEPT_NAMES[atlas][others]])
                    elif type(array_others[TAXONCONCEPT_NAMES[atlas][others]]) is str:
                        data_dict[others].append(array_others[TAXONCONCEPT_NAMES[atlas][others]].lower().capitalize())
                    else:
                        data_dict[others].append("")
                else:
                        data_dict[others].append("")
            else:
                data_dict[others].append("")

        # now, check for higher orders
        for depth in ATLAS_SPECIES_FIELDS[atlas]:
            if array_depth and type(array_depth) is list:
                for entry in array_depth:
                    if atlas in ["France"] and entry[TAXONCONCEPT_NAMES[atlas]['species']].lower() != species_guid.lower():
                        pass
                    else:      
                        if depth in entry and entry[depth] is not None:
                            if type(entry[depth]) is not str:
                                data_dict[depth].append(entry[depth])
                            elif type(entry[depth]) is str:
                                data_dict[depth].append(entry[depth].lower().capitalize())
                            else:
                                data_dict[depth].append("")
                        else:
                            data_dict[depth].append("") 
            elif array_depth:
                if depth in array_depth and array_depth[depth] is not None:
                        data_dict[depth].append(array_depth[depth].lower().capitalize())
                else:
                    data_dict[depth].append("")
            else:
                data_dict[depth].append("")

        # get common names (vernacular names)
        if array_vernacular and type(array_vernacular) is list:
            
            # do a check for Austria and France
            if len(array_vernacular) > 1 and atlas in ["Austria","France"]:
                for entry in array_vernacular:
                    if atlas in ["France"] and entry[TAXONCONCEPT_NAMES[atlas]['species']].lower() != species_guid.lower():
                        pass
                    else:
                        vernacular_name_string = ""
                        if entry[VERNACULAR_NAMES[atlas][1]] is not None and entry[VERNACULAR_NAMES[atlas][1]] is not "":
                            if entry[VERNACULAR_NAMES[atlas][1]] not in vernacular_name_string:
                                vernacular_name_string += entry[VERNACULAR_NAMES[atlas][1]] + ", "
                        vernacular_name_string = vernacular_name_string[:-2]
                        data_dict["vernacular_name"].append(vernacular_name_string)
            # all other atlases fall under this
            elif len(array_vernacular) > 1 and atlas not in ["Austria","France"]:
                vernacular_name_string = ""
                for entry in array_vernacular:
                    if entry[VERNACULAR_NAMES[atlas][1]] is not None and entry[VERNACULAR_NAMES[atlas][1]] is not "":
                        if entry[VERNACULAR_NAMES[atlas][1]] not in vernacular_name_string:
                            vernacular_name_string += entry[VERNACULAR_NAMES[atlas][1]] + ", "
                vernacular_name_string = vernacular_name_string[:-2]
                data_dict["vernacular_name"].append(vernacular_name_string)
            else:
                data_dict["vernacular_name"].append(array_vernacular[0][VERNACULAR_NAMES[atlas][1]])
        elif array_vernacular:
            print(type(array_vernacular))
            print(array_vernacular)
            raise ValueError("This loop needs to be written.")
        else:
            data_dict["vernacular_name"].append("")

    # index any extra or faulty entries in the dictionary
    indexes_to_delete = []
    for i,entry in enumerate(data_dict['species']):
        if taxa.lower() not in entry.lower():
            indexes_to_delete.append(i)

    # remove these entries from dictionary
    for index in reversed(indexes_to_delete):
        for key in data_dict.keys():
            del(data_dict[key][index])

    # return data as a pandas dataframe
    return pd.DataFrame.from_dict(data_dict)