import os

import pandas as pd
import requests

from .common_dictionaries import atlases as ATLASES
from .common_functions import get_api_url, print_if_verbose
from .galah_config import readConfig
from .version import __version__


def show_all(
    assertions=False,
    atlases=False,
    apis=False,
    collection=False,
    datasets=False,
    fields=False,
    licences=False,
    lists=False,
    profiles=False,
    providers=False,
    ranks=False,
    reasons=False,
    verbose=False,
):
    """
    The living atlases store a huge amount of information, above and beyond the occurrence records that are their main output.
    In galah, one way that users can investigate this information is by showing all the available options or categories for the
    type of information they are interested in. ``show_all()`` is a helper function that can display multiple types of information,
    displaying all valid options for the information specified.

    Parameters
    ----------
        assertions : logical
            Show results of data quality checks run by each atlas
        atlases : logical
            Show what atlases are available
        apis : logical
            Show what APIs & functions are available for each atlas
        collection : logical
            Show the specific collections within those institutions
        datasets : logical
            Shows all the data groupings within those collections
        fields : logical
            Show fields that are stored in an atlas
        licences : logical
            Show what copyright licenses are applied to media
        lists : logical
            Show what species lists are available
        profiles : logical
            Show what data profiles are available
        providers : logical
            Show which institutions have provided data
        ranks : logical
            Show valid taxonomic ranks (e.g. Kingdom, Class, Order, etc.)
        reasons : logical
            Show what values are acceptable as 'download reasons' for a specified atlas

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.show_all(datasets=True)

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.show_all(datasets=True))"
    """

    # get configurations for different atlases
    configs = readConfig()

    atlas = configs["galahSettings"]["atlas"]

    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # set up the option for getting back multiple values
    return_array = []

    # options in list
    options = {
        "assertions": [assertions, show_all_assertions],
        "atlases": [atlases, show_all_atlases],
        "apis": [apis, show_all_apis],
        "collection": [collection, show_all_collections],
        "datasets": [datasets, show_all_datasets],
        "fields": [fields, show_all_fields],
        "licences": [licences, show_all_licences],
        "lists": [lists, show_all_lists],
        "profiles": [profiles, show_all_profiles],
        "providers": [providers, show_all_providers],
        "ranks": [ranks, show_all_ranks],
        "reason": [reasons, show_all_reasons],
    }

    # check for
    if not all(type(options[x][0]) is bool for x in options):
        raise ValueError("Only True and False values are accepted in the show_all() function.")

    # Now, go through all options
    for o in options.keys():
        if options[o][0]:
            if o in ["atlases", "apis", "ranks"]:
                return_array.append(options[o][1]())
            else:
                return_array.append(options[o][1](atlas=atlas, headers=headers, verbose=verbose))

    # if there is only a singular data frame in the return_array, return only this; otherwise, return list
    if len(return_array) == 1:
        return return_array[0]
    return return_array


def get_response_show_all(
    column1=None,
    column1value=None,
    column2=None,
    column2value=None,
    atlas=None,
    headers={},
    max_entries=-1,
    offset=None,
    verbose=False,
):
    """
    This function is for getting the responses to all the show_all functions.

    Parameters
    ----------
        column1 : str
            Name of first column in the ``node_config.csv`` file
        column1value : str
            Value in the first column of the ``node_config.csv`` file
        column2 : str
            Name of second column in the ``node_config.csv`` file
        column2value : str
            Value in the second column of the ``node_config.csv`` file
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        max_entries : int
            Maximum number of entries to get.  Default is -1 to get everything.
        offset : str
            Offset to get information that you want from the API
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``requests.response`` containing all data of interest.
    """
    # get headers
    headers = {"User-Agent": "galah-python {}".format(__version__)}

    # get data and check for
    URL, method = get_api_url(
        column1=column1,
        column1value=column1value,
        column2=column2,
        column2value=column2value,
    )

    # if user wants more verbose message, print it
    print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

    # add max entries and offset
    if max_entries is not None and offset is not None:
        URL += "?max={}&offset={}".format(max_entries, offset)

    # get the response from the URL
    response = requests.request(method, URL, headers=headers)

    # check for status codes for these APIs
    if response.status_code == 403:
        raise ValueError("Provide a/an {} API key to get this information".format(atlas))
    if response.status_code == 429:
        raise ValueError("You have reached the maximum number of daily queries for the ALA.")

    # return response
    return response


