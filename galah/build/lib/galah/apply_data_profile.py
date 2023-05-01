from .get_api_url import readConfig
from .show_all import show_all

def apply_data_profile(baseURL):
    """
    A 'profile' is a group of filters that are pre-applied by the ALA. Using a data profile allows a query to be filtered 
    quickly to the most relevant or quality-assured data that is fit-for-purpose. For example, the "ALA" profile is designed 
    to exclude lower quality records, whereas other profiles apply filters specific to species distribution modelling (e.g. CDSM).

    Parameters
    ----------
        baseURL : string
            TBD  

    Returns
    -------
        TBD

    Examples
    --------

        .. prompt:: python

            galah.apply_data_profile()

        .. program-output:: python -c "import galah; print(galah.atlas_counts())"

    """

    # first, get configurations and check for configurations
    configs = readConfig()

    # adding a few things to baseURL
    if configs['galahSettings']['data_profile'].lower() == "none":
        baseURL += "disableAllQualityfilters=true"
    else:
        data_profile_list = list(show_all(profiles=True)['shortName'])
        if configs['galahSettings']['data_profile'] in data_profile_list:
            baseURL += "qualityProfile={}&".format(configs['galahSettings']['data_profile'])
        else:
            raise ValueError("The data quality profile not recognised. To see valid data quality profiles, run \n\n"
                             "profiles = galah.show_all(profiles=True)\n\n"
                             "then type\n\n"
                             "profiles['shortName']\n\n"
                             "  To set a data profile, type\n" 
                             "galah.galah_config(data_profile=\"NAME FROM SHORTNAME HERE\")"
                             "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
                             "galah.galah_config(data_profile=\"None\")")

    return baseURL