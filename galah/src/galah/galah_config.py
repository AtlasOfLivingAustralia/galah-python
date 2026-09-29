import configparser
import json
import os
import time
from functools import cache

import pandas as pd
import requests

from .common_checks import check_atlas_authenticate, check_atlas_data_profile
from .common_dictionaries import (
    USER_AGENT,
    USER_AGENT_QGIS,
    atlases,
    atlases_not_working,
)
from .common_functions import is_bool_argument, set_bool_argument
from .get_tokens_from_web import get_auth_config, get_tokens_from_web

# how I did this:
# https://www.codeproject.com/Articles/5319621/Configuration-Files-in-Python
# run this first at installation


def galah_config(
    email=None,
    email_notify=None,
    atlas=None,
    data_profile=None,
    ranks=None,
    reason=None,
    verbose=None,
    timeout=600,
    usernameGBIF=None,
    passwordGBIF=None,
    config_file=None,
    authenticate=None,
    auth_filename=None,
    auth_clear=None,
    qgis=None,
):
    """
    The galah package supports large data downloads, and also interfaces with the ALA which requires that users of some
    services provide a registered email address and reason for downloading data. The ``galah_config()`` function provides a way
    to manage these issues as simply as possible.

    Parameters
    ----------
        email : string
            An email address that has been registered with the chosen atlas. For the ALA, you can register `here <https://auth.ala.org.au/userdetails/registration/createAccount>`_.
        email_notify : string
            Used to receive an email for each query to ``galah.atlas_occurrences()``. Defaults to ``None``, but can be useful in some instances, for example for tracking DOIs assigned to specific downloads for later citation.
        atlas : string
            Living Atlas to point to, ``Australia`` by default. Can be an organisation name, acronym, or region (see ``show_all(atlases=True)`` for admissible values)
        data_profile : string
            A profile name. Should be a string - the name or abbreviation of a data quality profile to apply to the query. Valid values can be seen using ``galah.show_all(profiles=True)``
        ranks: string
            A string letting galah know what taxonomic ranks to show.  Use 'all' to see all 69 possible ranks, and 'gbif' to see the 9 most common ranks.
        reason: integer
            A number (integer) providing the reason you are downloading data.  Default is set to 4 (scientific research).  For a list of all possible reasons run ``galah.show_all_reasons()``
        verbose : logical
            If ``True``, galah gives you the URLs used to query all the data.  Default to ``False``.
        usernameGBIF: string
            Your username for GBIF atlas.  Default is ''.
        passwordGBIF: string
            Your password for GBIF atlas.  Default is ''.
        authenticate: logical
            An argument to

    Returns
    -------
        - No arguments: A ``pandas.DataFrame`` of all current configuration options.
        - >=1 arguments: None

    Examples
    --------

    .. prompt:: python

        import galah
        galah.galah_config(email='yourname@example.com')
    """

    # read the config file
    inifile = get_config_filename(config_file=config_file)
    configs = readConfig(inifile)
    print(f"atlas in galah_config: {atlas}")

    # first, check if config file is empty; if so, create a dataframe with the default values
    if len(configs.sections()) == 0:
        configs["galahSettings"] = {
            "email": "",
            "email_notify": "False",
            "atlas": "Australia",
            "data_profile": "None",
            "ranks": "all",
            "reason": "4",
            "verbose": "False",
            "timeout": "600",
            "usernamegbif": "",
            "passwordgbif": "",
            "authenticate": "False",
            "client_id": "",
            "client_secret": "",
            "access_token": "",
            "refresh_token": "",
            "scopes": "",
            "expires_at": "",
            "qgis": "False",
        }

    # check for global atlas and make sure it is named correctly
    atlas = check_atlas_name(atlas=atlas)
    print(f"atlas in galah_config again: {atlas}")

    # set the ranks by default for the Global atlas
    ranks = set_ranks(atlas=atlas, ranks=ranks)

    # checking that these arguments are boolean if user has specified them
    is_bool_argument(email_notify, "email_notify")
    is_bool_argument(verbose, "verbose")
    is_bool_argument(authenticate, "authenticate")
    is_bool_argument(auth_clear, "auth_clear")
    is_bool_argument(qgis, "qgis")

    # check to see if someone wants to clear bad authentication information
    configs = check_for_clearing_auth_info(configs=configs, auth_clear=auth_clear)

    # check to see if there are any arguments to update - if not, return dataframe.  If so, update file.
    if (
        all(
            x is None
            for x in [
                authenticate,
                auth_filename,
                email,
                email_notify,
                atlas,
                data_profile,
                usernameGBIF,
                passwordGBIF,
                reason,
                verbose,
                qgis,
            ]
        )
        and timeout == 600
    ):

        df = pd.DataFrame(
            {
                "Configuration": list(configs["galahSettings"].keys()),
                "Value": list(configs["galahSettings"].values()),
            }
        )

        return df

    # if the user wants authentication on, make sure that all authentication information needed is stored
    if authenticate:

        configs = get_auth_information(configs=configs, auth_filename=auth_filename)

    # check these to ensure they are set to False if user doesn't specify True
    qgis = check_for_none_return_false(var_name=qgis)
    email_notify = check_for_none_return_false(var_name=email_notify)
    verbose = check_for_none_return_false(var_name=verbose)
    authenticate = check_for_none_return_false(var_name=authenticate)

    # set a dict with all values needing to be set for straightforward looping
    terms_vars_dict = {
        "email": email,
        "email_notify": email_notify,
        "atlas": atlas,
        "data_profile": data_profile,
        "ranks": ranks,
        "reason": reason,
        "verbose": verbose,
        "timeout": timeout,
        "usernameGBIF": usernameGBIF,
        "passwordGBIF": passwordGBIF,
        "authenticate": authenticate,
        "qgis": qgis,
    }

    # write the configuration file to disk
    write_config_file(configs=configs, terms_dict=terms_vars_dict, config_file=inifile)