def show_all_assertions(atlas=None, headers=None, verbose=None):
    """
    This function is for getting all assertions available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """

    # set returned to False for GBIF
    returned = False

    # then check for GBIF atlas
    if atlas in ["Global", "GBIF"]:
        gbif_json = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gbif_assertions.csv"))
        gbif_json.reset_index(drop=True, inplace=True)
        return gbif_json
    elif atlas in ATLASES:
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-assertions",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )
    else:
        raise ValueError("Atlas {} not taken into account in galah for assertions.".format(atlas))

    # if the response hasn't been added to the return array, add it here
    if not returned:

        # get the response in a data frame
        df = pd.DataFrame.from_dict(response.json())

        # set default value for the 'type' column
        df["type"] = True

        # append this data frame to the return_array
    return df[["name", "description", "category", "type"]]


def show_all_atlases():
    """
    This function is for getting all assertions available in the chosen atlas.

    Parameters
    ----------
        None

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """
    # data of all the atlases galah currently supports
    data = {
        "atlas": ["Australia", "Austria", "Brazil", "France", "Global", "Spain"],
        "institution": [
            "Atlas of Living Australia",
            "Biodiversitäts-Atlas Österreich",
            "Sistemas de Informações sobre a Biodiversidade Brasileira",
            "Inventaire National du Patrimoine Naturel",
            "Global Biodiversity Information Facility",
            "GBIF Spain",
        ],
        "acronym": ["ALA", "BAO", "SiBBr", "INPN", "GBIF", "GBIF.es"],
        "url": [
            "https://www.ala.org.au",
            "https://biodiversityatlas.at",
            "https://sibbr.gov.br",
            "https://inpn.mnhn.fr",
            "https://gbif.org",
            "https://www.gbif.es",
        ],
    }

    # append this data frame to the return_array
    return pd.DataFrame.from_dict(data)


def show_all_apis():
    """
    This function is for getting all apis available.

    Parameters
    ----------
        None

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """

    # append the full atlaslist to return_array
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_config.csv")
    return pd.read_csv(atlasfile)


def show_all_collections(atlas=None, headers=None, verbose=None):
    """
    This function is for getting all collections available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """

    # first, check for GBIF; then, the rest of the Atlases
    if atlas in ["Global", "GBIF", "United Kingdom", "UK"]:
        raise ValueError("{} atlas does not have a list of collections".format(atlas))
    elif atlas in ATLASES:
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-collections",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )
    else:
        raise ValueError("Atlas {} not taken into account in galah-python for collections.".format(atlas))

    # append data frame to return_array (while checking for France)
    if atlas in ["France"]:
        return pd.DataFrame.from_dict(response.json()["_embedded"])
    else:
        return pd.DataFrame.from_dict(response.json())


def show_all_datasets(atlas=None, headers=None, verbose=None):
    """
    This function is for getting all datasets available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """

    # check for datasets
    if atlas in ["Global", "GBIF"]:
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-datasets",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )
        return pd.DataFrame.from_dict(response.json()["results"])

    elif atlas in ATLASES:
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-datasets",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )
        if atlas in ["France"]:
            return pd.DataFrame.from_dict(response.json()["_embedded"]["datasets"])
        else:
            return pd.DataFrame.from_dict(response.json())

    else:
        raise ValueError("Atlas {} not taken into account in galah-python for datasets.".format(atlas))


