import sys,requests,urllib.parse,time,zipfile,io,configparser,glob
import pandas as pd
from .galah_filter import galah_filter
from .galah_group_by import galah_group_by
from .search_taxa import search_taxa

'''
counts
------
get the count of the number of records of specified specie(s).  Filters can be applied, such as year of occurrence.

arguments
---------
species: a string or a list of species to get the number of counts for
         (example: "Vulpes vulpes" or ["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
separate: boolean argument used if the user wants separate counts when they are querying multiple species
verbose: boolean argument used to get URLs used for the query
filter: list of filters as text

returns
-------
dataFrame: a pandas dataframe containing the species name and total number of records for that species.  Can be separated
           into multiple species with the separate argument

TODO
----
1. Test more filters available on the ALA
'''

def atlas_counts(species=None, separate=False, verbose=False, filters=None, groups=None, expand=False):
    # get the baseURL for getting total number of records
    baseURL = "https://biocache-ws.ala.org.au/ws/occurrence/search?"

    # if there is no species, assume you will get the total number of records in the ALA
    if species is None:

        # check if groups exist
        if groups is None:

            # check if filters are specified
            if filters is not None:

                # check the type of variable filters is
                if type(filters) is list or type(filters) is str:

                    # change to list for easier looping
                    if type(filters) is str:
                        filters = [filters]

                    # add filters and final part of URL
                    URL += "&" + galah_filter(filters) + "&pageSize=0"

                # else, make sure that the filters is in the following format
                else:
                    raise TypeError(
                        "Filters should only be a list, and are in the following format:\n\nfilter=[\'year:2020\']")

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
            return galah_group_by(baseURL, groups, filters, expand)

    # if there is a single species, get
    elif type(species) is str or type(species) is list:

        # change species into list for easier looping
        if type(species) is str:
            species = [species]

        # set these variables to 0 and empty initially
        totalRecords = 0
        tempTotalRecords = []

        # get the number of records associated with each species
        for name in species:

            # get the taxonConceptID for species
            taxonConceptID = search_taxa(name)['taxonConceptID'][0]

            # add this ID to the URL
            URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"

            # check to see if filters exist
            if filters is not None:

                # check the type of variable filters is
                if type(filters) is list or type(filters) is str:

                    # change to list for easier looping
                    if type(filters) is str:
                        filters = [filters]

                    # add filters and final part of URL
                    URL += "&" + galah_filter(filters) + "&pageSize=0"

                # else, make sure that the filters is in the following format
                else:
                    raise TypeError(
                        "Filters should only be a list, and are in the following format:\n\nfilter=[\'year:2020\']")

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

        # make a dataframe with the total records for each species separate
        if separate:
            dataFrame = pd.DataFrame({'Species': species, 'totalRecords': tempTotalRecords})

        # make a dataframe with the total number of records
        else:
            dataFrame = pd.DataFrame({'totalRecords': [totalRecords]})

        # return the dataFrame with the specified counts
        return dataFrame

    # if the species variable isn't a string or a list, raise an exception
    else:
        raise TypeError("The species argument can only be a string or a list."
                        "\nExample: atlas.counts(\"Vulpes vulpes\")"
                        "\n         atlas.counts[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")
