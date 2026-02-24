import configparser
import json
import os
import time

import pandas as pd
import requests

from .common_functions import is_bool_argument
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

    # open the config parser
    configParser = configparser.ConfigParser()

    # read the config file
    inifile = get_config_filename(config_file=config_file)
    configParser.read(inifile)

    # if configuration file is empty, fill with default values

    if len(configParser.sections()) == 0:
        configParser["galahSettings"] = {
            "email": "None",
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
        }

    # check for global atlas and make sure it is named correctly
    atlas = check_atlas_name(atlas=atlas)

    # set the ranks by default for the Global atlas
    ranks = set_ranks(atlas=atlas, ranks=ranks)

    # checking that these arguments are boolean if user has specified them
    is_bool_argument(email_notify, "email_notify")
    is_bool_argument(verbose, "verbose")
    is_bool_argument(authenticate, "authenticate")
    is_bool_argument(auth_clear, "auth_clear")

    # check to see if someone wants to clear bad authentication information
    configParser = check_for_clearing_auth_info(configParser=configParser, auth_clear=auth_clear)

    # if the user wants authentication on, make sure that all authentication information needed is stored
    if authenticate:

        all_auth_settings = [
            configParser["galahSettings"]["client_id"],
            configParser["galahSettings"]["client_secret"],
            configParser["galahSettings"]["refresh_token"],
            configParser["galahSettings"]["access_token"],
            configParser["galahSettings"]["scopes"],
            configParser["galahSettings"]["expires_at"],
        ]

        if all(x not in [None, ""] for x in all_auth_settings):

            # check if token is expired
            expiry = is_access_token_expired(expires_at=float(configParser["galahSettings"]["expires_at"]))

            # if token is expired, regenerate the token
            if expiry:

                # get token url
                auth_info = get_auth_config()

                # regenerate the token
                refresh_token, expires_in = regenerate_token(
                    refresh_token=configParser["galahSettings"]["refresh_token"],
                    token_url=auth_info["token_url"],
                    client_id=configParser["galahSettings"]["client_id"],
                    client_secret=configParser["galahSettings"]["client_secret"],
                    scope=configParser["galahSettings"]["scopes"],
                )

                # set the new token in the config file
                configParser["galahSettings"]["refresh_token"] = refresh_token
                configParser["galahSettings"]["expires_at"] = str(time.time() + float(expires_in))

        else:

            # check if person has provided an authentication json
            if auth_filename is not None:

                # read file into json
                with open(auth_filename) as f:
                    auth_json = json.load(f)

                # set client_id and expires_at now
                configParser["galahSettings"]["client_id"] = auth_json["profile"]["client_id"]
                # configParser["galahSettings"]["client_secret"] = auth_json["profile"]["client_secret"]
                configParser["galahSettings"]["expires_at"] = str(auth_json["expires_at"])

            # if not, open web for them
            elif all(x in [None, ""] for x in all_auth_settings):

                # get the tokens from the web
                try:
                    client_id, auth_json = get_tokens_from_web()
                    configParser["galahSettings"]["client_id"] = client_id
                    configParser["galahSettings"]["expires_at"] = str(time.time() + float(auth_json["expires_in"]))

                except KeyboardInterrupt:
                    print("\nCancelled.")

            else:
                raise ValueError(
                    "Your stored authentication information is incomplete.  Set the 'auth_clear' argument to True to reset all of the config changes."
                )

            configParser["galahSettings"]["scopes"] = auth_json["scope"]
            configParser["galahSettings"]["refresh_token"] = auth_json["refresh_token"]
            configParser["galahSettings"]["access_token"] = auth_json["access_token"]

    # check to see if there are any arguments to update - if not, return dataframe.  If so, update file.
    if all(x is None for x in [authenticate, auth_filename, email, email_notify, atlas, data_profile, reason, verbose]):

        # create dictionary for pandas dataframe
        settings_dict = {"Configuration": [], "Value": []}
        for entry in configParser["galahSettings"]:
            settings_dict["Configuration"].append(entry)
            settings_dict["Value"].append(str(configParser["galahSettings"][entry]))

        # return options
        return pd.DataFrame.from_dict(settings_dict)

    else:

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
            "client_id": configParser["galahSettings"]["client_id"],
            "client_secret": "",  # need to implement this?
            "access_token": configParser["galahSettings"]["access_token"],
            "refresh_token": configParser["galahSettings"]["refresh_token"],
            "scopes": configParser["galahSettings"]["scopes"],
            "expires_at": configParser["galahSettings"]["expires_at"],
        }

        # update the field to change
        for key in terms_vars_dict.keys():
            if terms_vars_dict[key] is not None:
                configParser["galahSettings"][key] = str(terms_vars_dict[key])

        # write to file
        with open(inifile, "w") as fileObject:
            configParser.write(fileObject)
        fileObject.close()


