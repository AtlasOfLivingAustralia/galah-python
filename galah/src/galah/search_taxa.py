import urllib

import pandas as pd
import requests

from .common_dictionaries import SEARCH_TAXA_ENTRIES, SEARCH_TAXA_FIELDS, TAXONCONCEPT_NAMES, VERNACULAR_NAMES
from .common_functions import check_atlas_in_atlases, check_taxa_type, get_api_url, print_if_verbose
from .galah_config import readConfig
from .version import __version__


def search_taxa(
    taxa=None,
    identifiers=None,
    specific_epithet=None,
    scientific_name=None,
    verbose=False,
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
    configs = readConfig()

    # set header
    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # get atlas
    atlas = configs["galahSettings"]["atlas"]

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
    if any(x is not None for x in [identifiers, specific_epithet, scientific_name]) and atlas not in [
        "Australia",
        "ALA",
    ]:
        raise ValueError("identifiers and specific_epithet are only available for the Australian atlas.")

    # check to see if all args are None
    if all(x is None for x in all_args):
        raise ValueError(
            "You need to specify one of the following:\n\ntaxa\nidentifiers\nspecific_epithet\nscientific_name\n"
        )

    # do some sort of switch statement to
    index = [i for i, x in enumerate(all_args) if x is not None][0]

    # get the URLs
    check_atlas_in_atlases(atlas=atlas, func="search_taxa")

    # if taxa is None,
    if taxa is None:

        # check to see if arguments are correct
        check_taxa_specifics(dict_of_specifics=all_args_specifics[index])

        # get URL and method
        URL, method = create_search_taxa_url(dict_of_specifics=all_args_specifics[index])

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
            )

            # create URL, get result and concatenate result onto dataFrame
            # make sure all the atlases are checked
            URL = baseURL.replace("{name}", "%20".join(name.split(" ")))

            # print URLs if things are verbose
            print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

            # get the response
            response = requests.request(method=method, url=URL, headers=headers)
            response_json = response.json()

            # check to see if the taxa was successfully returned
            if atlas in ["Australia", "Spain"] and not response_json["success"]:
                continue

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
            print(raw_data)

            # if raw_data is None, go to next taxa (potentially put error here)
            if raw_data is None:
                continue

            # loop over data
            data = {k: raw_data[k] for k in SEARCH_TAXA_FIELDS[atlas]}

            # check if the atlas is GBIF and get vernacular names accordingly
            if atlas in ["Global", "GBIF", "Portugal", "Spain"]:
                data[VERNACULAR_NAMES[atlas][1]] = get_vernacularName(raw_data=raw_data, atlas=atlas)

            # add every taxon to dataframe
            tempdf = pd.DataFrame(data, index=[1])
            dataFrame = pd.concat([dataFrame, tempdf], ignore_index=True)

        # return dataFrame with all data
        return dataFrame


def create_search_taxa_url(dict_of_specifics=None):
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
    )

    # create URL based on different case
    if "identifiers" in dict_of_specifics.keys():
        URL = baseURL + "?taxonID=" + urllib.parse.quote(dict_of_specifics["identifiers"])
    if "specific_epithet" in dict_of_specifics.keys():
        URL = baseURL + "?" + "&".join(dict_of_specifics["specific_epithet"])
    if "scientific_name" in dict_of_specifics.keys():
        len_key = list(dict_of_specifics["scientific_name"].keys())[0]
        len_dict = len(dict_of_specifics["scientific_name"][len_key])
        end = ""
        for i in range(len_dict):
            end += (
                "&".join(
                    "=".join([key, urllib.parse.quote(dict_of_specifics["scientific_name"][key][i])])
                    for key in dict_of_specifics["scientific_name"].keys()
                )
                + "&"
            )
        URL = baseURL + "?" + end

    # return URL and method
    return URL, method


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

        # if keyword is not correct, raise error
        if not any("specificEpithet" in se for se in dict_of_specifics["specific_epithet"]):
            raise ValueError('you need to include a search term titled "specificEpithet"')

    if "scientificName" in dict_of_specifics.keys():

        # check to see if the correct information and type of variables is available
        if not any("scientificName" in sn for sn in list(dict_of_specifics["scientific_name"].keys())):
            raise ValueError('you need to include a search term titled "scientificName"')
        elif type(dict_of_specifics["scientific_name"]) is not dict:
            raise ValueError("You need to pass a dictionary value to scientific_name")

        # get length of the arrays in the dictionary
        lens = map(len, dict_of_specifics["scientific_name"].values())
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
    if atlas in ["Australia", "ALA"] and not response_json["success"]:
        if "homonym" in response_json["issues"]:
            print("Warning: Search returned multiple taxa due to a homonym issue.")
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
