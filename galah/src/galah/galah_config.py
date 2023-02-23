'''
Function for configuring
'''

import configparser,os

# how I did this:
# https://www.codeproject.com/Articles/5319621/Configuration-Files-in-Python
# run this first at installation
def galah_config(email=None,
                 email_notify=None,
                 atlas=None,
                 data_profile = None):
    """
    The galah package supports large data downloads, and also interfaces with the ALA which requires that users of some 
    services provide a registered email address and reason for downloading data. The ``galah.galah_config()`` function provides a way 
    to manage these issues as simply as possible.

    Parameters
    ----------
        email : string
            An email address that has been registered with the chosen atlas. For the ALA, you can register at [this address](https://auth.ala.org.au/userdetails/registration/createAccount).  
        email_notify : string
            Used to receive an email for each query to ``galah.atlas_occurrences()``. Defaults to ``None``, but can be useful in some instances, for example for tracking DOIs assigned to specific downloads for later citation.
        atlas : string
            Living Atlas to point to, ``Australia`` by default. Can be an organisation name, acronym, or region (see ``show_all(atlases=True)`` for admissible values)
        data_profile : string
            A profile name. Should be a string - the name or abbreviation of a data quality profile to apply to the query. Valid values can be seen using ``galah.show_all(profiles=True)``

    Returns
    -------
        A ``list`` of all current configuration options.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.galah_config(email="yourname@example.com")
    """

    # check to see if there are any arguments to update
    if email is None and email_notify is None and atlas is None and data_profile is None:
        raise ValueError("Please specify a value you would like to change, i.e. galah_config(email=\"youremail@example.come\")")

    # open the config parser
    configParser = configparser.ConfigParser()

    # read the config file
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configParser.read(inifile)

    # update the field to change
    if email is not None:
        configParser["galahSettings"]["email"] = email
    if email_notify is not None:
        configParser["galahSettings"]["email_notify"] = email_notify
    if atlas is not None:
        configParser["galahSettings"]["atlas"] = atlas
    if data_profile is not None:
        configParser["galahSettings"]["data_profile"] = data_profile
    # add things for data profiles here

    # write to file
    with open(inifile,"w") as fileObject:
        configParser.write(fileObject)