###################################################################################################
# read and write for config
###################################################################################################


# TODO: find a way to cache this
# @cache
def readConfig(config_file=None):

    # create a config parser
    configParser = configparser.ConfigParser()

    # read default name of config file if none is provided
    if config_file is None:
        config_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config.ini"
        )

    # read th config file and return it
    configParser.read(config_file)
    return configParser


def write_config_file(configs=None, terms_dict=None, config_file=None):

    for key in terms_dict.keys():
        if terms_dict[key] is not None:
            configs["galahSettings"][key] = str(terms_dict[key])

    # write to file
    with open(config_file, "w") as fileObject:
        configs.write(fileObject)
    fileObject.close()


# @cached(cache=cache_storage)
def get_config_values(function=None, config_file=None, use_data_profile=False):

    # get configs
    configs = readConfig(config_file=config_file)

    # get atlas
    atlas = configs["galahSettings"]["atlas"]
    email = configs["galahSettings"]["email"]
    email_notify = set_bool_argument(
        arg=configs["galahSettings"]["email_notify"], name_arg="email_notify"
    )
    timeout = int(configs["galahSettings"]["timeout"])
    verbose = set_bool_argument(
        arg=configs["galahSettings"]["verbose"], name_arg="verbose"
    )
    authenticate = set_bool_argument(
        arg=configs["galahSettings"]["authenticate"], name_arg="authenticate"
    )
    access_token = configs["galahSettings"]["access_token"]
    data_profile = configs["galahSettings"]["data_profile"]
    client_id = configs["galahSettings"]["client_id"]
    qgis = set_bool_argument(arg=configs["galahSettings"]["qgis"], name_arg="qgis")
    usernameGBIF = configs["galahSettings"]["usernameGBIF"]
    passwordGBIF = configs["galahSettings"]["passwordGBIF"]
    ranks = configs["galahSettings"]["ranks"]
    reason = configs["galahSettings"]["reason"]

    # set user agent
    user_agent = USER_AGENT
    if qgis:
        user_agent = USER_AGENT_QGIS

    # do checks on all variables to see if there are incompatibilities
    check_for_non_working_atlases(atlas=atlas)
    check_atlas(atlas=atlas, function=function)
    if function in ["atlas_occurrences", "atlas_media", "atlas_species"]:
        check_email_empty(email=email)
    check_atlas_authenticate(atlas=atlas, authenticate=authenticate)
    check_atlas_data_profile(atlas=atlas, use_data_profile=use_data_profile)

    # return all variables
    return (
        atlas,
        timeout,
        verbose,
        authenticate,
        access_token,
        client_id,
        user_agent,
        email,
        email_notify,
        data_profile,
        usernameGBIF,
        passwordGBIF,
        ranks,
        qgis,
        reason,
    )


###################################################################################################
# read and write for config
###################################################################################################


def check_atlas(atlas=None, function=None):
    """Check to see if the atlas the user provided is correct"""
    if atlas not in atlases:
        raise ValueError(
            "Atlas {} not taken into account for the {} function".format(
                atlas, function
            )
        )


def check_email_empty(email=None):

    if email in [
        None,
        "",
        "email@example.com",
    ]:
        raise ValueError("Please provide an email for querying.")


def check_for_non_working_atlases(atlas=None):
    if atlas in atlases_not_working:
        raise ValueError("The {} atlas is currently not working.".format(atlas))


def check_for_none_return_false(var_name):
    if var_name is None:
        return False
    return var_name


def set_ranks(atlas=None, ranks=None):
    if ranks is None:
        if atlas == "Global":
            return "Global"
        else:
            return "all"
    return ranks


def get_config_filename(config_file=None):
    if config_file is None:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    else:
        if not os.path.isfile(config_file):
            raise ValueError(
                "Please create your own config file on your system first before editing it."
            )
        return config_file


def check_atlas_name(atlas=None):

    # set the global name
    if atlas == "GBIF":
        return "Global"

    # same with UK
    if atlas == "UK":
        return "United Kingdom"

    # return atlas by default
    return atlas


