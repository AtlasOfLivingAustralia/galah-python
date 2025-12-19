import pandas as pd
import requests

from .common_functions import kvp_to_columns, print_if_verbose
from .galah_config import get_api_url, readConfig


def show_values(field=None, lists=False, all_fields=False, verbose=False, config_file=None):
    """
    Users may wish to see the specific values within a chosen field, profile or list to narrow queries or understand
    more about the information of interest. ``show_values()`` provides users with these values.

    Parameters
    ----------
        field : string
            A string to specify what type of parameters should be shown.
        lists : logical
            This lets ``show_values()`` know if you want to look up fields, or if you want to look up species in lists.  Default is False.
        all_fields : logical
            For threatened and sensitive lists, this argument will give you the option of downloading species statuses.  Default is False.
        verbose : logical
            This option is available for users who want to know what URLs this function is using to get the value.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.show_values(field='basisOfRecord')

    .. program-output:: python -c "import galah; print(galah.show_values(field=\\\'basisOfRecord\\\'))"
    """

    # check to see if field is input correctly
    if field is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field='basisOfRecord'")
    elif type(field) is not str:
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field='basisOfRecord'")

    # get configurations
    configs = readConfig(config_file=config_file)

    # get atlas
    atlas = configs["galahSettings"]["atlas"]

    # get headers
    headers = {}

    # get base URL for querying
    if atlas in ["Global", "GBIF"]:
        baseURL, method = get_api_url(column1="api_name", column1value="records_counts")
        URL = baseURL + "?facet=" + field + "&flimit=-1"
    else:
        if lists:
            baseURL, method = get_api_url(column1="called_by", column1value="show_values-lists")
            URL = baseURL.replace("{list_id}", field) + "?max=-1"
            if all_fields:
                URL += "&includeKVP=TRUE"
        else:
            baseURL, method = get_api_url(column1="api_name", column1value="records_facets")
            URL = baseURL + "?facets=" + field + "&flimit=-1"

    # check to see if the user wants the URL for querying
    print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

    # query the API
    response = requests.request(method, URL, headers=headers)
    response_json = response.json()

    # return dataFrame
    return process_value_results(atlas=atlas, response_json=response_json, lists=lists, all_fields=all_fields)


def process_value_results(atlas=None, response_json=None, lists=False, all_fields=False):
    """
    This function is for getting all assertions available in the chosen atlas.

    Parameters
    ----------
        atlas : str
            Name of the atlas you are getting information from.
        response_json : dict
            Response from the API in a JSON format
        lists : logical
            This lets ``show_values()`` know if you want to look up fields, or if you want to look up species in lists.  Default is False.
        all_fields : logical
            For threatened and sensitive lists, this argument will give you the option of downloading species statuses.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame`` containing all data of interest.
    """
    # create empty dataFrame to concatenate results to
    dataFrame = pd.DataFrame()

    # loop over results - look to see if GBIF is being used
    if atlas in ["Global", "GBIF"]:
        result = response_json["facets"][0]["counts"]
        for entry in result:
            tempdf = pd.DataFrame(
                {
                    "field": response_json["facets"][0]["field"],
                    "category": entry["name"],
                },
                index=[0],
            )  # facets
            dataFrame = pd.concat([dataFrame, tempdf], ignore_index=True)

    # otherwise, assume it is other atlases
    else:
        if lists:
            if all_fields:
                dataFrame = pd.DataFrame()
                for i in response_json:
                    kvp_values = i["kvpValues"]
                    flattened_values = kvp_to_columns(kvp_values)
                    i.update(flattened_values)
                    del i["kvpValues"]
                    dataFrame = pd.concat([dataFrame, pd.DataFrame(i, index=[0])])
                return dataFrame.reset_index(drop=True)
            return pd.DataFrame(response_json)
        else:
            result = response_json[0]["fieldResult"]
            for i, entry in enumerate(result):
                # check if last character is a full stop
                tempdf = pd.DataFrame([entry["i18nCode"].split(".")], columns=["field", "category"])
                dataFrame = pd.concat([dataFrame, tempdf], ignore_index=True)

    return dataFrame