def show_all_fields(atlas=None, headers=None, verbose=None):
    """
    This function is for getting all assertions available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """
    # get all possible fields
    if atlas not in ["Global", "GBIF"]:

        # get data from API
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-fields",
            column2="api_name",
            column2value="records_fields",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )

        if atlas in ["Portugal"]:
            df = pd.DataFrame()
            for i, item in enumerate(response.json()):
                df = pd.concat([df, pd.DataFrame(item, index=[i])])
            return df

        # get fields values in a table
        fields_values = pd.DataFrame.from_dict(response.json())

        # remove anything with 'Contextual' or 'Environmental' from the options for Australian atlas
        if atlas in ["Australia", "Brazil", "Spain"]:

            fields_values = fields_values[~fields_values["classs"].astype(str).str.contains("Contextual|Environmental")]

        # select only the columns titled 'name', 'info', (and) 'infoUrl'
        if atlas in ["Australia", "Spain"]:
            fields_select = fields_values[["name", "info", "infoUrl"]]
            dataFrame = fields_select.rename(columns={"name": "id", "info": "description", "infoUrl": "link"})
            dataFrame.insert(loc=2, column="type", value="field")
        elif atlas in [
            "Austria",
            "Brazil",
            "Canada",
            "Estonia",
            "France",
            "Guatemala",
            "Sweden",
            "United Kingdom",
        ]:
            fields_select = fields_values[["name", "info"]]
            dataFrame = fields_select.rename(columns={"name": "id", "info": "description"})  # , inplace=True)
            dataFrame["type"] = "field"
            dataFrame["link"] = ""

    # check if atlas is GBIF
    elif atlas in ["Global", "GBIF"]:
        dataFrame = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gbif_fields.csv"))

    # else, atlas not taken into account
    else:
        raise ValueError("Atlas {} not taken into account for fields.".format(atlas))

    # second: get spatial layers
    spatial_layers = get_spatial_layers_from_fields(atlas=atlas, headers=headers, verbose=verbose)

    # third: get media fields
    if atlas in ["Australia", "Spain"]:

        # third: get media
        media_values = pd.DataFrame.from_dict(
            {
                "id": [
                    "multimedia",
                    "multimediaLicence",
                    "images",
                    "videos",
                    "sounds",
                ],
                "description": "Media filter field",
                "type": "media",
                "link": "",
            }
        )

        # fourth: get other fields
        other_field_values = pd.DataFrame(
            {
                "id": "qid",
                "description": "Reference to pre-generated query",
                "type": "other",
                "link": "",
            },
            index=[0],
        )

        # create final dataframe
        return_dataFrame = pd.concat(
            [dataFrame, spatial_layers, media_values, other_field_values],
            ignore_index=True,
        )

        # reset index
        return_dataFrame.reset_index(drop=True, inplace=True)

        # return final dataframe to user
        return return_dataFrame

    # else: only return fields dataframe
    else:

        # reset index
        dataFrame.reset_index(drop=True, inplace=True)

        # return final thing
        return dataFrame


def get_spatial_layers_from_fields(atlas=None, headers=None, verbose=None):
    """
    This function is for getting the spatial layers for the fields argument.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """

    # initialise empty dataframe
    spatial_layers = pd.DataFrame()

    # get spatial layers either for Australia or Spain
    if atlas in ["Australia", "ALA", "Spain"]:

        # get data from API
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-fields",
            column2="api_name",
            column2value="spatial_layers",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )

        # process spatial data
        spatial_values = pd.DataFrame.from_dict(response.json())

        # select only the columns titled 'name', 'info', (and) 'infoUrl'
        if atlas in ["Australia", "Spain"]:

            # build layer id from this
            spatial_values.loc[spatial_values["type"] == "Contextual", "type"] = "cl"
            spatial_values.loc[spatial_values["type"] == "Environmental", "type"] = "el"
            spatial_layers["id"] = spatial_values["id"].astype(str).copy()

            # build descriptions from these
            if atlas in ["Australia"]:
                spatial_layers["description"] = (
                    spatial_values["name"] + " " + spatial_values["desc"]
                )  # changed from displayname and description
            else:
                spatial_layers["description"] = spatial_values["displayname"] + " " + spatial_values["description"]
            spatial_layers["type"] = "layers"
            spatial_layers["link"] = ""

        # look only into these atlases
        elif atlas in ["Austria", "Brazil", "France"]:
            layers_select = spatial_values[["name", "info"]]
            spatial_layers = layers_select.rename(columns={"name": "id", "info": "description"})
            spatial_layers["type"] = "layers"
            spatial_layers["link"] = ""

        # else, need to add another atlas
        else:
            raise ValueError("Atlas {} not taken into account for fields".format(atlas))

    # return the spatial layers dataframe
    return spatial_layers