@cache
def get_atlaslist():
    atlasfile = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "node_config.csv"
    )
    atlaslist = pd.read_csv(atlasfile)
    return atlaslist


def get_api_url(
    column1=None, column1value=None, column2=None, column2value=None, atlas=None
):

    # first, get specific atlas
    atlaslist = get_atlaslist()

    # get specific atlas
    specific_atlas = atlaslist[atlaslist["atlas"] == atlas]

    # get rows with specific value
    rows = specific_atlas[specific_atlas[column1] == column1value]

    # check to see if there are two columns to filter by
    if column2 is None and column2value is None:

        # else, return the singular URL
        index = list(rows[rows[column1] == column1value].index)[0]
        baseURL = rows[rows[column1] == column1value]["api_url"][
            index
        ]  # .astype(str).str.contains(column1value, case=True, na=False)]["api_url"][index]
        method = rows[rows[column1] == column1value]["method"][index]

    # if there are two columns to filter by, first check for the name and value
    else:

        print(list(rows[rows[column2] == column2value].index))
        # else, return the singular URL
        index = list(rows[rows[column2] == column2value].index)[
            0
        ]  # .astype(str).str.contains(column2value, case=True, na=False)].index[0]
        baseURL = rows.loc[rows[column2] == column2value]["api_url"][index]
        method = rows.loc[rows[column2] == column2value]["method"][index]

    # return the final URL
    return baseURL, method


def get_auth_information(configs=None, auth_filename=None):

    # get indices of auth settings
    all_auth_settings = [
        configs["galahSettings"]["client_id"],
        configs["galahSettings"]["client_secret"],
        configs["galahSettings"]["refresh_token"],
        configs["galahSettings"]["access_token"],
        configs["galahSettings"]["scopes"],
        configs["galahSettings"]["expires_at"],
    ]
    # check if all auth settings are prefilled - if so, refresh token
    if all(x not in [None, ""] for x in all_auth_settings):

        # check if token is expired
        expiry = is_access_token_expired(
            expires_at=float(configs["galahSettings"]["expires_at"])
        )

        # if token is expired, regenerate the token
        if expiry:

            # get token url
            auth_info = get_auth_config()

            # regenerate the token
            refresh_token, expires_in = regenerate_token(
                refresh_token=configs["galahSettings"]["refresh_token"],
                token_url=auth_info["token_url"],
                client_id=configs["galahSettings"]["client_id"],
                client_secret=configs["galahSettings"]["client_secret"],
                scope=configs["galahSettings"]["scopes"],
            )

            # set the new token in the config file
            configs["galahSettings"]["refresh_token"] = refresh_token
            configs["galahSettings"]["expires_at"] = str(
                time.time() + float(expires_in)
            )

    # else, authentication file, no settings are prefilled and navigate to website, something has gone on and the authentication information needs to be cleared
    else:

        # check if person has provided an authentication json
        if auth_filename is not None:

            # read file into json
            with open(auth_filename) as f:
                auth_json = json.load(f)

            # set client_id and expires_at now
            configs["galahSettings"]["client_id"] = auth_json["profile"]["client_id"]
            configs["galahSettings"]["expires_at"] = str(auth_json["expires_at"])

        # if not, open web for them
        elif all(x in [None, ""] for x in all_auth_settings):

            # get the tokens from the web
            try:
                client_id, auth_json = get_tokens_from_web()
                configs["galahSettings"]["client_id"] = client_id
                configs["galahSettings"]["expires_at"] = str(
                    time.time() + float(auth_json["expires_in"])
                )

            except KeyboardInterrupt:
                print("\nCancelled.")

        else:
            raise ValueError(
                "Your stored authentication information is incomplete.  Set the 'auth_clear' argument to True to reset all of the config changes."
            )

        # assign scope, refresh token and access token
        configs["galahSettings"]["scope"] = auth_json["scope"]
        configs["galahSettings"]["refresh_token"] = auth_json["refresh_token"]
        configs["galahSettings"]["access_token"] = auth_json["access_token"]

    # return configs as a data frame
    return configs


def is_access_token_expired(expires_at=None):

    # return True or False depending on whether or not the current time is more than the time the
    # token expires at
    return time.time() > expires_at


def regenerate_token(
    token_url=None, refresh_token=None, scope=None, client_id=None, client_secret=None
):

    # set up payload
    payload = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "scope": scope,
        "client_id": client_id,
    }
    if client_secret not in [None, ""]:
        payload["client_secret"] = client_secret

    # get the new token
    r = requests.post(token_url, data=payload, timeout=600)

    # return the access token and expires_in if it works; otherwise, throw error
    if r.ok:
        data = r.json()
        return data["access_token"], data["expires_in"]
    else:
        print("Unable to refresh access token. ", r.status_code, r.content)


def check_for_clearing_auth_info(configs=None, auth_clear=False):

    # clear all authentication information
    if auth_clear:
        for x in ["client_id", "refresh_token", "access_token", "scopes", "expires_at"]:
            configs["galahSettings"][x] = ""

    # return the empty configuration
    return configs
