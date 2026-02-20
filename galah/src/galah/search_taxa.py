import json
import urllib

import pandas as pd
import requests

from .common_checks import (
    check_args_none,
    check_args_specific_atlas,
    check_atlas,
    check_atlas_authenticate,
    check_for_dict,
    check_for_non_working_atlases,
    check_taxa_type,
)
from .common_dictionaries import (
    ATLAS_KEYWORDS,
    SEARCH_TAXA_ENTRIES,
    SEARCH_TAXA_FIELDS,
    TAXONCONCEPT_NAMES,
    VERNACULAR_NAMES,
)
from .common_functions import print_if_verbose, set_bool_argument
from .galah_config import get_api_url, readConfig
from .version import __version__


def search_taxa(taxa=None, identifiers=None, specific_epithet=None, scientific_name=None, config_file=None):
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

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.search_taxa(specific_epithet={\\\"class\\\":\\\"aves\\\",\\\"family\\\":\\\"pardalotidae\\\",\\\"genus\\\":\\\"pardalotus\\\",\\\"specificEpithet\\\":\\\"punctatus\\\"}))"

    Search taxonomic levels by using the key word "scientificName"

    .. prompt:: python

        import galah
        galah.search_taxa(scientific_name={"family": ["pardalotidae","maluridae"],"scientificName": ["pardolatus striatus","malurus cyaneus"]})

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.search_taxa(scientific_name={\\\"family\\\": [\\\"pardalotidae\\\",\\\"maluridae\\\"],\\\"scientificName\\\": [\\\"pardolatus striatus\\\",\\\"malurus cyaneus\\\"]}))"
    """

    # ---------------------------------------------------------------------------------------------
    # Declare all variables, run checks on compatibility of arguments.
    # ---------------------------------------------------------------------------------------------

    # get configuration
    configs = readConfig(config_file=config_file)

    # set header
    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # get args from config
    atlas = configs["galahSettings"]["atlas"]
    verbose = set_bool_argument(arg=configs["galahSettings"]["verbose"], name_arg="verbose")
    timeout = int(configs["galahSettings"]["timeout"])
    authenticate = set_bool_argument(arg=configs["galahSettings"]["authenticate"], name_arg="authenticate")
    access_token = configs["galahSettings"]["access_token"]
    client_id = configs["galahSettings"]["client_id"]

    # run checks to see if atlas is valid, as well as the options with it
    check_for_non_working_atlases(atlas=atlas)
    check_atlas(atlas=atlas, function="search_taxa")
    check_atlas_authenticate(atlas=atlas, authenticate=authenticate)

    # ---------------------------------------------------------------------------------------------
    # Put arguments in specific order to check which argument the user has specified
    # ---------------------------------------------------------------------------------------------

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
    specific_args = [identifiers, specific_epithet]
    names_specific_args = ["identifiers", "specific_epithet"]
    check_args_specific_atlas(
        all_args=specific_args, names_all_args=names_specific_args, atlas=atlas, specific_atlases=["Australia", "ALA"]
    )

    # check to see if all args are None
    all_args = [identifiers, specific_epithet, scientific_name, taxa]
    names_all_args = ["identifiers", "specific_epithet", "scientific_name", "taxa"]
    check_args_none(all_args=all_args, names_all_args=names_all_args)

    # get index of type of taxa you are searching for
    index = [i for i, x in enumerate(all_args) if x is not None][0]

    # ---------------------------------------------------------------------------------------------
    # After argument has been determined, get information from the database on the taxa
    # ---------------------------------------------------------------------------------------------

    if taxa is None:

        # check to see if arguments are correct
        check_taxa_specifics(dict_of_specifics=all_args_specifics[index])

        # get URL and method
        URL, method = create_search_taxa_url(dict_of_specifics=all_args_specifics[index], config_file=config_file)

        # check to see if the user wants the URL for querying
        print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

        # get the data from API
        response = requests.request(method=method, url=URL, headers=headers, timeout=timeout)
        response_json = response.json()

        # check for homonyms and other thingsio
        check_for_homonyms(atlas=atlas, response_json=response_json, taxa=taxa)

        # check for lists
        response_json = check_for_lists(response_json=response_json, atlas=atlas)

        # compile dataframe
        return_dict = {}
        for k in SEARCH_TAXA_FIELDS[atlas]:
            if k in response_json:
                return_dict[k] = [response_json[k]]

        # return dataframe
        return pd.DataFrame(return_dict)

    else:

        # check taxa type and turn it into list for easy looping
        taxa = check_taxa_type(taxa=taxa)

        # initialise dataframe
        dataFrame = pd.DataFrame()

        # if the person has authentication set to True, do more efficient query
        if authenticate:

            return authenticate_bulk_query(taxa=taxa, access_token=access_token, client_id=client_id, verbose=verbose)

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
            response = requests.request(method=method, url=URL, headers=headers, timeout=timeout)
            response_json = response.json()

            # check for homonyms
            check_for_homonyms(atlas=atlas, response_json=response_json, taxa=taxa)

            # check to see if the taxa was successfully returned
            check_for_success_AU_ES(atlas=atlas, response_json=response_json, taxa=taxa)

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
                "Kew": None,
                "Portugal": response_json,
                "Spain": response_json,
                "Sweden": response_json,
                "United Kingdom": None,
                "UK": None,
            }

            if atlas in ["Flanders"]:
                data = {}
                if "key" in response_json["usage"]:
                    data["taxonConceptID"] = response_json["usage"]["key"]
                if "name" in response_json["usage"]:
                    data["scientificName"] = response_json["usage"]["name"]
                if "authorship" in response_json["usage"]:
                    data["scientificNameAuthorship"] = response_json["usage"]["authorship"]
                if "rank" in response_json["usage"]:
                    data["taxonRank"] = response_json["usage"]["rank"]
                for entry in response_json["classification"]:
                    rank = entry["rank"].lower().capitalize()
                    data[rank] = entry["name"]

            else:

                # get the raw data
                raw_data = check_raw_data(
                    raw_data=raw_data_dict[atlas], response_json=response_json, atlas=atlas, name=name
                )

                # if raw_data is None, go to next taxa (potentially put error here)
                # ["Global", "GBIF", "Austria", "UK", "United Kingdom"]
                if atlas in ["Australia", "ALA"] and not raw_data["success"]:
                    continue

                # get the data from the raw_data
                data = {}
                if raw_data is not None:
                    for k in SEARCH_TAXA_FIELDS[atlas]:
                        if k in raw_data:
                            data[k] = raw_data[k]

                # check if the atlas is GBIF and get vernacular names accordingly
                if atlas in ["Global", "GBIF", "Portugal", "Spain"]:
                    data[VERNACULAR_NAMES[atlas][1]] = get_vernacularName(
                        raw_data=raw_data, atlas=atlas, timeout=timeout
                    )

            # add every taxon to dataframe
            tempdf = pd.DataFrame(data, index=[1])
            dataFrame = pd.concat([dataFrame, tempdf], ignore_index=True)

        # return dataFrame with all data
        return dataFrame


###################################################################################################
# Functions that other galah functions use uses
###################################################################################################


def generate_list_taxonConceptIDs(taxa=None, scientific_name=None, atlas=None, authenticate=False):
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

        if authenticate:
            return taxonConceptID

        # add %22
        return (
            "fq=%28lsid%3A%22"
            + "%22%20OR%20lsid%3A%22".join(urllib.parse.quote(str(tid)) for tid in taxonConceptID)
            + "%29"
        )

    else:

        return "fq=%28lsid%3A" + "%20OR%20lsid%3A".join(urllib.parse.quote(str(tid)) for tid in taxonConceptID) + "%29"


###################################################################################################
# Functions that search_taxa uses
###################################################################################################


def create_search_taxa_url(dict_of_specifics=None, config_file=None):
    """
    Create a search_taxa URL for either identifiers, specific_epithet or scientific_name.
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
    """
    Function for adding information in dicts to the URLs themselves
    """

    # get the length of keys and dicts for looping
    len_key = list(dict_of_specifics[head_key].keys())[0]
    len_dict = len(dict_of_specifics[head_key][len_key])

    # initialise ending of URL
    end = ""

    # add dict information to the end variable
    for i in range(len_dict):
        end += (
            "&".join(
                "=".join([key, urllib.parse.quote(dict_of_specifics[head_key][key][i])])
                for key in dict_of_specifics[head_key].keys()
            )
            + "&"
        )

    # add the information to the URL
    URL = baseURL + "?" + end

    # return the URL for querying
    return URL


def check_taxa_specifics(dict_of_specifics=None):
    """
    Checking whether or not the correct terms are used in the dict_of_specifics.
    """

    # first, check the specific epithet argument
    if "specific_epithet" in dict_of_specifics.keys():

        check_for_dict(variable=dict_of_specifics["specific_epithet"], variable_name="specific_epithet")

        # if keyword is not correct, raise error
        if not any("specificEpithet" in se for se in dict_of_specifics["specific_epithet"]):
            raise ValueError('you need to include a search term titled "specificEpithet"')

        for key in dict_of_specifics["specific_epithet"].keys():
            if not isinstance(dict_of_specifics["specific_epithet"][key], list):
                dict_of_specifics["specific_epithet"][key] = [dict_of_specifics["specific_epithet"][key]]

        check_dict_key_lengths(dict_to_check=dict_of_specifics["specific_epithet"])

    # then, check scientific name argument
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
    """
    Checking whether or not the length of all the dictionary elements are the same.
    """

    # get length of the arrays in the dictionary
    lens = map(len, dict_to_check.values())
    len_dict = list(set(list(lens)))

    # throw error if dictionary values are not the same length
    if len(len_dict) != 1:
        raise ValueError("All of your dictionary values need to be the same length")


def get_vernacularName(raw_data=None, atlas=None, timeout=600):
    """
    Get all of the vernacular names from GBIF
    """

    # get the response from the GBIF vernacular names endpoint
    response_vernacular = requests.get(
        "https://api.gbif.org/v1/species/{}/vernacularNames".format(raw_data[TAXONCONCEPT_NAMES[atlas]["guid"]]),
        timeout=timeout,
    )

    # get the array of vernacular names
    array_vernacular = response_vernacular.json()["results"]

    # initialise the vernacular names string
    vernacular_name = ""

    # loop over the array and only add the information that's in the accepted names for this atlas
    for item in array_vernacular:
        for key in item.keys():
            if key in VERNACULAR_NAMES[atlas][1]:
                vernacular_name += item[key] + ", "

    # remove the trailing comma and space
    vernacular_name = vernacular_name[:-2]

    # return this string
    return vernacular_name


def check_for_homonyms(atlas=None, response_json=None, taxa=None):
    """
    Check for homonyms in the ALA
    """
    # check for homonyms only for Australia
    if atlas in ["Australia", "ALA"]:
        if not response_json["success"]:
            if "homonym" in response_json["issues"]:
                print("Warning: Search for {} returned multiple taxa due to a homonym issue.".format(taxa))
                print("Please use the `scientific_name` argument to clarify taxa.")
                return pd.DataFrame({"search_term": taxa, "issues": response_json["issues"]})


def check_for_lists(response_json=None, atlas=None):
    """
    Check if any information returned by atlases is a list; if so, turn these lists into strings
    """

    # check for any lists in the response_json; if so, make these lists strings
    for x in SEARCH_TAXA_FIELDS[atlas]:
        if x in response_json:
            if isinstance(response_json[x], list):
                # field = [x for x in SEARCH_TAXA_FIELDS[atlas] if isinstance(response_json[x], list)]
                # for f in field:
                new_value = ",".join(response_json[x])
                response_json[x] = new_value

    # return the new response_json
    return response_json


def check_raw_data(raw_data=None, response_json=None, atlas=None, name=None):
    """
    Check if you need to search for raw data
    """

    # check to see if raw_data is None and needs to be filtered through
    if raw_data is None:
        if SEARCH_TAXA_ENTRIES[atlas][0] in response_json:
            for item in response_json[SEARCH_TAXA_ENTRIES[atlas][0]][SEARCH_TAXA_ENTRIES[atlas][1]]:
                if name.lower() == item["scientificName"].lower():
                    return item

    # otherwise, return the raw data
    return raw_data


def check_for_success_AU_ES(atlas=None, response_json=None, taxa=None):
    """
    Check to see if a name wasn't found either in the Australian or Spanish backbone
    """

    # Check to see if a name wasn't found either in the Australian or Spanish backbone
    if atlas in ["Australia", "Spain"] and not response_json["success"]:
        print("We were not able to find {} in the {} backbone.".format(taxa, atlas))


def authenticate_bulk_query(taxa=None, access_token=None, client_id=None, verbose=None):
    """
    If a person provides a list of species names and they're authenticated, do a bulk query
    """

    # get the baseURL
    baseURL, method = get_api_url(
        column1="called_by",
        column1value="atlas_species",
        column2="api_name",
        column2value="names_search_bulk_species",
    )

    # set up the payload and headers
    payload = {"names": [], "vernacular": "true"}  # , "issues": "true"}
    headers = {
        "User-Agent": "galah-python {}".format(__version__),
        "Authorization": "Bearer {}".format(access_token),
        "client_id": client_id,
        "accept": "*/*",
        "Content-Type": "application/json",
    }
    payload["names"] = taxa

    # print everything if the user has chosen to be verbose with their commands
    print_if_verbose(verbose=verbose, headers=headers, URL=baseURL, method=method, payload=payload)

    # get the list of species data and add it to a dataframe
    species_list = requests.request(method=method, url=baseURL, data=json.dumps(payload), headers=headers)
    species_list_json = species_list.json()
    species_list_dataframe = pd.DataFrame()
    for i in range(len(species_list_json)):
        if all(not isinstance(species_list_json[i][x], list) for x in species_list_json[i]):
            for x in species_list_json[i]:
                species_list_json[i][x] = [species_list_json[i][x]]
        species_list_dataframe = pd.concat([species_list_dataframe, pd.DataFrame(species_list_json[i])])

    # reset the index so everything is sequential
    species_list_dataframe = species_list_dataframe.reset_index(drop=True)
    if species_list_dataframe.empty:
        raise ValueError("There are no taxa with the name(s) {} in the Australian atlas.".format(taxa))

    # rename some of the columns to ensure clarity
    species_list_rename = species_list_dataframe.rename(
        columns={
            "identifier": "taxonConceptID",
            "classs": "class",
            "author": "scientificNameAuthorship",
            "acceptedConceptName": "scientificName",
            "name": "species",
            "commonName": "vernacularName",
        }
    )

    # test this
    if species_list_rename.shape[0] > 1:

        # combine multiple vernacular names into one entry
        species_list_rename = (
            species_list_rename.groupby(
                [
                    "scientificName",
                    "scientificNameAuthorship",
                    "taxonConceptID",
                    "rank",
                    "kingdom",
                    "phylum",
                    "class",
                    "order",
                    "family",
                    "genus",
                    "species",
                ]
            )
            .agg({"vernacularName": ", ".join})
            .reset_index()
        )

    # return the species list
    return species_list_rename[
        [
            "scientificName",
            "scientificNameAuthorship",
            "taxonConceptID",
            "rank",
            "kingdom",
            "phylum",
            "class",
            "order",
            "family",
            "genus",
            "species",
            "vernacularName",
        ]
    ]
