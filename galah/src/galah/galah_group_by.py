import itertools
import urllib

import pandas as pd
import requests

from .common_functions import print_if_verbose
from .galah_config import readConfig
from .galah_filter import add_filters
from .version import __version__


def galah_group_by(
    URL=None,
    method=None,
    group_by=None,
    total_group_by=False,
    filters=None,
    payload={},
    verbose=False,
):
    """
    Used for grouping counts by a specific query, i.e. "year" or "basisOfRecord".  It's mainly utilized in atlas_counts.
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs["galahSettings"]["atlas"]

    # get headers
    headers = {"User-Agent": "galah-python {}".format(__version__)}

    # check for group_by
    if group_by is None:

        # raise error, as you want this specified for this function
        raise ValueError("Please specify how to group your results.  Examples are: 'year', 'basisOfRecord'")

    if isinstance(group_by, (list, str)):

        if isinstance(group_by, str):
            group_by = [group_by]

        if len(group_by) > 3:
            raise ValueError("Only 3 groups are allowed, as otherwise the queries will get complicated")

    # check if expand option works
    if type(group_by) is list and len(group_by) > 1:
        ifGroupBy = True
    else:
        ifGroupBy = False

    # first, check for filters
    if filters is not None:

        # check type of filter
        if isinstance(filters, (str, list)):

            URL = add_filters(URL=URL, atlas=atlas, filters=filters, ifGroupBy=ifGroupBy)

        # else, raise a TypeError because this variable needs to be either a string or a list
        else:
            raise TypeError("Your filters need to either be a string (for one filter), or a list of strings.")

    # loop over group_by
    for g in group_by:

        # ensure each group is given its own facet
        if atlas in ["Global", "GBIF"]:
            URL += "&facet={}".format(g)
        else:
            URL += "&facets={}".format(g)

    ### TODO: start here

    # round out the URL
    startingURL += "&flimit=-1&pageSize=0"

    # check to see if the user wants the URL for querying
    print_if_verbose(verbose=verbose, headers=headers, URL=startingURL, method=method)

    # get response from your query, which will include all available fields
    response = requests.request(method, startingURL, headers=headers)
    response_json = response.json()
    facets_array = []

    # set some common variables
    if atlas in ["Global", "GBIF"]:
        group_by = sorted(group_by)
        length = len(response_json["facets"])
        results_array = response_json["facets"]
        field_name = "counts"
        if ifGroupBy:
            response_json["facets"] = sorted(response_json["facets"], key=lambda d: d["field"])
            results_array = response_json["facets"]
            facet_name = "name"
    elif atlas in ["Brazil"]:
        length = len(response_json)
        results_array = response_json
        field_name = "fieldResult"
        facet_name = "fq"
    else:
        length = len(response_json["facetResults"])
        results_array = response_json["facetResults"]
        field_name = "fieldResult"
        if ifGroupBy:
            facet_name = "fq"

    # get all counts for each value
    dict_values = {entry: [] for entry in [*group_by, "count"]}

    # do this if the expand option is try
    if ifGroupBy:

        # was 1,len(group_by)
        if atlas not in ["Global", "GBIF"]:
            start = 0
            end = len(group_by) - 1
        else:
            start = 1
            end = len(group_by)

        # now do loop
        for i in range(start, end):
            temp_array = []
            for entry in results_array[i][field_name]:
                temp_array.append(entry[facet_name])
            facets_array.append(temp_array)

        combined_facets_array = list(itertools.product(*facets_array))

        # loop over facets array
        # was combined_facets_array
        for f in combined_facets_array:

            # check for GBIF atlas
            if atlas in ["Global", "GBIF"]:

                inc = 0

                for facet in f:

                    # was i+1
                    tempURL = (
                        URL
                        + "&{}={}".format(group_by[start + inc], urllib.parse.quote(facet))
                        + "&facet="
                        + group_by[start - 1 + inc]
                        + "&flimit=-1&pageSize=0"
                    )

                    # check if user is grouping by scientific name
                    # i + 1
                    if group_by[start + inc] == "scientificName":
                        tempURL = (
                            URL
                            + "&{}={}".format(
                                group_by[start + inc],
                                "%20".join(facet.split(" ")[0:2]),
                            )
                            + "&facet="
                            + group_by[start - 1 + inc]
                            + "&flimit=-1&pageSize=0"
                        )
                    else:
                        tempURL = (
                            URL
                            + "&{}={}".format(group_by[start + inc], "%20".join(facet.split(" ")))
                            + "&facet="
                            + group_by[start - 1 + inc]
                            + "&flimit=-1&pageSize=0"
                        )

                    inc += 1

                if verbose:
                    print()
                    print("URL for querying: {}".format(tempURL))
                    print("Method: {}".format(method))
                    print()

                # get the data
                response = requests.request(method, tempURL, headers=headers)
                response_json = response.json()

                # put data in dict
                for entry in response_json["facets"][0]["counts"]:
                    dict_values[group_by[start - 1]].append(entry["name"])
                    dict_values["count"].append(int(entry["count"]))
                    dict_values[group_by[start]].append(facet)
                    for key in dict_values:
                        if (key != group_by[start]) and (key != group_by[start - 1]) and (key != "count"):
                            dict_values[key].append("-")

            # do this loop for all other atlases
            else:
                for facet in f:

                    # split each facet to make it human readable
                    name, value = facet.split(":")
                    value = value.replace('"', "")
                    if name in group_by:
                        tempURL = URL + "%20AND%20%28{}%3A%22{}%22%29".format(name, value)
                        for group in group_by:
                            if (group != name) and ("facets={}".format(group) not in URL):
                                tempURL += "&facets={}".format(group)

                        # finalise the URL for querying
                        tempURL += "&flimit=-1&pageSize=0"

                        # check to see if the user wants the URL for querying
                        if verbose:
                            print()
                            print("URL for querying: {}".format(tempURL))
                            print("Method: {}".format(method))
                            print()

                        # get data
                        response = requests.request(method, tempURL, headers=headers)
                        response_json = response.json()

                        # if there is no data available, move onto next variable
                        if atlas not in ["Brazil"]:
                            if response_json is None or not response_json["facetResults"]:
                                continue
                        else:
                            if response_json is None or not response_json[0]["fieldResult"]:
                                continue

                        # put data in table (and check if user wants Brazil, because that is an exception)
                        if atlas in ["Brazil"]:
                            if len(group_by) <= 2:
                                results_array = response_json[0]["fieldResult"]
                            else:
                                results_array = response_json[1]["fieldResult"]
                        else:
                            results_array = response_json["facetResults"][0]["fieldResult"]

                        # loop over each entry in the results
                        for entry in results_array:

                            if entry["fq"].split(":")[0] in group_by:

                                # add facet value to dictionary for expand
                                for facet in f:

                                    if len(facet.split(":")) > 2:
                                        name_and_values = facet.split(":")
                                        name = name_and_values[0]
                                        value = ":".join(name_and_values[1:])
                                    else:
                                        name, value = facet.split(":")
                                    value = value.replace('"', "")
                                    # trying this - potentially remove it
                                    if name in group_by and name not in entry["fq"].split(":"):
                                        dict_values[name].append(value)

                            # potentially tab again
                            dict_values = put_entries_in_grouped_dict(
                                entry=entry,
                                dict_values=dict_values,
                                expand=ifGroupBy,
                            )

        # format table
        counts = pd.DataFrame(dict_values).reset_index(drop=True)
        counts.sort_values(by=group_by)

        # if user wants total, return total number of rows
        if total_group_by:
            return pd.DataFrame({"count": [counts.shape[0]]})

        # return dataFrame with all counts values
        return counts

    # else, expand is False
    else:

        # loop over the array length
        for i in range(length):

            # check if atlas is GBIF
            if atlas in ["Global", "GBIF"]:

                # loop over each group and make sure entry is human readable and have a dash if
                # it doesn't have a count
                for g in group_by:
                    if "_" in results_array[i]["field"]:
                        test_name = results_array[i]["field"].split("_")
                        for k in range(len(test_name)):
                            test_name[k] = test_name[k].lower()
                            if k > 0:
                                test_name[k] = test_name[k].capitalize()
                        test_name = "".join(test_name)
                    else:
                        test_name = results_array[i]["field"].lower()
                    if test_name == g:
                        for item in results_array[i][field_name]:
                            dict_values[g].append(item["name"])
                            dict_values["count"].append(int(item["count"]))
                            for entry in dict_values:
                                if (entry != g) and (entry != "count"):
                                    dict_values[entry].append("-")

            # otherwise, it's all other atlases
            else:

                # loop over entry in results
                for entry in results_array[i][field_name]:

                    # loop over each group and make sure entry is human readable and have a dash if
                    # it doesn't have a count
                    for g in group_by:

                        # check for only items you want
                        if g in entry["fq"] and entry["fq"].split(":")[0] == g:

                            # add values to dictionary
                            dict_values = put_entries_in_grouped_dict(
                                entry=entry,
                                dict_values=dict_values,
                                expand=ifGroupBy,
                            )

        # get all counts into a dictionary and sort them
        counts = pd.DataFrame(dict_values).reset_index(drop=True)
        counts.sort_values(by=group_by)

        # if user wants total, return total number of rows
        if total_group_by:
            return pd.DataFrame({"count": [counts.shape[0]]})

        # return dataFrame with all counts values
        return counts


def put_entries_in_grouped_dict(entry=None, dict_values=None, expand=None):
    """Creating dictionaries for galah_group_by"""

    # update dict values with entry
    name, dict_values = get_name_value_grouped_dict(entry=entry, dict_values=dict_values)

    if expand:

        # because it is expanded, loop over all key in dict values
        for key in dict_values:
            if (key != name) and (key != "count"):
                while len(dict_values[key]) < len(dict_values["count"]):
                    dict_values[key].append("-")

    else:

        # only go over entries because it is not expanded
        for entry in dict_values:
            if (entry != name) and (entry != "count"):
                dict_values[entry].append("-")

    # return the dict_values
    return dict_values


def get_name_value_grouped_dict(entry=None, dict_values=None):

    # check the values
    if len(entry["fq"].split(":")) > 2:
        name_and_values = entry["fq"].split(":")
        name = name_and_values[0]
        value = ":".join(name_and_values[1:])
    else:
        name, value = entry["fq"].split(":")

    # replace any quotes and check for integers for values
    value = value.replace('"', "")
    if value.isdigit():
        value = int(value)

    # if name is an expected value (i.e. not NaN or *-), add value to your dict
    if name in dict_values:
        dict_values[name].append(value)
        dict_values["count"].append(int(entry["count"]))

    # return both the name and dict values
    return name, dict_values
