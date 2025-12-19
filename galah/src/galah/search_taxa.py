import urllib

import pandas as pd
import requests

from .common_checks import check_atlas, check_for_dict, check_taxa_type, check_args_none, check_args_specific_atlas
from .common_dictionaries import (
    ATLAS_KEYWORDS,
    SEARCH_TAXA_ENTRIES,
    SEARCH_TAXA_FIELDS,
    TAXONCONCEPT_NAMES,
    VERNACULAR_NAMES,
)
from .common_functions import print_if_verbose
from .galah_config import get_api_url, readConfig
from .version import __version__


def search_taxa(
    taxa=None, identifiers=None, specific_epithet=None, scientific_name=None, verbose=False, config_file=None
):
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
    configs = readConfig(config_file=config_file)

    # set header
    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # get atlas
    atlas = configs["galahSettings"]["atlas"]
    check_atlas(atlas=atlas, function="search_taxa")

    # make a list of all arguments for checking
    all_args = [identifiers, specific_epithet, scientific_name, taxa]

    # ensure each argument has their specific cases for querying
    all_args_specifics = {
        0: {
            "identifiers": identifiers,
            "column1": "called_by",
            "column1value": "search_identifiers",
            "column2": "api_name",
            "column2value": "names_lookup",
        },  # identifiers
        1: {
            "specific_epithet": specific_epithet,
            "column1": "called_by",
            "column1value": "search_taxa",
            "column2": "api_name",
            "column2value": "names_search_epithet",
        },  # specific_epithet
        2: {
            "scientific_name": scientific_name,
            "column1": "called_by",
            "column1value": "search_taxa",
            "column2": "api_name",
            "column2value": "names_search_epithet",
        },  # scientific_name
    }

    # check for identifiers or specific epithets
    check_args_specific_atlas(
        all_args=[identifiers, specific_epithet], atlas=atlas, specific_atlases=["Australia", "ALA"]
    )
    print("Amanda remember to check the check_args_specific_atlas function")
    import sys

    sys.exit()

    # check to see if all args are None
    check_args_none(all_args=all_args)

    # do some sort of switch statement to
    index = [i for i, x in enumerate(all_args) if x is not None][0]

    # if taxa is None,
    if taxa is None:

        # check to see if arguments are correct
        check_taxa_specifics(dict_of_specifics=all_args_specifics[index])

        # get URL and method
        URL, method = create_search_taxa_url(dict_of_specifics=all_args_specifics[index], config_file=config_file)

        # check to see if the user wants the URL for querying
        print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

        # get the data from API
        response = requests.request(method=method, url=URL, headers=headers)
        response_json = response.json()

        # check for homonyms and other things
        check_for_homonyms(atlas=atlas, response_json=response_json, taxa=taxa)

        # check for lists
        response_json = check_for_lists(response_json=response_json, atlas=atlas)

        # return dataframe
        return pd.DataFrame({k: [response_json[k]] for k in SEARCH_TAXA_FIELDS[atlas]})

    else:

        # check taxa type and turn it into list for easy looping
        taxa = check_taxa_type(taxa=taxa)

        # initialise dataframe
        dataFrame = pd.DataFrame()

        # loop over all taxa (as doing bulk query requires authentication)
        for name in taxa:

            # get base URL for querying
            baseURL, method = get_api_url(
                column1="called_by",
                column1value="search_taxa",
                column2="api_name",
                column2value="names_search_single",
                config_file=config_file,
            )

            # create URL, get result and concatenate result onto dataFrame
            # make sure all the atlases are checked
            URL = baseURL.replace("{name}", "%20".join(name.split(" ")))

            # print URLs if things are verbose
            print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

            # get the response
            response = requests.request(method=method, url=URL, headers=headers)
            response_json = response.json()

            # check for homonyms
            if atlas in ["ALA", "Australia"]:
                check_for_homonyms(atlas=atlas, response_json=response_json, taxa=taxa)

            # check to see if the taxa was successfully returned
            if atlas in ["Australia", "Spain"] and not response_json["success"]:
                print("We were not able to find {} in the {} backbone.".format(taxa, atlas))

            # set default raw_data value
            raw_data_dict = {
                "Australia": response_json,
                "ALA": response_json,
                "Austria": None,
                "Brazil": None,
                "France": None,
                "Guatemala": None,
                "Global": response_json,
                "GBIF": response_json,
                "Portugal": response_json,
                "Spain": response_json,
                "Sweden": response_json,
                "United Kingdom": None,
                "UK": None,
            }

            # get the raw data
            raw_data = check_raw_data(
                raw_data=raw_data_dict[atlas], response_json=response_json, atlas=atlas, name=name
            )

            # if raw_data is None, go to next taxa (potentially put error here)
            # ["Global", "GBIF", "Austria", "UK", "United Kingdom"]
            if atlas in ["Australia", "ALA"] and not raw_data["success"]:
                continue

            data = {}
            if raw_data is not None:
                for k in SEARCH_TAXA_FIELDS[atlas]:
                    if k in raw_data:
                        data[k] = raw_data[k]

            # check if the atlas is GBIF and get vernacular names accordingly
            if atlas in ["Global", "GBIF", "Portugal", "Spain"]:
                data[VERNACULAR_NAMES[atlas][1]] = get_vernacularName(raw_data=raw_data, atlas=atlas)

            # add every taxon to dataframe
            tempdf = pd.DataFrame(data, index=[1])
            dataFrame = pd.concat([dataFrame, tempdf], ignore_index=True)

        # return dataFrame with all data
        return dataFrame


