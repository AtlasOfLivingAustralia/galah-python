import requests,urllib.parse,math
import pandas as pd

from .search_taxa import search_taxa
from .get_api_url import get_api_url,readConfig
from .atlas_occurrences import atlas_occurrences
from .common_dictionaries import ATLAS_KEYWORDS,ATLAS_RANKS,DEPTH_STRINGS,FRANCE_TRANSLATION_RANKS
from .common_dictionaries import VERNACULAR_NAMES,ATLAS_SPECIES_FIELDS,TAXONCONCEPT_NAMES,FRANCE_FIELDS
from .common_functions import add_filters,add_predicates

import sys

# this function looks for all species with the associated name
def atlas_species(taxa=None,
                  rank="species",
                  filters=None,
                  verbose=False):
    """
    While there are reasons why users may need to check every record meeting their search criteria (i.e. using ``galah.atlas_occurrences()``), 
    a common use case is to simply identify which species occur in a specified region, time period, or taxonomic group. 
    This function returns a ``pandas.DataFrame`` with one row per species, and columns giving associated taxonomic information.

    Parameters
    ----------
        taxa : string / list
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.  
        rank : string
            the rank you ultimately want to get names for, i.e. "genus" or "species"
        filters : string
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
    if type(taxa) is not str and type(taxa) is not list and taxa is not None:
        raise ValueError("Only a string or list can be specified for taxa names")

    # check to see if rank is in possible ranks for atlas
    if rank.lower() not in ATLAS_SPECIES_FIELDS[atlas]:
        raise ValueError("{} is not a valid rank for the {} atlas.  Possible ranks are:\n\n{}\n".format(rank,atlas,", ".join(ATLAS_SPECIES_FIELDS[atlas])))

    # get initial url
    if atlas not in ["Global","GBIF"]:
        baseURL = get_api_url(column1='api_name', column1value='records_species')
    else:
        # is this correct?
        baseURL = get_api_url(column1='api_name', column1value='records_occurrences')

    # raise warning - not sure how to fix it
    if atlas in ["Spain"]:
        print("There have been some issues getting all species when using a genus name.  If genus doesn't work, either use a species name or anything of family or higher order.")
    if atlas in ["Sweden"]:
        print("There have been some issues getting taxonomy from the Swedish atlas, as they don't store names of taxon higher than species.")

    # get the taxonConceptID for taxa
    if atlas in ["Australia","Austria","Brazil","France","Guatemala","Spain","Sweden"]:

        # if there is no taxa, just add question mark
        if taxa is None:
            
            URL = baseURL + "?"

        # if there is taxa, add these as fields on the URL
        else:
            taxon_info = search_taxa(taxa)
            if atlas in ["France"]:
                taxon_rank = FRANCE_TRANSLATION_RANKS[taxon_info[ATLAS_RANKS[atlas]][0]]
            else:
                taxon_rank = taxon_info[ATLAS_RANKS[atlas]][0]
            taxonConceptID = taxon_info[ATLAS_KEYWORDS[atlas]][0]
            if atlas in ["Brazil","Spain"] and rank == "subspecies":
                URL = baseURL + "?fq=%28lsid%3A" + urllib.parse.quote(str(taxonConceptID)) # did have fq=
            else:
                URL = baseURL + "?fq=%28lsid%3A" + urllib.parse.quote(str(taxonConceptID)) 
        
        # check if filters are specified
        if filters is not None:

            # check the type of variable filters is
            if type(filters) is list or type(filters) is str:

                # add filters to URL
                if taxa is None:
                    URL = add_filters(URL=URL+"fq=",atlas=atlas,filters=filters) #URL=URL
                    if atlas in ["Brazil","Spain"] and rank == "subspecies":
                    # get base URL for querying
                        URL += "&facets={}".format("subspecies_name")
                    else:
                        URL += "&facets={}".format(rank)
                else:
                    URL = add_filters(URL=URL+"%20AND%20",atlas=atlas,filters=filters)
                    if atlas in ["Brazil","Spain"] and rank == "subspecies":
                    # get base URL for querying
                        URL += "%29&facets={}".format("subspecies_name")
                    else:
                        URL += "%29&facets={}".format(rank)

            # else, make sure that the filters is in the following format
            else:
                raise TypeError("filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")
        
        else:
            
            # get base URL for querying
            if atlas in ["Brazil","Spain"] and rank == "subspecies":
                URL += "%29&facets={}".format("subspecies_name")
            else:
                URL += "%29&facets={}".format(rank)
        
        # check to see if user wants the query URL
        if verbose:
            print("URL for querying:\n\n{}\n".format(URL))

        # get url and transform from a text string to a list
        response = requests.get(URL)
        all_ids = response.text[1:-2].split('"\n"')[1:]
        print(sorted(all_ids)[:2])
        
    elif atlas in ["Global","GBIF"]:
        taxon_info = search_taxa(taxa)
        taxon_rank = taxon_info[ATLAS_RANKS[atlas]][0].lower()
        test_list = atlas_occurrences(taxa=taxa,filters=filters,species_list=True,verbose=verbose)
        all_ids = list(set(test_list['species']))
        all_ids = [id for id in all_ids if str(id) != "NaN" and str(id) != "nan"]
    else:
        raise ValueError("Atlas {} is not taken into account".format(atlas))

    # check if ids couldn't be found
    if not all_ids:
        if atlas in ["France"]:
            rank_name = FRANCE_TRANSLATION_RANKS[taxon_info[ATLAS_RANKS[atlas]][0]]
        else:
            taxon_info[ATLAS_RANKS[atlas]][0]
        raise ValueError("galah couldn't find any {} for your chosen taxa {}, which is a {}.".format(rank,taxa,taxon_info[ATLAS_RANKS[atlas]][0]))
    
    # need to get species, author and other things
    index = ATLAS_SPECIES_FIELDS[atlas].index(rank) + 1
    temp_data_dict = {entry:[] for entry in ATLAS_SPECIES_FIELDS[atlas][:index]}
    temp_data_dict2 = {"vernacular_name": [], "author": [], "guid": []}
    data_dict = {**temp_data_dict, **temp_data_dict2}
    
    # species_lookup for each individual species
    # names_search_single is for APIs without namematching service
    if atlas in ["Austria","France","Global","GBIF","Guatemala","Sweden"]:
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
        elif atlas in ["Austria","France","Global","GBIF","Guatemala","Sweden"]:
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
        if atlas in ["Austria","Guatemala","Sweden"]:
            array_depth = response_json[DEPTH_STRINGS[atlas]]['results'] 
            array_others = response_json[DEPTH_STRINGS[atlas]]['results'] 
            array_vernacular = response_json[DEPTH_STRINGS[atlas]]['results']
        elif atlas in ["France"]:
            array_depth = response_json[DEPTH_STRINGS[atlas]]['taxa']
            array_others = response_json[DEPTH_STRINGS[atlas]]['taxa']
            array_vernacular = response_json[DEPTH_STRINGS[atlas]]['taxa']
        elif atlas in ["Global","GBIF"]:
            array_depth = response_json
            array_others = response_json
            response_vernacular = requests.get("https://api.gbif.org/v1/species/{}/vernacularNames".format(response_json[TAXONCONCEPT_NAMES[atlas]["guid"]]))
            array_vernacular = response_vernacular.json()['results']
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
        for others in TAXONCONCEPT_NAMES[atlas].keys(): 
            if type(array_others) is list:
                for entry in array_others:
                    if TAXONCONCEPT_NAMES[atlas][others] in entry and entry[TAXONCONCEPT_NAMES[atlas][others]] is not None:
                        if type(entry[TAXONCONCEPT_NAMES[atlas][others]]) is not str:
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
        for depth in ATLAS_SPECIES_FIELDS[atlas][:index]:
            if atlas in ["France"]:
                atlas_depth = FRANCE_FIELDS[depth]
            else:
                atlas_depth = depth
            if type(array_depth) is list:
                for entry in array_depth:
                    # was atlas_depth with entry and "for atlas_depth in entry"
                    if atlas_depth in entry and entry[ATLAS_RANKS[atlas]] is not None and entry [ATLAS_RANKS[atlas]] is not "None":
                        if type(entry[atlas_depth]) is not str:
                            data_dict[depth].append(entry[atlas_depth])
                        elif type(entry[atlas_depth]) is str:
                            data_dict[depth].append(entry[atlas_depth].lower().capitalize())
                        else:
                            data_dict[depth].append("")
                    else:
                        if atlas in ["France"]:
                            if atlas_depth == FRANCE_TRANSLATION_RANKS[entry[ATLAS_RANKS[atlas]]]:
                                data_dict[depth].append(entry['scientificName'].lower().capitalize())
                            else:
                                data_dict[depth].append("")
                        else:
                            data_dict[depth].append("") 
            elif type(array_depth) is dict:
                if depth in array_depth and array_depth[atlas_depth] is not None:
                    data_dict[depth].append(array_depth[atlas_depth].lower().capitalize())
                else:
                    data_dict[depth].append("")
            else:
                data_dict[depth].append("")

        # get common names (vernacular names)
        if array_vernacular and type(array_vernacular) is list:

            # do a check for Austria and France
            if len(array_vernacular) > 1 and atlas in ["Austria","France","Guatemala","Sweden"]:
                for entry in array_vernacular:
                    vernacular_name_string = ""
                    if VERNACULAR_NAMES[atlas][1] in entry:
                        if entry[VERNACULAR_NAMES[atlas][1]] is not None and entry[VERNACULAR_NAMES[atlas][1]] is not "":
                            if entry[VERNACULAR_NAMES[atlas][1]] not in vernacular_name_string:
                                vernacular_name_string += entry[VERNACULAR_NAMES[atlas][1]] + ", "
                    vernacular_name_string = vernacular_name_string[:-2]
                    data_dict["vernacular_name"].append(vernacular_name_string)
            # all other atlases fall under this
            elif len(array_vernacular) > 1 and atlas not in ["Austria","France","Guatemala","Sweden"]:
                vernacular_name_string = ""
                for entry in array_vernacular:
                    if entry[VERNACULAR_NAMES[atlas][1]] is not None and entry[VERNACULAR_NAMES[atlas][1]] is not "":
                        if entry[VERNACULAR_NAMES[atlas][1]] not in vernacular_name_string:
                            vernacular_name_string += entry[VERNACULAR_NAMES[atlas][1]] + ", "
                vernacular_name_string = vernacular_name_string[:-2]
                data_dict["vernacular_name"].append(vernacular_name_string)
            else:
                data_dict["vernacular_name"].append(array_vernacular[0][VERNACULAR_NAMES[atlas][1]])
        
        # haven't come across this loop before; write it when I come to it 
        elif array_vernacular:
            if VERNACULAR_NAMES[atlas][1] in array_vernacular:
                data_dict["vernacular_name"].append(array_vernacular[VERNACULAR_NAMES[atlas][1]])
            else:
                data_dict["vernacular_name"].append("")
        # else, no vernacular name
        else:
            data_dict["vernacular_name"].append("")

    # index any extra or faulty entries in the dictionary
    indexes_to_delete = []
    for i,entry in enumerate(data_dict[taxon_rank]): # was 'species', then 'rank'
        if taxa.lower() not in entry.lower() or data_dict[taxon_rank][i] == "":
            indexes_to_delete.append(i)

    #print(indexes_to_delete)

    # remove these entries from dictionary
    for index in reversed(indexes_to_delete):
        for key in data_dict.keys():
            del(data_dict[key][index])

    # return data as a pandas dataframe
    return pd.DataFrame.from_dict(data_dict)