###################################################################################################
# Checks for galah_config
###################################################################################################


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
            raise ValueError("Please create your own config file on your system first before editing it.")
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


def readConfig(config_file=None):
    """
    The galah package supports large data downloads, and also interfaces with the ALA which requires that users of some
    services provide a registered email address and reason for downloading data. The ``galah_config()`` function provides a way
    to manage these issues as simply as possible.

    Parameters
    ----------
        config_file : str
            Name of your configuration file.  Default is `config.ini`.

    Returns
    -------
        Dictionary containing configuration file information.
    """
    configFile = configparser.ConfigParser()
    if config_file is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    configFile.read(config_file)
    return configFile


# readConfig
# get the URL for the API we want to ping for the
def get_api_url(column1=None, column1value=None, column2=None, column2value=None, config_file=None):

    # first, get specific atlas
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_config.csv")
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig(config_file=config_file)

    # get specific atlas
    specific_atlas = atlaslist[atlaslist["atlas"] == configs["galahSettings"]["atlas"]]

    # get rows with specific value
    rows = specific_atlas[specific_atlas[column1].astype(str).str.contains(column1value, case=True, na=False)]

    # check to see if there are two columns to filter by
    if column2 is None and column2value is None:

        # else, return the singular URL
        index = rows[rows[column1].astype(str).str.contains(column1value, case=True, na=False)].index[0]
        baseURL = rows[rows[column1].astype(str).str.contains(column1value, case=True, na=False)]["api_url"][index]
        method = rows[rows[column1].astype(str).str.contains(column1value, case=True, na=False)]["method"][index]

    # if there are two columns to filter by, first check for the name and value
    else:

        # else, return the singular URL
        index = rows[rows[column2].astype(str).str.contains(column2value, case=True, na=False)].index[0]
        baseURL = rows.loc[rows[column1].astype(str).str.contains(column1value, case=True, na=False)]["api_url"][index]
        method = rows.loc[rows[column1].astype(str).str.contains(column1value, case=True, na=False)]["method"][index]

    # return the final URL
    return baseURL, method


def is_access_token_expired(expires_at=None):
    """
    Check if your JWT token is expired
    """
    return time.time() > expires_at


def regenerate_token(token_url=None, refresh_token=None, scope=None, client_id=None, client_secret=None):

    # set up payload
    payload = {"refresh_token": refresh_token, "grant_type": "refresh_token", "scope": scope, "client_id": client_id}
    if client_secret is not None and not "":
        payload["client_secret"] = client_secret

    # get the new token
    r = requests.post(token_url, data=payload, timeout=600)

    # return the access token and expires_in if it works; otherwise, throw error
    if r.ok:
        data = r.json()
        return data["access_token"], data["expires_in"]
    else:
        print("Unable to refresh access token. ", r.status_code, r.content)


def check_for_clearing_auth_info(configParser=None, auth_clear=False):
    if auth_clear:
        for x in ["client_id", "refresh_token", "access_token", "scopes", "expires_at"]:
            configParser["galahSettings"][x] = ""
    return configParser