def create_search_taxa_url(dict_of_specifics=None, config_file=None):
    """
    Create a search_taxa URL for either identifiers, specific_epithet or scientific_name.

    Parameters
    ----------
        dict_of_specifics : dict
            Dictionary containing all information needed for building URLs

    Returns
    -------
        URL: str
            string containing URL for querying
        method: str
            method for querying the API URL
    """

    # if keyword correct, add to URL
    baseURL, method = get_api_url(
        column1=dict_of_specifics["column1"],
        column1value=dict_of_specifics["column1value"],
        column2=dict_of_specifics["column2"],
        column2value=dict_of_specifics["column2value"],
        config_file=config_file,
    )

    # create URL based on different case
    if "identifiers" in dict_of_specifics.keys():
        URL = baseURL + "?taxonID=" + urllib.parse.quote(dict_of_specifics["identifiers"])
    if "specific_epithet" in dict_of_specifics.keys():
        URL = process_dicts_to_URLs(baseURL=baseURL, dict_of_specifics=dict_of_specifics, head_key="specific_epithet")
    if "scientific_name" in dict_of_specifics.keys():
        URL = process_dicts_to_URLs(baseURL=baseURL, dict_of_specifics=dict_of_specifics, head_key="scientific_name")

    # return URL and method
    return URL, method


def process_dicts_to_URLs(baseURL=None, dict_of_specifics=None, head_key=None):
    len_key = list(dict_of_specifics[head_key].keys())[0]
    len_dict = len(dict_of_specifics[head_key][len_key])
    end = ""
    for i in range(len_dict):
        end += (
            "&".join(
                "=".join([key, urllib.parse.quote(dict_of_specifics[head_key][key][i])])
                for key in dict_of_specifics[head_key].keys()
            )
            + "&"
        )
    URL = baseURL + "?" + end
    return URL


def check_taxa_specifics(dict_of_specifics=None):
    """
    Checking whether or not the correct terms are used in the dict_of_specifics.

    Parameters
    ----------
        dict_of_specifics : dict
            Dictionary containing all information needed for building URLs

    Returns
    -------
       None
    """
    if "specific_epithet" in dict_of_specifics.keys():

        check_for_dict(variable=dict_of_specifics["specific_epithet"], variable_name="specific_epithet")

        # if keyword is not correct, raise error
        if not any("specificEpithet" in se for se in dict_of_specifics["specific_epithet"]):
            raise ValueError('you need to include a search term titled "specificEpithet"')

        for key in dict_of_specifics["specific_epithet"].keys():
            if not isinstance(dict_of_specifics["specific_epithet"][key], list):
                dict_of_specifics["specific_epithet"][key] = [dict_of_specifics["specific_epithet"][key]]

        check_dict_key_lengths(dict_to_check=dict_of_specifics["specific_epithet"])

    if "scientific_name" in dict_of_specifics.keys():

        check_for_dict(variable=dict_of_specifics["scientific_name"], variable_name="scientific_name")

        # check to see if the correct information and type of variables is available
        if not any("scientificName" in sn for sn in list(dict_of_specifics["scientific_name"].keys())):
            raise ValueError('you need to include a search term titled "scientificName"')

        for key in dict_of_specifics["scientific_name"].keys():
            if not isinstance(dict_of_specifics["scientific_name"][key], list):
                dict_of_specifics["scientific_name"][key] = [dict_of_specifics["scientific_name"][key]]

        check_dict_key_lengths(dict_to_check=dict_of_specifics["scientific_name"])


