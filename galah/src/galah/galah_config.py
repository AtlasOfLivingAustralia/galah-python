import configparser
import os

import pandas as pd

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
    usernameGBIF=None,
    passwordGBIF=None,
    config_file=None,
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
        usernameGBIF: string
            Your username for GBIF atlas.  Default is ''.
        passwordGBIF: string
            Your password for GBIF atlas.  Default is ''.

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
    if config_file is None:
        inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    else:
        if not os.path.isfile(config_file):
            os.system("touch {}".format(config_file))
        inifile = config_file
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
            "usernameGBIF": "None",
            "passwordGBIF": "None",
        }

    # check for global atlas and make sure it is named correctly
    atlas = check_atlas_name(atlas=atlas)

    # set the ranks by default for the Global atlas
    if atlas == "Global":
        ranks = "Global"

    # check to see if there are any arguments to update - if not, return dataframe.  If so, update file.
    if (
        email is None
        and email_notify is None
        and atlas is None
        and data_profile is None
        and ranks is None
        and reason is None
    ):

        # create dictionary for pandas dataframe
        settings_dict = {"Configuration": [], "Value": []}
        for entry in configParser["galahSettings"]:
            settings_dict["Configuration"].append(entry)
            settings_dict["Value"].append(str(configParser["galahSettings"][entry]))

        # return options
        return pd.DataFrame.from_dict(settings_dict)

    else:

        list_of_terms = [
            "email",
            "email_notify",
            "atlas",
            "data_profile",
            "ranks",
            "reason",
            "usernameGBIF",
            "passwordGBIF",
        ]
        list_of_vars = [
            email,
            email_notify,
            atlas,
            data_profile,
            ranks,
            reason,
            usernameGBIF,
            passwordGBIF,
        ]

        # update the field to change
        for name, item in zip(list_of_terms, list_of_vars):
            if item is not None:
                configParser["galahSettings"][name] = str(item)

        # write to file
        with open(inifile, "w") as fileObject:
            configParser.write(fileObject)
        fileObject.close()


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
