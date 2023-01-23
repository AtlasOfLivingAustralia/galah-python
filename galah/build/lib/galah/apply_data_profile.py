from .get_api_url import get_api_url
from .get_api_url import readConfig
from .show_all import show_all

def apply_data_profile(baseURL):

    # first, get configurations and check for configurations
    configs = readConfig()

    # adding a few things to baseURL
    if configs['galahSettings']['data_profile'].lower() == "none":
        baseURL += "disableAllQualityfilters=true"
    else:
        data_profile_list = list(show_all(profiles=True)['shortName'])
        print(data_profile_list)
        if configs['galahSettings']['data_profile'] in data_profile_list:
            baseURL += "&qualityProfile={}".format(configs['galahSettings']['data_profile'])
        else:
            raise ValueError("The data quality profile you've chosen is not one of the ones used - run \n\n"
                             "profiles = galah.show_all(profiles=True)\n\n"
                             "and then type\n\n"
                             "profiles['shortName']\n\n"
                             "to get the names of the data quality profiles you can use.  To set a data profile, type\n" 
                             "galah.galah_config(data_profile=\"NAME FROM SHORTNAME HERE\")"
                             "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
                             "galah.galah_config(data_profile=\"None\")")

    return baseURL