def check_dict_key_lengths(dict_to_check=None):
    # get length of the arrays in the dictionary
    lens = map(len, dict_to_check.values())
    len_dict = list(set(list(lens)))

    # throw error if dictionary values are not the same length
    if len(len_dict) != 1:
        raise ValueError("All of your dictionary values need to be the same length")


def get_vernacularName(raw_data=None, atlas=None):
    """
    Get all of the vernacular names from GBIF

    Parameters
    ----------
        raw_data : dict
            Raw data from the GBIF API URL

    Returns
    -------
        vernacular_name: dict
            Dictionary containing all the vernacular names
    """
    response_vernacular = requests.get(
        "https://api.gbif.org/v1/species/{}/vernacularNames".format(raw_data[TAXONCONCEPT_NAMES[atlas]["guid"]])
    )
    array_vernacular = response_vernacular.json()["results"]
    vernacular_name = ""
    for item in array_vernacular:
        for key in item.keys():
            if key in VERNACULAR_NAMES[atlas][1]:
                vernacular_name += item[key] + ", "
    vernacular_name = vernacular_name[:-2]
    return vernacular_name


def check_for_homonyms(atlas=None, response_json=None, taxa=None):
    """
    Check for homonyms in the ALA

    Parameters
    ----------
        atlas : dict
            Name of atlas you are querying
        response_json : dict
            Dictionary containing data from the API
        taxa : str,list


    Returns
    -------
        URL: str
            string containing URL for querying
        method: str
            method for querying the API URL
    """
    # check for homonyms
    if not response_json["success"]:
        if "homonym" in response_json["issues"]:
            print("Warning: Search for {} returned multiple taxa due to a homonym issue.".format(taxa))
            print("Please use the `scientific_name` argument to clarify taxa.")
            return pd.DataFrame({"search_term": taxa, "issues": response_json["issues"]})


def check_for_lists(response_json=None, atlas=None):

    # check for any lists in the response_json; if so, make these lists strings
    if any(isinstance(response_json[x], list) for x in SEARCH_TAXA_FIELDS[atlas]):
        field = [x for x in SEARCH_TAXA_FIELDS[atlas] if isinstance(response_json[x], list)]
        for f in field:
            new_value = ",".join(response_json[f])
            response_json[f] = new_value

    # return the new response_json
    return response_json


def check_raw_data(raw_data=None, response_json=None, atlas=None, name=None):

    # check to see if raw_data is None and needs to be filtered through
    if raw_data is None:
        if SEARCH_TAXA_ENTRIES[atlas][0] in response_json:
            for item in response_json[SEARCH_TAXA_ENTRIES[atlas][0]][SEARCH_TAXA_ENTRIES[atlas][1]]:
                if name.lower() == item["scientificName"].lower():
                    return item
    return raw_data


def generate_list_taxonConceptIDs(taxa=None, scientific_name=None, atlas=None):
    """Function for getting more than one taxonConceptIDs"""

    # get the taxonConceptID for taxa while checking for extant atlas
    if scientific_name is not None:
        df_taxa = search_taxa(scientific_name=scientific_name)
        if df_taxa.empty:
            return None
        taxonConceptID = list(df_taxa[ATLAS_KEYWORDS[atlas]])
    else:
        df_taxa = search_taxa(taxa=taxa)
        if df_taxa.empty:
            return None
        taxonConceptID = list(df_taxa[ATLAS_KEYWORDS[atlas]])

    # add taxon IDs to URL, but first check for GBIF
    if atlas in ["Global", "GBIF"]:

        # add using taxonKey
        return "".join(["taxonKey={}&".format(urllib.parse.quote(str(tid))) for tid in taxonConceptID])

    # for Australia
    elif atlas in ["Australia", "ALA"]:

        # add %22
        return (
            "fq=%28lsid%3A%22"
            + "%22%20OR%20lsid%3A%22".join(urllib.parse.quote(str(tid)) for tid in taxonConceptID)
            + "%29"
        )

    else:

        return "fq=%28lsid%3A" + "%20OR%20lsid%3A".join(urllib.parse.quote(str(tid)) for tid in taxonConceptID) + "%29"
