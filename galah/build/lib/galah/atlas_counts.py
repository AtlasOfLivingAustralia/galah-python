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
                 verbose=False,
                 use_data_profile=False,
                 ):
    """
    Prior to downloading data it is often valuable to have some estimate of how many records are available, both for deciding 
    if the query is feasible, and for estimating how long it will take to download. Alternatively, for some kinds of reporting, 
    the count of observations may be all that is required, for example for understanding how observations are growing or shrinking 
    in particular locations, or for particular taxa. 
    
    To this end, ``galah.atlas_counts()`` takes arguments in the same format as 
    ``galah.atlas_occurrences()``, and provides either a total count of records matching the criteria, or a data.frame of counts matching 
    the criteria supplied to the `group_by` argument.

    Parameters
    ----------
        taxa : string
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.  
        filters : pandas.DataFrame
            filters, in the form ``field`` ``logical`` ``value`` (e.g. ``"year=2021"``)
        group_by : string
            zero or more individual column names (i.e. fields) to include. See ``galah.show_all()`` and ``galah.search_all()`` to see valid fields.
        expand : logical
            When using the ``group_by`` argument of ``galah.atlas_counts()``, controls whether counts for each row value are combined or calculated separately. Defaults to ``True``.
        verbose : logical
            If ``True``, galah gives more information like progress bars. Defaults to ``False``.
        use_data_profile : string
            A profile name. Should be a string - the name or abbreviation of a data quality profile to apply to the query. Valid values can be seen using ``galah.show_all(profiles=True)``

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------
        Return total records in your chosen atlas

        .. prompt:: python

            galah.atlas_counts()

        .. program-output:: python -c "import galah; print(galah.atlas_counts())"

        Return records from 2020 onwards, grouped by year    

        .. prompt:: python

            galah.atlas_counts(filters="year>2019",group_by="year")

        .. program-output:: python -c "import galah; print(galah.atlas_counts(filters=\\\"year>2019\\\",group_by=\\\"year\\\",expand=False))"

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
                return galah_group_by(URL, group_by=group_by, filters=filters, expand=expand, verbose=verbose)

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
                    URL = URL[:-len("%20AND%20")] + "%29&flimit=10000&pageSize=0"

                # else, make sure that the filters is in the following format
                else:
                    raise TypeError(
                        "filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")

            # add the last bit of the URL
            else:

                # check if it's separate one last time
                URL += "&flimit=10000&pageSize=0"

        # check to see if the user wants the URL for querying
        if verbose:
            print("URL for querying:\n\n{}\n".format(URL))

        # get results form the URL
        response = requests.get(URL)
        json = response.json()

        return pd.DataFrame({'totalRecords': [int(json['totalRecords'])]})

    # if the taxa variable isn't a string or a list, raise an exception
    else:
        raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: atlas.counts(\"Vulpes vulpes\")"
                        "\n         atlas.counts[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")
