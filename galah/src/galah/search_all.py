from pandas.api.types import is_numeric_dtype

from .common_checks import check_atlas
from .galah_config import readConfig
from .show_all import (show_all_apis, show_all_assertions, show_all_atlases,
                       show_all_collections, show_all_datasets,
                       show_all_fields, show_all_licences, show_all_lists,
                       show_all_profiles, show_all_providers, show_all_ranks,
                       show_all_reasons)
from .version import __version__


def search_all(
    assertions=None,
    atlases=None,
    apis=None,
    collection=None,
    datasets=None,
    fields=None,
    licences=None,
    lists=None,
    profiles=None,
    providers=None,
    ranks=None,
    reasons=None,
    column_name=None,
    verbose=False,
    config_file=None,
):
    """
    The living atlases store a huge amount of information, above and beyond the occurrence records that are their main output.
    In galah, one way that users can investigate this information is by searching for a specific option or category for the
    type of information they are interested in.  ``search_all()`` is a helper function that can do searches within multiple
    types of information.

    Parameters
    ----------
        assertions : string
            Search for results of data quality checks run by each atlas
        atlases : string
            Search for what atlases are available
        apis : string
            Search for what APIs & functions are available for each atlas
        collection : string
            Search for the specific collections within those institutions
        datasets : string
            Search for the data groupings within those collections
        fields : string
            Search for fields that are stored in an atlas
        licences : string
            Search for copyright licences applied to media
        lists : string
            Search for what species lists are available
        profiles : string
            Search for what data profiles are available
        providers : string
            Search for which institutions have provided data
        ranks : string
            Search for valid taxonomic ranks (e.g. Kingdom, Class, Order, etc.)
        reasons : string
            Search for what values are acceptable as 'download reasons' for a specified atlas
        column_name : string
            Determines what column in the table this function will search for the string specified as the argument

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.search_all(apis='Australia')

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.search_all(apis=\'Australia\'))"
    """
    # was \\\'

    # configs
    configs = readConfig(config_file=config_file)

    # get atlas
    atlas = configs["galahSettings"]["atlas"]

    # check atlas is valid
    check_atlas(atlas=atlas, function="search_all")

    headers = {"User-Agent": "galah-python/{}".format(__version__)}
    # check for column_name variable not being a string

    if column_name is not None and not isinstance(column_name, str):
        raise ValueError("Only strings are a valid query for the column_name variable")

    options = {
        # name:  [var, show_all function, check_column_name ,column_name]
        "assertions": [assertions, show_all_assertions, check_column_name_assertions],
        "atlases": [atlases, show_all_atlases, check_column_name_apis_atlases],
        "apis": [apis, show_all_apis, check_column_name_apis_atlases],
        "collection": [collection, show_all_collections, check_column_name_collection],
        "datasets": [datasets, show_all_datasets, check_column_name_datasets],
        "fields": [fields, show_all_fields, check_column_name_fields],
        "licences": [licences, show_all_licences, check_column_name_licences],
        "lists": [lists, show_all_lists, check_column_name_lists],
        "profiles": [profiles, show_all_profiles, check_column_name_profiles],
        "providers": [providers, show_all_providers, check_column_name_providers],
        "ranks": [ranks, show_all_ranks, check_column_name_ranks],
        "reason": [reasons, show_all_reasons, check_column_name_reasons],
    }

    # loop over all options
    for o in options:

        # check to see if first argument is not None
        if options[o][0] is not None:
            if not isinstance(options[o][0], str):
                raise ValueError(
                    "You can only pass one string to your search parameter = run show_all(assertions=True) to get strings to pass"
                )

            if o in ["atlases", "apis", "ranks"]:
                dataFrame = options[o][1]()

                # first, check column name, and then check sorting name
                column_name = options[o][2](column_name=column_name)

            else:
                # get initial dataframe
                dataFrame = options[o][1](atlas=atlas, headers=headers, verbose=verbose)

                # first, check column name, and then check sorting name
                column_name = options[o][2](atlas=atlas, column_name=column_name)

            if is_numeric_dtype(dataFrame[column_name].dtypes):
                dataFrame = dataFrame.map(str)
            return_dataFrame = dataFrame.loc[
                dataFrame[column_name].astype(str).str.contains(options[o][0], case=False, na=False)
            ]
            return return_dataFrame.sort_values(column_name, key=lambda x: x.str.len()).reset_index(drop=True)


"""
Checking all column name functions
"""


def check_column_name_assertions(atlas=None, column_name=None):
    # check if column_name is None; if it is, set it to default
    if column_name is None and atlas in ["Global", "GBIF"]:
        return "Description"
    if column_name is None:
        return "description"
    return column_name


def check_column_name_apis_atlases(column_name=None):
    # check if column_name is None; if it is, set it to default
    if column_name is None:
        return "atlas"
    return column_name


def check_column_name_collection(atlas=None, column_name=None):
    # check to see if user wants default column name
    if column_name is None:
        # if atlas in ["France"]:
        #     return "producers"
        return "name"
    return column_name


def check_column_name_datasets(atlas=None, column_name=None):
    if column_name is None and atlas in [
        "Australia",
        "Austria",
        "Brazil",
        "France",
        "Guatemala",
        "Kew",
        "Portugal",
        "Spain",
        "Sweden",
        "United Kingdom",
        "UK",
    ]:
        return "name"
    elif column_name is None:
        return "description"
    return column_name


def check_column_name_fields(atlas=None, column_name=None):
    if column_name is None and atlas in ["Global", "GBIF"]:
        return "qualifiedName"
    # elif column_name is None and atlas in ["Portugal"]:
    #     return "name"
    elif column_name is None:
        return "description"
    return column_name


def check_column_name_licences(atlas=None, column_name=None):
    # check if column_name is None; if it is, set it to default
    if column_name is None:
        return "name"
    return column_name


def check_column_name_lists(atlas=None, column_name=None):
    # check if column_name is None; if it is, set it to default
    if column_name is None:
        return "listName"
    return column_name


def check_column_name_profiles(atlas=None, column_name=None):
    # check if column_name is None; if it is, set it to default
    if column_name is None:
        return "description"
    return column_name


def check_column_name_providers(atlas=None, column_name=None):
    # check if column_name is None; if it is, set it to default
    if column_name is None and atlas in ["Global", "GBIF"]:
        return "title"
    elif column_name is None:
        return "name"
    return column_name


def check_column_name_ranks(atlas=None, column_name=None):
    if column_name is None:
        return "name"
    return column_name


def check_column_name_reasons(atlas=None, column_name=None):
    if column_name is None:
        return "name"
    return column_name
