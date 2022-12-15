import os,sys,requests,urllib.parse,time,zipfile,io,glob
import pandas as pd
from .galah_filter import galah_filter
from .galah_group_by import galah_group_by
from .search_taxa import search_taxa
from .get_api_url import get_api_url
from .get_api_url import readConfig
from .show_all import show_all
from .apply_data_profile import apply_data_profile

def atlas_counts(taxa=None,
                 filters=None,
                 group_by=None,
                 expand=True,
                 separate=False,
                 verbose=False,
                 use_data_profile=False,
                 ):
    """
    Used for getting the number of occurrence records before you're ready
    to download the actual occurrences.

    To know how many total records are in your chosen atlas, type

    .. prompt:: python

        import galah
        galah.atlas_counts()

    which returns

    .. program-output:: python3 -c "import galah; print(galah.atlas_counts())"

    example of filters that can be used: "year=2020","basisOfRecord=HUMAN_OBSERVATION"
    example of group_by groups that can be used: "year","basisOfRecord"
    """

    # get configs
    configs = readConfig()

    # get the URL needed for the query
    if use_data_profile and configs['galahSettings']['atlas'] == "Australia":
        baseURL = apply_data_profile("{}?".format(get_api_url(column1='called_by',column1value='atlas_counts',column2="api_name",
                                                              column2value="records_counts"))) + "&"
    elif not use_data_profile:
        baseURL = "{}?".format(get_api_url(column1='called_by', column1value='atlas_counts',column2="api_name",
                                           column2value="records_counts"))
    else:
        raise ValueError("True and False are the only values accepted for data_profile, and the only atlas using a data \n"
                         "quality profile is Australia.  Your atlas and data profile is \n"
                         "set in your config file.  To set your default filter, find out what profiles are on offer:\n"
                         "profiles = galah.show_all(profiles=True)\n\n"
                         "and then type\n\n"
                         "profiles['shortName']\n\n"
                         "to get the names of the data quality profiles you can use.  To set a data profile, type\n" 
                         "galah.galah_config(data_profile=\"NAME FROM SHORTNAME HERE\")"
                         "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
                         "galah.galah_config(data_profile=\"None\")"
                         )

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
                    URL = baseURL #+ "&"

                    # add filters
                    for f in filters:
                        URL += galah_filter(f) + "&"

                    # add final part of URL
                    URL += "pageSize=0"

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
            return galah_group_by(baseURL, group_by=group_by, filters=filters, expand=expand, verbose=verbose)

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

            #print(search_taxa(name))

            # get the taxonConceptID for taxa
            if configs['galahSettings']['atlas'] in ["Australia"]:
                taxonConceptID = search_taxa(name)['taxonConceptID'][0]
            elif configs['galahSettings']['atlas'] in ["Austria","Brazil","Estonia","Guatemala","Sweden","United Kingdom"]:
                taxonConceptID = search_taxa(name)['guid'][0]
            elif configs['galahSettings']['atlas'] in ["Canada","France","Portugal"]:
                taxonConceptID = search_taxa(name)['usageKey'][0]
            else:
                raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

            #print(taxonConceptID)
            #print(baseURL)
            #print(taxonConceptID)
            #print(type(taxonConceptID))

            # add this ID to the URL
            URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(str(taxonConceptID)) + "%29&" # try making it a string

            # return a grouped dataFrame
            if group_by is not None:

                # does verbose work here?
                return galah_group_by(URL, group_by=group_by, filters=filters, expand=expand, verbose=verbose)

            else:

                # check to see if filters exist
                if filters is not None:

                    # check the type of variable filters is
                    if type(filters) is list or type(filters) is str:

                        # change to list for easier looping
                        if type(filters) is str:
                            filters = [filters]

                        # add filters
                        for f in filters:
                            URL += galah_filter(f) + "&"

                        # add final part of URL
                        URL += "pageSize=0"

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
