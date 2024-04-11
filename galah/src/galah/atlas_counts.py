import requests
import pandas as pd
from .galah_group_by import galah_group_by
from .get_api_url import get_api_url,readConfig
from .apply_data_profile import apply_data_profile
from .galah_geolocate import galah_geolocate
from .show_all import show_all
from .common_functions import add_filters,add_to_payload_ALA,generate_list_taxonConceptIDs
from .common_dictionaries import COUNTS_NAMES
from .version import __version__

import json

def atlas_counts(taxa=None,
                 scientific_name=None,
                 filters=None,
                 group_by=None,
                 total_group_by=False,
                 expand=True,
                 use_data_profile=False,
                 verbose=False,
                 polygon=None,
                 bbox=None,
                 simplify_polygon=False,
                 ):
    """
    Prior to downloading data, it is often valuable to have some estimate of how many records are available, both for deciding
    if the query is feasible, and for estimating how long it will take to download. Alternatively, for some kinds of reporting,
    the count of observations may be all that is required, for example for understanding how observations are growing or shrinking
    in particular locations, or for particular taxa.
    
    To this end, ``galah.atlas_counts()`` takes arguments in the same format as ``galah.atlas_occurrences()``, and provides either 
    a total count of records matching the criteria, or a pandas dataframe of counts matching the criteria supplied to the `group_by` 
    argument.  It can also return the total number of groups by using the `total_group_by` argument.

    Parameters
    ----------
        taxa : string
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.
        filters : pandas.DataFrame
            filters, in the form ``field`` ``logical`` ``value`` (e.g. ``"year=2021"``)
        group_by : string
            zero or more individual column names (i.e. fields) to include. See ``galah.show_all()`` and ``galah.search_all()`` to see valid fields.
        total_group_by : logical
            If ``True``, galah gives total number of groups in data. Defaults to ``False``.
        expand : logical
            When using the ``group_by`` argument of ``galah.atlas_counts()``, controls whether counts for each row value are combined or calculated separately. Defaults to ``True``.
        verbose : logical
            If ``True``, galah gives more information like progress bars. Defaults to ``False``.
        use_data_profile : string
            A profile name. Should be a string - the name or abbreviation of a data quality profile to apply to the query. Valid values can be seen using ``galah.show_all(profiles=True)``
        polygon : shapely Polygon
            A polygon object denoting a geographical region.  Defaults to ``None``.
        bbox : dict or shapely Polygon
            A polygon or dictionary object denoting four points, which are the corners of a geographical region.  Defaults to ``None``.
        simplify_polygon : logical
            When using the ``polygon`` argument of ``galah.atlas_counts()``, specifies whether or not to draw a bounding box around the polygon and use this instead.  Defaults to ``False``.
                    
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

            galah.atlas_counts(filters="year>2019",group_by="year",expand=False)

        .. program-output:: python -c "import galah; print(galah.atlas_counts(filters=\\\"year>2019\\\",group_by=\\\"year\\\",expand=False))"
        
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas']

    # raise error if argument is wrong type and/or the atlas doesn't have a quality profile but the user has specified one
    if use_data_profile and atlas not in ["Australia","ALA"]:
        raise ValueError("True and False are the only values accepted for data_profile, and the only atlas using a data \n"
                        "quality profile is Australia.  Your atlas and data profile is \n"
                        "set in your config file.  To set your default filter, find out what profiles are on offer:\n"
                        "profiles = galah.show_all(profiles=True)\n\n"
                        "and then type\n\n"
                        "profiles['shortName']\n\n"
                        "to get the names of the data quality profiles you can use.  To set a data profile, type\n" 
                        "galah.galah_config(data_profile=\"NAME FROM SHORTNAME HERE\")"
                        "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
                        "galah.galah_config(data_profile=\"None\")")
    
    # check for Brazilian atlas
    elif group_by is not None and atlas in ["Brazil"]:
        baseURL,method = get_api_url(column1='called_by',column1value='atlas_counts',column2="api_name",
                                           column2value="records_facets")
    # use this if they don't want a data quality profile or none exists
    else:
        baseURL,method = get_api_url(column1='called_by',column1value='atlas_counts',column2="api_name",
                                           column2value="records_counts")

    # add a question mark at the end of the URL to separate between endpoint and queries
    URL = baseURL + "?"

    # get headers
    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # create payload (for ALA)
    payload = {}

    # check for Australian atlas
    if atlas in ["Australia","ALA"]:

        # check for data profile first
        if use_data_profile:

            # add data quality profile directly to URL
            data_profile_list = list(show_all(profiles=True)['shortName'])
            baseURL = apply_data_profile(baseURL=baseURL,data_profile_list=data_profile_list)

        # else, disable all quality filters
        else:

            baseURL += "?disableAllQualityfilters=true&"

        # create payload
        payload = add_to_payload_ALA(payload=payload,atlas=atlas,taxa=taxa,filters=filters,
                                     polygon=polygon,bbox=bbox,scientific_name=scientific_name,
                                     simplify_polygon=simplify_polygon)
        
        # check for group by
        if group_by is not None:

            # get grouped table
            return galah_group_by(URL=baseURL,method=method,group_by=group_by, filters=filters, expand=expand, verbose=verbose, total_group_by=total_group_by,payload=payload)

        # create the query id
        qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")
        
        # add options for data quality profiles
        if use_data_profile:
            data_profile_list = list(show_all(profiles=True)['shortName'])
            qid_URL = apply_data_profile(baseURL=qid_URL,data_profile_list=data_profile_list)
        else:
            qid_URL += "?disableAllQualityfilters=true&"

        # cache the user's query and get a query ID
        qid = requests.request(method2,qid_URL,data=payload,headers=headers)
        
        # create the URL to grab your queryID and counts
        URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&flimit=-1&pageSize=0"

        if verbose:
            print()
            print("headers: {}".format(headers))
            print()
            print("payload for queryID: {}".format(payload))
            print("queryID URL: {}".format(qid_URL))
            print("method: {}".format(method2))
            print()
            print("qid for query: {}".format(qid.text))
            print("URL for result:{}".format(URL))
            print("method: {}".format(method))
            print()

        # get data
        response = requests.request(method,URL,headers=headers)

        # check for daily maximum
        if response.status_code == 429:
            raise ValueError("You have reached the maximum number of daily queries for the ALA.")
        
        # get data from response
        response_json = response.json()
        
        # return dataFrame with total number of records
        return pd.DataFrame({'totalRecords': [response_json[COUNTS_NAMES[atlas]]]})

    else:

        # if there is no taxa, assume you will get the total number of records in the ALA
        if taxa is not None:

            URL += generate_list_taxonConceptIDs(taxa=taxa,atlas=atlas,verbose=verbose)

        # check if user wants to gropu counts
        if group_by is not None:

            # check for GBIF first
            if configs["galahSettings"]['atlas'] not in ["Global","GBIF"]:

                # add a separator if the user has taxa specified
                if taxa is not None and filters is not None:
                    URL += "%20AND%20"
                
                # return grouped data frame
                return galah_group_by(URL=URL, method=method, group_by=group_by, filters=filters, expand=expand, verbose=verbose, total_group_by=total_group_by)
            
            # else, if not GBIF, just run group_by
            else:

                # return grouped data frame
                return galah_group_by(URL=URL, method=method, group_by=group_by, filters=filters, expand=expand, verbose=verbose, total_group_by=total_group_by)

        # check if filters are specified
        if filters is not None:

            # check the type of variable filters is
            if type(filters) is list or type(filters) is str:
                
                # add a separator if the user has taxa specified
                if taxa is not None:
                    URL += "%20AND%20"
                    URL = add_filters(URL=URL,atlas=atlas,filters=filters)

                # then, add filters
                else:
                    URL = add_filters(URL=URL,atlas=atlas,filters=filters)
                    
            # else, make sure that the filters is in the following format
            else:
                raise TypeError(
                    "filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")

        # testing for galah_geolocate - implemented in next version
        if polygon is not None or bbox is not None:
            URL += "&" + galah_geolocate(polygon=polygon,bbox=bbox,simplify_polygon=simplify_polygon)
        
        # use this to get only the data we need
        URL += "&pageSize=0"

        # check to see if the user wants the querying URL
        if verbose:
            print()
            print("headers: {}".format(headers))
            print("URL for querying: {}".format(URL))
            print("Method: {}".format(method))
            print()

        # get data
        response = requests.request(method,URL,headers=headers)

        # check for daily maximum
        if response.status_code == 429:
            raise ValueError("You have reached the maximum number of daily queries for the ALA.")
        
        # get data from response
        response_json = response.json()
        
        # return dataFrame with total number of records
        return pd.DataFrame({'totalRecords': [response_json[COUNTS_NAMES[atlas]]]})