import os,sys,requests,urllib.parse,time,zipfile,io,configparser,glob
import pandas as pd
from .galah_filter import galah_filter
from .galah_group_by import galah_group_by
from .search_taxa import search_taxa

# read configuration file
def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

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

    # set up configs
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig()
    specific_atlas = atlaslist[atlaslist['atlas'] == configs['galahSettings']['atlas']]

    # test to check if ALA is working
    ALA_check = specific_atlas[specific_atlas['called_by'] == 'atlas_counts']
    index = ALA_check[ALA_check['called_by'] == "atlas_counts"].index[0]
    baseURL = "{}?".format(specific_atlas[specific_atlas['called_by'] == 'atlas_counts']['api_url'][index])

    # get the baseURL for getting total number of records
    ### TODO: change this
    #baseURL = "https://biocache-ws.ala.org.au/ws/occurrence/search?"

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