def show_all_licences(atlas=None, headers=None, verbose=None):
    """
    This function is for getting all licences available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """

    # check for atlases that don't have licences
    if atlas in ["France", "Global", "GBIF"]:
        raise ValueError("The {} atlas does not have a list of licences".format(atlas))

    # check for atlases that have an endpoint but no data
    elif atlas in ["Austria", "Brazil"]:
        raise ValueError("{} has an API endpoint for licences, but it is empty.".format(atlas))

    # check if atlas is taken into account for licences
    elif atlas not in ATLASES:
        raise ValueError("Atlas {} not taken into account for licences.".format(atlas))

    # otherwise, do default call
    else:

        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-licences",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )

    # check to see if this URL is not working
    if response.status_code == 404:
        raise ValueError("The licences URL for the {} atlas is not working.".format(atlas))

    # create a data frame from the API response
    df = pd.DataFrame.from_dict(response.json())

    # append data frame with only the column names 'id', 'name', 'acronym' and 'url'
    return df[["id", "name", "acronym", "url"]]


def show_all_lists(atlas=None, headers=None, verbose=None):
    """
    This function is for getting all lists available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """

    # first, check for APIs that do not have lists
    if atlas in ["France", "GBIF", "Global"]:
        raise ValueError("The {} atlas does not have a lists API.".format(atlas))

    # then, look for lists and set offsets
    if atlas in ATLASES:
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-lists",
            atlas=atlas,
            headers=headers,
            max_entries=-1,
            offset=0,
            verbose=verbose,
        )
    else:
        raise ValueError("Atlas {} not taken into account for lists.".format(atlas))

    # get all the lists from the API call response
    df = pd.DataFrame.from_dict(response.json()["lists"])

    # rename dataResourceUid
    if "dataResourceUid" in df:
        df = df.rename(columns={"dataResourceUid": "species_list_uid"})

    # append data frame to return_array
    return df


def show_all_profiles(atlas=None, headers=None, verbose=None):
    """
    This function is for getting all profiles available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """

    # check for only APIs that have data quality profiles
    if atlas in ["Australia", "Spain"]:

        # get data
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-profiles",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )

        # create dataframe
        df = pd.DataFrame.from_dict(response.json())

        # append data frame with only the column names 'id', 'name', 'shortName' and 'description'
        if atlas in ["Spain"]:
            print(
                "WARNING: The Spanish atlas has data quality profiles, but they are not yet linked to the biocache yet"
            )

        # return data frame
        return df[["id", "name", "shortName", "description"]]

    # else, raise value error
    else:
        raise ValueError("Only the Australian atlas has data quality profiles you can use.")


def show_all_providers(atlas=None, headers=None, verbose=None):
    """
    This function is for getting all data providers available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """
    # raise an exception specific to France, as their providers are empty
    if atlas in ["France"]:
        raise ValueError("{} has an API endpoint for providers, but it is empty.".format(atlas))

    # check for atlases with providers
    elif atlas in ATLASES:

        # get data
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-providers",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )

        # make data frame
        if atlas in ["Global", "GBIF"]:
            providers_list = pd.DataFrame.from_dict(response.json()["results"])
        else:
            providers_list = pd.DataFrame.from_dict(response.json())

    # else, do default call
    else:
        raise ValueError("Atlas {} not taken into account for show_all_lists.".format(atlas))

    # append data frame to return_array
    return providers_list


