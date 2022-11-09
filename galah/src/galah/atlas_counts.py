import os,sys,requests,urllib.parse,time,zipfile,io,glob
import pandas as pd
from .galah_filter import galah_filter
from .galah_group_by import galah_group_by
from .search_taxa import search_taxa
from .get_api_url import get_api_url
from .get_api_url import readConfig
from .show_all import show_all

'''
counts
------
get the count of the number of records of specified specie(s).  filters can be applied, such as year of occurrence.

arguments
---------
taxa: a string or a list of taxa to get the number of counts for
         (example: "Vulpes vulpes" or ["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
separate: boolean argument used if the user wants separate counts when they are querying multiple taxa
verbose: boolean argument used to get URLs used for the query
filters: list of filters as text

returns
-------
dataFrame: a pandas dataframe containing the taxa name and total number of records for that taxa.  Can be separated
           into multiple taxa with the separate argument

TODO
----
1. Test more filters available on the ALA
'''
def atlas_counts(taxa=None, separate=False, verbose=False, filters=None, group_by=None, expand=True):

    # get the URL needed for the query
    baseURL = "{}?".format(get_api_url(column1='called_by',column1value='atlas_counts'))

    # first, get configurations and check for configurations
    configs = readConfig()

    # email for querying
    if configs['galahSettings']['email'] is None:
        raise ValueError("You need to provide a valid email address for occurrences to be able to download data")

    # adding a few things to baseURL
    if configs['galahSettings']['data_profile'].lower() == "none":
        baseURL += "disableAllQualityfilters=true"
    else:
        data_profile_list = list(show_all(profiles=True)['shortName'])
        if configs['galahSettings']['data_profile'] in data_profile_list:
            baseURL += "&qualityProfile={}".format(configs['galahSettings']['data_profile'])
        else:
            raise ValueError("The data quality profile you've chosen is not one of the ones used - run \n\n"
                             "profiles = galah.show_all(profiles=True)\n\n"
                             "and then type\n\n"
                             "profiles['shortName']\n\n"
                             "to get the names of the data quality profiles you can use.  If you don't want to use a data"
                             " quality profile, set it to None by typing the following:\n\n"
                             "galah.galah_config(data_profile=\"None\")")
    baseURL += "&email={}&dwcHeaders=True".format(configs['galahSettings']['email'])
    if configs['galahSettings']['email_notify'].lower() == "false":
        baseURL += "&emailNotify=false"
    elif configs['galahSettings']['email_notify'].lower() == "true":
        baseURL += "&emailNotify=True" # check if this is correct
    else:
        raise ValueError("email_notify option should be set to either True or False - please set that with "
                         "galah_config(email_notify=\"False\") or galah_config(email_notify=\"True\")")

    # if there is no taxa, assume you will get the total number of records in the ALA
    if taxa is None:

        # check if group_by exist
        if group_by is None:

            # check if filters are specified
            if filters is not None:

                # check the type of variable filters is
                if type(filters) is list or type(filters) is str:

                    # change to list for easier looping
                    if type(filters) is str:
                        filters = [filters]

                    # start URL
                    URL = baseURL + "&"

                    # add filters
                    for f in filters:
                        URL += galah_filter(f) + "&"

                    # add final part of URL
                    URL += "&pageSize=0"

                # else, make sure that the filters is in the following format
                else:
                    raise TypeError(
                        "filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")

            # else, add the final bit of the URL
            else:
                URL = baseURL + "pageSize=0"

            # check to see if the user wantw the querying URL
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))

            # get the response and data
            response = requests.get(URL)
            json = response.json()

            # return dataFrame with total number of records
            return pd.DataFrame({'totalRecords': [json['totalRecords']]})

        # else, the user wants a grouped dataFrame
        else:

           # return a grouped dataFrame
            return galah_group_by(baseURL, group_by=group_by, filters=filters, expand=expand)

    # if there is a single taxa, get
    elif type(taxa) is str or type(taxa) is list:

        # change taxa into list for easier looping
        if type(taxa) is str:
            taxa = [taxa]

        # set these variables to 0 and empty initially
        totalRecords = 0
        tempTotalRecords = []

        # get the number of records associated with each taxa
        for name in taxa:

            # get the taxonConceptID for taxa
            taxonConceptID = search_taxa(name)['taxonConceptID'][0]

            # add this ID to the URL
            URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"

            # return a grouped dataFrame
            if group_by is not None:

                # does verbose work here?
                return galah_group_by(URL, group_by, filters, expand)

            else:

                # check to see if filters exist
                if filters is not None:

                    # check the type of variable filters is
                    if type(filters) is list or type(filters) is str:

                        # change to list for easier looping
                        if type(filters) is str:
                            filters = [filters]

                        # start URL
                        URL = baseURL + "&"

                        # add filters
                        for f in filters:
                            URL += galah_filter(f) + "&"

                        # add final part of URL
                        URL += "&pageSize=0"

                    # else, make sure that the filters is in the following format
                    else:
                        raise TypeError(
                            "filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")

                # add the last bit of the URL
                else:
                    URL += "pageSize=0"

            # check to see if the user wants the URL for querying
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))

            # get results form the URL
            response = requests.get(URL)
            json = response.json()

            # if the user wants them separated, add counts to a temporary array to make a dataframe with
            if separate:
                tempTotalRecords.append(int(json['totalRecords']))

            # if the user doesn't want them separate, then add them to the existing counts
            else:
                totalRecords += int(json['totalRecords'])

        # make a dataframe with the total records for each taxa separate
        if separate:
            dataFrame = pd.DataFrame({'taxa': taxa, 'totalRecords': tempTotalRecords})

        # make a dataframe with the total number of records
        else:
            dataFrame = pd.DataFrame({'totalRecords': [totalRecords]})

        # return the dataFrame with the specified counts
        return dataFrame

    # if the taxa variable isn't a string or a list, raise an exception
    else:
        raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: atlas.counts(\"Vulpes vulpes\")"
                        "\n         atlas.counts[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")
