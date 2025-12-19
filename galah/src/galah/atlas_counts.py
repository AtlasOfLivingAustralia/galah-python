import pandas as pd
import requests

from .common_add_functions import add_extras_to_URL, add_filters, add_spatial_shapes, add_taxa
from .common_checks import check_atlas, check_string_list
from .common_dictionaries import COUNTS_NAMES
from .common_functions import print_if_verbose
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
    verbose=False,
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
        verbose : logical
            If ``True``, galah gives more information like progress bars. Defaults to ``False``.
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

    # get configs
    configs = readConfig(config_file=config_file)

    # get atlas
    atlas = configs["galahSettings"]["atlas"]

    # check atlas is valid
    check_atlas(atlas=atlas, function="atlas_counts")

    # raise error if argument is wrong type and/or the atlas doesn't have a quality profile but the user has specified one
    if use_data_profile and atlas not in ["Australia", "ALA"]:
        raise ValueError(
            "True and False are the only values accepted for data_profile, and the only atlas using a data \n"
            "quality profile is Australia.  Your atlas and data profile is \n"
            "set in your config file.  To set your default filter, find out what profiles are on offer:\n"
            "profiles = galah.show_all(profiles=True)\n\n"
            "and then type\n\n"
            "profiles['shortName']\n\n"
            "to get the names of the data quality profiles you can use.  To set a data profile, type\n"
            'galah.galah_config(data_profile="NAME FROM SHORTNAME HERE")'
            "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
            'galah.galah_config(data_profile="None")'
        )

    # set default column 2 value
    column2value = "records_counts"

    # check for Brazilian atlas
    if group_by is not None and atlas in ["Brazil"]:
        column2value = "records_facets"

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
    if URL is None:
        return None

    # check if user wants to group counts
    if group_by is not None:

        # check for GBIF first
        if configs["galahSettings"]["atlas"] not in ["Global", "GBIF"]:

            # # add a separator if the user has taxa specified
            # if taxa is not None and filters is not None:
            #     URL += "%20AND%20"

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
        )
    else:
        URL += add_extras_to_URL(add_email=False, atlas=atlas)

    # check to see if the user wants the querying URL
    print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

    # get data
    response = requests.request(method, URL, headers=headers)

    # get data from response
    response_json = response.json()

    # return dataFrame with total number of records
    return pd.DataFrame({"totalRecords": [response_json[COUNTS_NAMES[atlas]]]})