def show_all_ranks():
    """
    This function is for getting all ranks available in the chosen atlas.

    Parameters
    ----------
        None

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """
    # get configuration
    configs = readConfig()

    # extended ranks dictionary
    if configs["galahSettings"]["ranks"] == "all":
        all_ranks = {
            "id": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
                31,
                32,
                33,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
                41,
                42,
                43,
                44,
                45,
                46,
                47,
                48,
                49,
                50,
                51,
                52,
                53,
                54,
                55,
                56,
                57,
                58,
                59,
                60,
                61,
                62,
                63,
                64,
                65,
                66,
                67,
                68,
                69,
            ],
            "name": [
                "root",
                "superkingdom",
                "kingdom",
                "subkingdom",
                "superphylum",
                "phylum",
                "subphylum",
                "superclass",
                "class",
                "subclass",
                "infraclass",
                "subinfraclass",
                "superdivison zoology",
                "division zoology",
                "subdivision zoology",
                "supercohort",
                "cohort",
                "subcohort",
                "superorder",
                "order",
                "suborder",
                "infraorder",
                "parvorder",
                "superseries zoology",
                "series zoology",
                "subseries zoology",
                "supersection zoology",
                "section zoology",
                "subsection zoology",
                "superfamily",
                "family",
                "subfamily",
                "infrafamily",
                "supertribe",
                "tribe",
                "subtribe",
                "supergenus",
                "genus group",
                "genus",
                "nothogenus",
                "subgenus",
                "supersection botany",
                "section botany",
                "subsection botany",
                "superseries botany",
                "series botany",
                "subseries botany",
                "species group",
                "superspecies",
                "species subgroup",
                "species",
                "nothospecies",
                "holomorph",
                "anamorph",
                "teleomorph",
                "subspecies",
                "nothosubspecies",
                "infraspecies",
                "variety",
                "nothovariety",
                "subvariety",
                "form",
                "nothoform",
                "subform",
                "biovar",
                "serovar",
                "cultivar",
                "pathovar",
                "infraspecific",
            ],
        }
        return pd.DataFrame.from_dict(all_ranks)

    # check for reduced ranks
    elif configs["galahSettings"]["ranks"] == "gbif":
        gbif_ranks = {
            "id": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "name": [
                "kingdom",
                "phylum",
                "class",
                "order",
                "family",
                "genus",
                "species",
                "subspecies",
                "infraspecific",
            ],
        }
        return pd.DataFrame.from_dict(gbif_ranks)
    else:
        raise ValueError(
            "For ranks, you can only have two values currently:\n\nall: all possible ranks\ngbif: only the nine major ranks\n"
        )


def show_all_reasons(atlas=None, headers=None, verbose=None):
    """
    This function is for getting all reasons available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        headers : dict
            Dictionary of information to pass to the API via the headers option
        verbose : logical
            If True, print all APIs that are hit to screen.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """
    # check for atlases that don't have a reasons API
    if atlas in [
        "Brazil",
        "France",
        "Global",
        "GBIF",
    ]:
        raise ValueError("The {} atlas does not have a reasons API.".format(atlas))

    # check for ones that do
    elif atlas in ATLASES:

        # get data
        response = get_response_show_all(
            column1="called_by",
            column1value="show_all-reasons",
            atlas=atlas,
            headers=headers,
            verbose=verbose,
        )

    # else, do default call
    else:
        raise ValueError("Atlas {} not taken into account for show_all_lists.".format(atlas))

    # create a data frame from the API response
    df = pd.DataFrame.from_dict(response.json())

    # append data frame with only the column names 'id', 'name', sort values by 'id', and renumber indices
    return df[["id", "name"]].sort_values("id").reset_index(drop=True)
