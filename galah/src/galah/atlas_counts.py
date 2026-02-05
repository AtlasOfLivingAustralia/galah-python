import pandas as pd
import requests

from .add_to_payload_functions import add_to_payload_ALA
from .common_add_functions import (add_extras_to_URL, add_filters,
                                   add_spatial_shapes, add_taxa)
from .common_checks import (check_atlas, check_atlas_authenticate,
                            check_atlas_data_profile,
                            check_for_non_working_atlases,
                            check_max_queries_ALA, check_string_list)
from .common_dictionaries import COUNTS_NAMES
from .common_functions import print_if_verbose, set_bool_argument
from .galah_config import get_api_url, readConfig
from .galah_group_by import galah_group_by
from .show_all import show_all
from .version import __version__


def atlas_counts(
    taxa=None,
    scientific_name=None,
    filters=None,
    group_by=None,
    total_group_by=False,
    use_data_profile=False,
    polygon=None,
    bbox=None,
    simplify_polygon=False,
    tolerance=0.05,
    config_file=None,
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
        use_data_profile : string
            A profile name. Should be a string - the name or abbreviation of a data quality profile to apply to the query. Valid values can be seen using ``galah.show_all(profiles=True)``
        polygon : shapely Polygon
            A polygon object denoting a geographical region.  Defaults to ``None``.
        bbox : dict or shapely Polygon
            A polygon or dictionary object denoting four points, which are the corners of a geographical region.  Defaults to ``None``.
        simplify_polygon : logical
            When using the ``polygon`` argument of ``galah.atlas_counts()``, specifies whether or not to simplify the polygon and use this instead.  Defaults to ``True``.
        config_file : string
            If you want to specify your own config file, put the path and name of the file here.  This is applicable when you are running on a server and each user has different configurations.  Defaults to ``None``.

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

        .. program-output:: python -c "import galah; print(galah.atlas_counts(filters=\\\"year>2019\\\",group_by=\\\"year\\\"))"

    """

    # ---------------------------------------------------------------------------------------------
    # Declare all variables, run checks on compatibility of arguments.
    # ---------------------------------------------------------------------------------------------

    # get configs
    configs = readConfig(config_file=config_file)

    # get atlas and verbose
    atlas = configs["galahSettings"]["atlas"]
    verbose = set_bool_argument(arg=configs["galahSettings"]["verbose"], name_arg="verbose")
    timeout = int(configs["galahSettings"]["timeout"])
    authenticate = set_bool_argument(arg=configs["galahSettings"]["authenticate"], name_arg="authenticate")
    access_token = configs["galahSettings"]["access_token"]
    client_id = configs["galahSettings"]["client_id"]

    # check to see if atlas is in list of non-functioning atlases
    check_for_non_working_atlases(atlas=atlas)

    # check atlas is valid
    check_atlas(atlas=atlas, function="atlas_counts")
    check_atlas_authenticate(atlas=atlas, authenticate=authenticate)
    check_atlas_data_profile(atlas=atlas, use_data_profile=use_data_profile)

    # set default column 2 value
    column2value = "records_counts"

    # check for Brazilian atlas
    if group_by is not None and atlas in ["Brazil"]:
        column2value = "records_facets"

    # ---------------------------------------------------------------------------------------------
    # Declare all variables, run checks on compatibility of arguments.
    # ---------------------------------------------------------------------------------------------

    # first, check if the authenticate argument is true
    if authenticate:

        # create payload (for ALA)
        payload = {}

        # check for Australian atlas
        if atlas in ["Australia", "ALA"]:

            # create payload
            payload = add_to_payload_ALA(
                payload=payload,
                atlas=atlas,
                taxa=taxa,
                filters=filters,
                polygon=polygon,
                bbox=bbox,
                scientific_name=scientific_name,
                simplify_polygon=simplify_polygon,
                authenticate=authenticate,
            )

            # get the URL for counts
            countsURL, method = get_api_url(
                column1="called_by",
                column1value="atlas_counts",
                column2="api_name",
                column2value=column2value,
                config_file=config_file,
            )

            # check for group by
            if group_by is not None:

                # return grouped table
                return galah_group_by(
                    URL=countsURL,
                    method=method,
                    group_by=group_by,
                    filters=filters,
                    verbose=verbose,
                    total_group_by=total_group_by,
                    payload=payload,
                )

            # create the query id
            qid_URL, method2 = get_api_url(column1="api_name", column1value="occurrences_qid")

            # format headers with authentication
            headers = {
                "User-Agent": "galah-python {}".format(__version__),
                "Authorization": "Bearer {}".format(access_token),
                "client_id": client_id,
            }

            # print all information in the query ID call if verbose is True
            print_if_verbose(verbose=verbose, headers=headers, URL=qid_URL, method=method2, payload=payload)

            # cache the user's query and get a query ID
            qid = requests.request(method2, qid_URL, data=payload, headers=headers)

            # create the URL to grab your queryID and counts
            URL = countsURL + "?fq=%28qid%3A" + qid.text + "%29&flimit=-1&pageSize=0"

            # add last things to URL
            if atlas in ["Australia", "ALA"]:
                URL += add_extras_to_URL(
                    add_email=False,
                    use_data_profile=use_data_profile,
                    data_profile_list=list(show_all(profiles=True)["shortName"]),
                    atlas=atlas,
                    config_file=config_file
                )
            else:
                URL += add_extras_to_URL(add_email=False, atlas=atlas,config_file=config_file)

            # print all information in the counts call if verbose is True
            print_if_verbose(verbose=verbose, URL=URL, method=method)

            # get data
            response = requests.request(method, URL, headers=headers)

            # check for max queries ALA
            check_max_queries_ALA(response=response)

            # get data from response
            response_json = response.json()

            # return dataFrame with total number of records
            return pd.DataFrame({"totalRecords": [response_json[COUNTS_NAMES[atlas]]]})

    else:

        # get the baseURL and method
        URL, method = get_api_url(
            column1="called_by",
            column1value="atlas_counts",
            column2="api_name",
            column2value=column2value,
            config_file=config_file,
        )

        # check the type of filters
        filters = check_string_list(filters, "filters")

        # get headers
        headers = {"User-Agent": "galah-python/{}".format(__version__)}

        # add taxa to URL
        URL = add_taxa(taxa=taxa, atlas=atlas, URL=URL, scientific_name=scientific_name)
        
        # return None if there are no valid taxa
        if "fq" not in URL and all(x is None for x in [filters,polygon,bbox]):
            if taxa is not None:
                return None

        # check if user wants to group counts
        if group_by is not None:

            # check for GBIF first
            if atlas not in ["Global", "GBIF"]:

                # return grouped data frame
                return galah_group_by(
                    URL=URL,
                    method=method,
                    group_by=group_by,
                    filters=filters,
                    verbose=verbose,
                    total_group_by=total_group_by,
                )

            # return grouped data frame
            return galah_group_by(
                URL=URL,
                method=method,
                group_by=group_by,
                filters=filters,
                verbose=verbose,
                total_group_by=total_group_by,
            )

        # add filters and spatial shapes
        URL = add_filters(URL=URL, atlas=atlas, filters=filters)
        URL = add_spatial_shapes(
            polygon=polygon, bbox=bbox, URL=URL, simplify_polygon=simplify_polygon, tolerance=tolerance
        )

        # add last things to URL
        if atlas in ["Australia", "ALA"]:
            URL += add_extras_to_URL(
                add_email=False,
                use_data_profile=use_data_profile,
                data_profile_list=list(show_all(profiles=True)["shortName"]),
                atlas=atlas,
                config_file=config_file
            )
        else:
            URL += add_extras_to_URL(add_email=False, atlas=atlas,config_file=config_file)

        # check to see if the user wants the querying URL
        print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

        # get data
        response = requests.request(method, URL, headers=headers, timeout=timeout)

        # get data from response
        response_json = response.json()

        # check for max queries ALA
        check_max_queries_ALA(response=response)

        # return dataFrame with total number of records
        return pd.DataFrame({"totalRecords": [response_json[COUNTS_NAMES[atlas]]]})
