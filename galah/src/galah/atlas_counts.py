import requests,urllib.parse,warnings
import pandas as pd
from .galah_filter import galah_filter
from .galah_group_by import galah_group_by
from .search_taxa import search_taxa
from .get_api_url import get_api_url
from .get_api_url import readConfig
from .apply_data_profile import apply_data_profile

ATLAS_KEYWORDS = {
    "Australia": "taxonConceptID",
    "Austria": "guid",
    "Brazil": "guid", 
    "Canada": "usageKey",
    "Estonia": "guid",
    "France": "usageKey",
    "Guatemala": "guid",
    "Portugal": "usageKey",
    "Spain": "taxonConceptID",
    "Sweden": "guid",
    "United Kingdom": "guid",
}

atlases = ["Australia","Austria","Brazil","Canada","Estonia","France","Guatemala","Portugal","Sweden","Spain","United Kingdom"]

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

    .. program-output:: python -c "import galah; print(galah.atlas_counts())"

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

    # set initial variables
    group_by_dataframe = pd.DataFrame()

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

                    # start URL - might need to add + "&" later
                    URL = baseURL + "fq=%28"

                    # loop over filters
                    for f in filters:
                        URL += galah_filter(f, ifgroupBy=expand) + "%20AND%20"

                    # add final part of URL
                    URL = URL[:-len("%20AND%20")] + "%29"

                # else, make sure that the filters is in the following format
                else:
                    raise TypeError(
                        "filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")

            # else, add the final bit of the URL
            else:
                if configs["galahSettings"]["atlas"] == "Australia":
                    URL = baseURL + "flimit=10000&pageSize=0"
                else:
                    URL = baseURL

            # check to see if the user wants the querying URL
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
            URL = baseURL + "fq="
            return galah_group_by(URL, group_by=group_by, filters=filters, expand=expand, verbose=verbose)

    # if taxa exist, do this
    elif type(taxa) is str or type(taxa) is list:

        # change taxa into list for easier looping
        if type(taxa) is str:
            taxa = [taxa]

        # get the number of records associated with each taxa
        # check for separate here first?
        for i,name in enumerate(taxa):

            # create temporary dataframe for taxon id
            tempdf = search_taxa(name)

            # check if dataframe is empty - if so, return None; else, continue
            if tempdf.empty:
                print("No taxon matches were found for {} in the selected atlas ({})".format(name, configs[
                    'galahSettings']['atlas']))
                if len(taxa) == 1:
                    return None
                continue

        # get the taxonConceptID for taxa - first check for extant atlas
        if configs['galahSettings']['atlas'] in atlases:
            taxonConceptID = list(search_taxa(taxa)[ATLAS_KEYWORDS[configs['galahSettings']['atlas']]])
        else:
            raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

        # add this ID to the URL
        URL = baseURL + "fq=%28lsid%3A" + "%20OR%20lsid%3A".join(
            urllib.parse.quote(str(tid)) for tid in taxonConceptID) + "%29"

        # return a grouped dataFrame
        if group_by is not None:

            if filters is not None:
                URL += "%20AND%20"
                return galah_group_by(URL, group_by=group_by, filters=filters, expand=expand, verbose=verbose)
            else:
                return galah_group_by(baseURL, group_by=group_by, filters=filters, expand=expand, verbose=verbose)

        else:

            # check to see if filters exist
            if filters is not None:

                # check the type of variable filters is
                if type(filters) is list or type(filters) is str:

                    # change to list for easier looping
                    if type(filters) is str:
                        filters = [filters]

                    URL += "%20AND%20%28"

                    # loop over filters
                    for f in filters:
                        URL += galah_filter(f, ifgroupBy=expand) + "%20AND%20"

                    # add final part of URL
                    URL = URL[:-len("%20AND%20")] + "%29"
                    if separate:
                        URL += "&facets=species"
                    URL += "&flimit=10000&pageSize=0"

                # else, make sure that the filters is in the following format
                else:
                    raise TypeError(
                        "filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")

            # add the last bit of the URL
            else:

                # check if it's separate one last time
                if separate:
                    URL += "&facets=species"
                URL += "&flimit=10000&pageSize=0"

        # check to see if the user wants the URL for querying
        if verbose:
            print("URL for querying:\n\n{}\n".format(URL))

        # get results form the URL
        response = requests.get(URL)
        json = response.json()

        # if the user wants them separated, add counts to a temporary array to make a dataframe with
        if separate:
            separate_dict={entry:[] for entry in ['label','count']}
            for entry in json['facetResults'][0]['fieldResult']:
                for name in ['label','count']:
                    separate_dict[name].append(entry[name])
            dataFrame = pd.DataFrame(separate_dict)
            if dataFrame.shape[0] < len(taxa):
                #warnings.warn("One of the taxa is not found in your designated atlas")
                print("One of the taxa is not found in your designated atlas")
            return dataFrame

        if not group_by_dataframe.empty:
            return group_by_dataframe

        ### TODO: Figure this out
        # raise warning if one of the taxa isn't in the atlas
        #if num_taxa < len_taxa:
        #    warnings.warn("One of the taxa is not found in your designated atlas")

        # make a dataframe with the total number of records
        else:
            return pd.DataFrame({'totalRecords': [int(json['totalRecords'])]})

    # if the taxa variable isn't a string or a list, raise an exception
    else:
        raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: atlas.counts(\"Vulpes vulpes\")"
                        "\n         atlas.counts[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")
