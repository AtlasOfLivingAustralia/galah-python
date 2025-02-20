'''
Function for configuring
'''

import configparser,os
import pandas as pd

# how I did this:
# https://www.codeproject.com/Articles/5319621/Configuration-Files-in-Python
# run this first at installation
'''
 ALA_API_key = None,
                 clientID = None,
                 clientSecretID = None
'''
def galah_config(email=None,
                 email_notify=None,
                 atlas=None,
                 data_profile = None,
                 ranks = None,
                 reason = None,
                 usernameGBIF = None,
                 passwordGBIF = None,
                 config_file=None
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
            A string letting galah know what taxonomic ranks to show.  Use "all" to see all 69 possible ranks, and "gbif" to see the 9 most common ranks.
        reason: integer
            A number (integer) providing the reason you are downloading data.  Default is set to 4 (scientific research).  For a list of all possible reasons run ``galah.show_all_reasons()``
        usernameGBIF: string
            Your username for GBIF atlas.  Default is "".
        passwordGBIF: string
            Your password for GBIF atlas.  Default is "".
            
    Returns
    -------
        - No arguments: A ``pandas.DataFrame`` of all current configuration options.
        - >=1 arguments: None

    Examples
    --------

    .. prompt:: python

        import galah
        galah.galah_config(email="yourname@example.com")
    """

    # open the config parser
    configParser = configparser.ConfigParser()

    # read the config file
    if config_file is None:
        inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    else:
        inifile = config_file
    configParser.read(inifile)

    if len(configParser.sections()) == 0:
        configParser["galahSettings"] = {
            "email": "None",
            "email_notify": "False",
            "atlas": "Australia",
            "data_profile": "None",
            "ranks": "all",
            "reason": "4",
            "usernameGBIF": "None",
            "passwordGBIF": "None"
        }

    # check to see if there are any arguments to update
    if email is None and email_notify is None and atlas is None and data_profile is None and ranks is None and reason is None:
        
        # create dictionary for pandas dataframe 
        settings_dict = {"Configuration": [], "Value": []}
        for entry in configParser["galahSettings"]:
            settings_dict["Configuration"].append(entry)
            settings_dict["Value"].append(str(configParser["galahSettings"][entry]))
        
        # return options
        return pd.DataFrame.from_dict(settings_dict)
    
    else:
        
        list_of_terms = ["email","email_notify","atlas","data_profile","ranks","reason","usernameGBIF","passwordGBIF"]
        list_of_vars = [email,email_notify,atlas,data_profile,ranks,reason,usernameGBIF,passwordGBIF]

        # update the field to change
        for name,item in zip(list_of_terms,list_of_vars):
            if item is not None:
                configParser["galahSettings"][name] = str(item)

        # write to file
        with open(inifile,"w") as fileObject:
            configParser.write(fileObject)
        fileObject.close()