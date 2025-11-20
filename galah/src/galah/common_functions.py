import os
import urllib

import pandas as pd

from .common_dictionaries import atlases
from .galah_config import galah_config, readConfig
from .galah_filter import galah_filter


def check_taxa_type(taxa=None):

    # check to see if taxa is string or list
    if isinstance(taxa, (list, str)):

        # convert to list for easy looping
        if type(taxa) is str:
            taxa = [taxa]

    else:
        raise ValueError("The taxa argument only takes a string or a list, not {}.".format(type(taxa)))

    # return taxa
    return taxa


def check_atlas_in_atlases(atlas=None, func=None):

    if atlas not in atlases:
        raise ValueError("Atlas {} is not taken into account for function {}".format(atlas, func))


# get the URL for the API we want to ping for the
def get_api_url(
    column1=None,
    column1value=None,
    column2=None,
    column2value=None,
):

    # check that there is at least column 1 name and column 1 value
    if column1 is None and column1value is None:
        raise ValueError("You need to provide a column name for column1 and value for column1value")
    if column1 is None:
        raise ValueError("You need to provide a column name for column1")
    if column1value is None:
        raise ValueError("You need to provide a value for this function to search for in the column")

    # first, get specific atlas
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_config.csv")
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig()

    # check for global atlas and make sure it is named correctly
    if configs["galahSettings"]["atlas"] == "GBIF":
        galah_config(atlas="Global")
        configs = readConfig()

    # check for global atlas and make sure it is named correctly
    if configs["galahSettings"]["atlas"] == "UK":
        print("here")
        galah_config(atlas="United Kingdom")
        configs = readConfig()

    # get specific atlas
    specific_atlas = atlaslist[atlaslist["atlas"] == configs["galahSettings"]["atlas"]]

    # get rows with specific value
    rows = specific_atlas[specific_atlas[column1].astype(str).str.contains(column1value, case=True, na=False)]

    # check to see if there are two columns to filter by
    if column2 is None and column2value is None:

        # check if there is more than one entry
        if len(rows.loc[rows[column1].astype(str).str.contains(column1value, case=True, na=False)].index) > 1:
            raise ValueError("There are more than one possible APIs - need to specify column2 and column2value")

        # else, return the singular URL
        else:
            index = rows[rows[column1].astype(str).str.contains(column1value, case=True, na=False)].index[0]
            baseURL = rows[rows[column1].astype(str).str.contains(column1value, case=True, na=False)]["api_url"][index]
            method = rows[rows[column1].astype(str).str.contains(column1value, case=True, na=False)]["method"][index]

    # if there are two columns to filter by, first check for the name and value
    elif column2 is not None and column2value is not None:

        # check if there is more than one entry
        if len(rows[rows[column2].astype(str).str.contains(column2value, case=True, na=False)].index) > 1:
            raise ValueError(
                "There are more than one possible APIs with column2 and column2value - choose this API another way"
            )

        # else, return the singular URL
        else:
            index = rows[rows[column2].astype(str).str.contains(column2value, case=True, na=False)].index[0]
            baseURL = rows.loc[rows[column1].astype(str).str.contains(column1value, case=True, na=False)]["api_url"][
                index
            ]
            method = rows.loc[rows[column1].astype(str).str.contains(column1value, case=True, na=False)]["method"][
                index
            ]

    # else, the user has provided something incorrect
    else:
        raise ValueError("A value needs to be provided for both column2 and column2 value")

    # return the final URL
    return baseURL, method


def print_if_verbose(verbose=False, headers=None, URL=None, method=None, payload=None):

    if verbose:
        print()
        print("headers: {}".format(headers))
        print()
        print("URL for querying: {}".format(URL))
        print("Method: {}".format(method))
        print()

    if payload is not None:
        print("Payload: \n\n{}\n".format(payload))
        print()


def add_predicates(predicates=None, filters=None):
    """for adding filters specifically to atlas_occurrences"""

    if isinstance(filters, str):
        filters = [filters]

    if any("!=" in f for f in filters):
        raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")

    for f in filters:

        predicates.append(galah_filter(f, occurrencesGBIF=True))

    return predicates


def kvp_to_columns(kvp_values):
    """
    All data is in the KVP for lists.  Make sure the KVP data is in a pandas dataframe by itself.
    """
    return_dict = {}
    for entry in kvp_values:
        return_dict[entry["key"]] = entry["value"]
    return return_dict


def add_extras_to_URL(add_email=True, use_data_profile=False, data_profile_list=None):

    # get your configs
    configs = readConfig()

    # initialise variable
    end_url = "&"

    # first, check for email_notify
    end_url += "emailNotify={}&".format(configs["galahSettings"]["email_notify"].lower())

    # next, check for email
    if add_email:
        if configs["galahSettings"]["email_notify"] not in ["None", ""]:
            end_url += "email={}&".format(urllib.parse.quote(configs["galahSettings"]["email"]))

    # then, check for data profile
    if use_data_profile:
        if not (configs["galahSettings"]["data_profile"] in ["None", ""]):
            if configs["galahSettings"]["data_profile"] in data_profile_list:
                end_url += "qualityProfile={}&".format(configs["galahSettings"]["data_profile"])
            else:
                raise ValueError(
                    "The data quality profile not recognised. To see valid data quality profiles, run \n\n"
                    "profiles = galah.show_all(profiles=True)\n\n"
                    "then type\n\n"
                    "profiles['shortName']\n\n"
                    "  To set a data profile, type\n"
                    "galah.galah_config(data_profile='NAME FROM SHORTNAME HERE')"
                    "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
                    "galah.galah_config(data_profile='None')"
                )
    else:
        end_url += "disableAllQualityFilters=true&"

    # finally, add reason
    end_url += "reasonTypeId={}".format(configs["galahSettings"]["reason"])

    # return end_url
    return end_url
