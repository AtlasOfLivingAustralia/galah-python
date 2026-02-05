import copy
import itertools

import pandas as pd
import requests

from .common_add_functions import add_filters
from .common_checks import check_string_list
from .common_dictionaries import GROUP_BY_FACETS
from .common_functions import print_if_verbose, set_bool_argument
from .galah_config import get_api_url, readConfig
from .version import __version__


def galah_group_by(
    URL=None, method=None, group_by=None, total_group_by=False, filters=None, verbose=False, payload=None
):
    """
    Used for grouping counts by a specific query, i.e. "year" or "basisOfRecord".  It's mainly utilized in atlas_counts.
    """

    # ---------------------------------------------------------------------------------------------
    # Declare all variables, run checks on compatibility of arguments.
    # ---------------------------------------------------------------------------------------------

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs["galahSettings"]["atlas"]
    verbose = set_bool_argument(arg=configs["galahSettings"]["verbose"], name_arg="verbose")
    authenticate = set_bool_argument(arg=configs["galahSettings"]["authenticate"], name_arg="authenticate")
    access_token = configs["galahSettings"]["access_token"]
    client_id = configs["galahSettings"]["client_id"]

    # get headers
    headers = {"User-Agent": "galah-python {}".format(__version__)}

    # check types for group by and filters
    group_by = check_string_list(group_by, "group_by")
    filters = check_string_list(filters, "filters")

    # check to see how many group_by options we have, because that will determine if we expand this or not
    expand = check_group_by(group_by=group_by)

    # ---------------------------------------------------------------------------------------------
    # First, check to see if a user has chosen the authentication route and there is a payload for
    # the query; if not, pass to the regular processing
    # ---------------------------------------------------------------------------------------------

    # check if authenticate is True and there is a payload
    if authenticate and payload:

        headers["Authorization"] = "Bearer {}".format(access_token)
        headers["client_id"] = client_id

        # get response from your query, which will include all available fields
        qid_URL, method2 = get_api_url(column1="api_name", column1value="occurrences_qid")

        # print information if wanting to know what the URL is
        print_if_verbose(verbose=verbose, headers=headers, URL=qid_URL, method=method2, payload=payload)

        # post the request to get a QID
        qid = requests.request(method2, qid_URL, data=payload, headers=headers)

        # now, add facets to the URL with the QID
        facets = "".join("&facets={}".format(g) for g in group_by)
        if URL[-1] not in ["&"]:
            URL += "?"
        facetURL = URL + "fq=%28qid%3A" + qid.text + "%29" + facets + "&flimit=-1&pageSize=0"

        # if verbose is true, print all new information
        print_if_verbose(verbose=verbose, headers=headers, URL=facetURL, method=method, payload=payload)

        # get data
        response = requests.request(method, facetURL, headers=headers)
        response_json = response.json()

    else:

        # then, add filters
        URL = add_filters(URL=URL, atlas=atlas, filters=filters)

        # then, add facets and round out the URL
        if URL[-1] not in ["&", "?"] and "fq" not in URL:
            URL += "?"
        initial_URL = (
            URL
            + "&"
            + "&".join(["{}={}".format(GROUP_BY_FACETS[atlas], g) for g in group_by])
            + "&flimit=-1&pageSize=0"
        )

        # check to see if the user wants the URL for querying
        print_if_verbose(verbose=verbose, headers=headers, URL=initial_URL, method=method)

        # get response from your query, which will include all available fields
        response = requests.request(method, initial_URL, headers=headers)
        response_json = response.json()

    # ---------------------------------------------------------------------------------------------
    # Now that we have the response from the API, we need to set some common variables for more
    # efficient checking.
    # ---------------------------------------------------------------------------------------------

    # declare facets array
    facets_array = []

    # check if group_by needs to be sorted (if atlas is GBIF)
    group_by = check_needs_sorting(atlas=atlas, group_by=group_by)

    # create common variables for looping
    common_vars = create_common_variables(atlas=atlas, group_by=group_by, response_json=response_json, expand=expand)

    # get all counts for each value
    dict_values = {entry: [] for entry in [*group_by, "count"]}

    # ---------------------------------------------------------------------------------------------
    # If group_by == 2: expand=True, queries are made with group_by values as a filter and
    #                   formatted into a dataframe
    # If group_by == 1: expand=False, data is retrieved from the json and directly formatted into a
    #                   dataframe
    # ---------------------------------------------------------------------------------------------
    if expand:

        facets_array = get_facets_array(
            atlas=atlas,
            facets_array=facets_array,
            group_by=group_by,
            results_array=common_vars["results_array"],
            field_name=common_vars["field_name"],
            facet_name=common_vars["facet_name"],
        )

        combined_facets_array = list(itertools.product(*facets_array))

        # loop over facets array
        # was combined_facets_array
        for f in combined_facets_array:

            # check for GBIF atlas
            if atlas in ["Global", "GBIF"]:

                dict_values = get_GBIF_facets_expand(
                    URL=URL,
                    f=f,
                    group_by=group_by,
                    verbose=verbose,
                    headers=headers,
                    method=method,
                    dict_values=dict_values,
                )

            # do this loop for all other atlases
            else:

                if authenticate:

                    dict_values = get_facets_expand_authenticate(
                        URL=URL,
                        f=f,
                        group_by=group_by,
                        verbose=verbose,
                        headers=headers,
                        method=method,
                        atlas=atlas,
                        expand=expand,
                        dict_values=dict_values,
                        payload=payload,
                    )

                else:

                    dict_values = get_facets_expand(
                        URL=URL,
                        f=f,
                        group_by=group_by,
                        verbose=verbose,
                        headers=headers,
                        method=method,
                        atlas=atlas,
                        expand=expand,
                        dict_values=dict_values,
                    )

        # format table
        counts = pd.DataFrame(dict_values).reset_index(drop=True)
        counts.sort_values(by=group_by)

        # if user wants total, return total number of rows
        counts = return_total_group_by(total_group_by=total_group_by, counts=counts)

        # return dataFrame with all counts values
        return counts

    else:

        # loop over the array length
        for i in range(common_vars["length"]):

            # check if atlas is GBIF
            if atlas in ["Global", "GBIF"]:

                dict_values = get_GBIF_facets(
                    group_by=group_by,
                    results_array=common_vars["results_array"],  # used to be results_array
                    i=i,
                    field_name=common_vars["field_name"],
                    dict_values=dict_values,
                )

            # otherwise, it's all other atlases
            else:

                dict_values = get_facets(
                    results=common_vars["results_array"][i][common_vars["field_name"]],  # results_array[i][field_name]
                    group_by=group_by,
                    expand=expand,
                    dict_values=dict_values,
                )

        # get all counts into a dictionary and sort them
        counts = pd.DataFrame(dict_values).reset_index(drop=True)
        counts.sort_values(by=group_by)

        # if user wants total, return total number of rows
        counts = return_total_group_by(total_group_by=total_group_by, counts=counts)

        # return dataFrame with all counts values
        return counts


###################################################################################################
# Check functions for galah_group_by
###################################################################################################


def check_group_by(group_by=None):
    """check to see if we have multiple group by arguments; return True if so, False if not"""
    # throw error for too many entries in group by
    if len(group_by) > 2:
        raise ValueError("Only 2 groups are allowed, as otherwise the queries will be too complicated.")
    if len(group_by) > 1:
        return True
    return False


def check_needs_sorting(atlas=None, group_by=None):
    # reorder GBIF group by
    if atlas in ["Global", "GBIF"]:
        group_by = sorted(group_by)
    return group_by


###################################################################################################
# Creating common variables for galah_group_by
###################################################################################################


def create_common_variables(atlas=None, group_by=None, response_json=None, expand=None):
    """create a common variables dictionary for straightforward looping for all atlases"""

    common_variables = {
        "length": 0,
        "results_array": None,
        "field_name": "",
        "facet_name": "fq",
    }

    # set some common variables
    if atlas in ["Global", "GBIF"]:
        common_variables["length"] = len(response_json["facets"])
        common_variables["results_array"] = response_json["facets"]
        common_variables["field_name"] = "counts"
        if expand:
            response_json["facets"] = sorted(response_json["facets"], key=lambda d: d["field"])
            common_variables["facet_name"] = "name"  # was name
    elif atlas in ["Brazil"]:
        common_variables["length"] = len(response_json)
        common_variables["results_array"] = response_json
        common_variables["field_name"] = "fieldResult"
    else:
        common_variables["length"] = len(response_json["facetResults"])
        common_variables["results_array"] = response_json["facetResults"]
        common_variables["field_name"] = "fieldResult"

    return common_variables


def get_facets_array(
    atlas=None, facets_array=None, group_by=None, results_array=None, field_name=None, facet_name=None
):
    """Get the facets array for all atlases"""

    # GBIF indexes from 1; all others index from 0
    if atlas not in ["Global", "GBIF"]:
        start = 0
        end = len(group_by) - 1
    else:
        start = 1
        end = len(group_by)

    # Now create facets array
    for i in range(start, end):
        temp_array = []
        if atlas in ["Global", "GBIF"]:
            name = results_array[i]["field"]
            for entry in results_array[i][field_name]:
                temp_array.append("{}:{}".format(name, (entry[facet_name])))
        else:
            for entry in results_array[i][field_name]:
                temp_array.append(entry[facet_name])

        # append this array to the end
        facets_array.append(temp_array)

    # return facets array
    return facets_array


###################################################################################################
# Getting all counts - different atlases and number of facets are taken into account
###################################################################################################


def get_GBIF_facets_expand(URL=None, f=None, group_by=None, verbose=None, headers=None, method=None, dict_values=None):
    """Get all facets from GBIF and expand the values into two columns"""

    # specify start and increment, as GBIF is different from the other atlases
    inc = 0
    start = 1

    # loop over facets
    for facet in f:

        # check if user is grouping by scientific name
        if group_by[start + inc] == "scientificName":
            newURL = (
                URL
                + "&{}={}".format(
                    group_by[start + inc],
                    "%20".join(facet.split(":")[1].split(" ")),
                )
                + "&facet="
                + group_by[start - 1 + inc]
                + "&flimit=-1&pageSize=0"
            )
        else:
            newURL = (
                URL
                + "&{}={}".format(group_by[start + inc], facet.split(":")[1])
                + "&facet="
                + group_by[start - 1 + inc]
                + "&flimit=-1&pageSize=0"
            )

        # increase your increment for looping
        inc += 1

    # check to see if the user wants the querying URL
    print_if_verbose(verbose=verbose, headers=headers, URL=newURL, method=method)

    # get the data
    response = requests.request(method=method, url=newURL, headers=headers)
    response_json = response.json()

    # put data in dict
    for entry in response_json["facets"][0]["counts"]:
        dict_values[group_by[start - 1]].append(entry["name"])
        dict_values["count"].append(int(entry["count"]))
        dict_values[group_by[start]].append(facet.split(":")[1])
        for key in dict_values:
            if (key != group_by[start]) and (key != group_by[start - 1]) and (key != "count"):
                dict_values[key].append("-")

    return dict_values


def get_facets_expand(
    URL=None,
    f=None,
    group_by=None,
    verbose=None,
    headers=None,
    method=None,
    atlas=None,
    expand=False,
    dict_values=None,
):
    """For all atlases other than GBIF, get the names and values of the group by list"""

    # loop over facets
    for facet in f:

        # split each facet to make it human readable
        name, value = facet.split(":")
        value = value.replace('"', "")

        # if name is in your group_by statement, do this loop
        if name in group_by:

            tempURL = get_tempURL(URL=URL, name=name, value=value, group_by=group_by)

            # check to see if the user wants the querying URL
            print_if_verbose(verbose=verbose, headers=headers, URL=tempURL, method=method)

            # get data
            response = requests.request(method, tempURL, headers=headers)
            response_json = response.json()

            # if there is no data available, move onto next variable
            if atlas in ["Brazil"]:
                if response_json is None or not response_json[0]["fieldResult"]:
                    continue
            else:
                if response_json is None or not response_json["facetResults"]:
                    continue

            # put data in table (and check if user wants Brazil, because that is an exception)
            results_array = get_results_array_expand(response_json=response_json, atlas=atlas, group_by=group_by)

            # loop over each entry in the results
            for entry in results_array:

                if entry["fq"].split(":")[0] in group_by:

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
                dict_values = put_entries_in_grouped_dict(entry=entry, dict_values=dict_values, expand=expand)

    return dict_values


def get_GBIF_facets(group_by=None, results_array=None, i=None, field_name=None, dict_values=None):
    """Get all facets from GBIF and put into dictionary"""

    # loop over each group and make sure entry is human readable and have a dash if
    # it doesn't have a count; return dictionary values
    for g in group_by:

        # check for an underscore in the name; if so, change to camel case
        if "_" in results_array[i]["field"]:
            test_name = results_array[i]["field"].split("_")
            for k in range(len(test_name)):
                test_name[k] = test_name[k].lower()
                if k > 0:
                    test_name[k] = test_name[k].capitalize()
            test_name = "".join(test_name)

        # otherwise, change to lowercase
        else:
            test_name = results_array[i]["field"].lower()

        # check to see for empty values - if empty values, add "-" rather than NaN
        if test_name == g:
            for item in results_array[i][field_name]:
                dict_values[g].append(item["name"])
                dict_values["count"].append(int(item["count"]))
                for entry in dict_values:
                    if (entry != g) and (entry != "count"):
                        dict_values[entry].append("-")

    # return dictionary values
    return dict_values


def get_facets(results=None, group_by=None, expand=None, dict_values=None):
    """Get the facets for all other atlases and put into dictionary"""

    # loop over entry in results
    for entry in results:

        # loop over each group and make sure entry is human readable and have a dash if
        # it doesn't have a count
        for g in group_by:

            # check for only items you want
            if g in entry["fq"] and entry["fq"].split(":")[0] == g:

                # add values to dictionary
                dict_values = put_entries_in_grouped_dict(
                    entry=entry,
                    dict_values=dict_values,
                    expand=expand,
                )

    # return resulting dict_values
    return dict_values


def get_facets_expand_authenticate(
    URL=None,
    f=None,
    group_by=None,
    verbose=None,
    headers=None,
    method=None,
    atlas=None,
    expand=None,
    dict_values=None,
    payload=None,
):
    """Return the dictionary values for two groups when the authenticate option is set to True"""

    # loop over facets
    for facet in f:

        # split each facet to make it human readable
        name, value = facet.split(":")
        value = value.replace('"', "")

        # if name is in your group_by statement, do this loop
        if name in group_by:

            # create a different payload to the original so you can:
            #     1) add the facets as filters for group_by counts
            #     2) in case filters and group_by have the same names in them
            temp_payload = copy.deepcopy(payload)
            if "fq" not in temp_payload:
                temp_payload["fq"] = [f]
            else:
                if any(name in x for x in temp_payload["fq"]):
                    temp_payload["fq"] = [x for x in temp_payload["fq"] if name not in x]
                    temp_payload["fq"].append(f)

            # create payload and get qid
            qid_URL, method2 = get_api_url(column1="api_name", column1value="occurrences_qid")

            # print options if verbose is set to True
            print_if_verbose(verbose=verbose, headers=headers, URL=qid_URL, method=method2, payload=temp_payload)

            # get the QID of the query
            qid = requests.request(method2, qid_URL, data=temp_payload, headers=headers)

            # make the URL with the QID
            if URL[-1] not in ["&", "?"]:
                tempURL = URL + "?"
            else:
                tempURL = URL + "fq=%28qid%3A" + qid.text + "%29"

            # add facets to the QID
            tempURL += "&facets={}".format(group_by[-1])

            # check to see if the user wants the querying URL
            print_if_verbose(verbose=verbose, headers=headers, URL=tempURL, method=method)

            # get data
            response = requests.request(method, tempURL, headers=headers)
            response_json = response.json()

            # if there is no data available, move onto next variable
            if response_json is None or not response_json["facetResults"]:
                continue

            # put data in table (and check if user wants Brazil, because that is an exception)
            results_array = get_results_array_expand(response_json=response_json, atlas=atlas, group_by=group_by)

            # loop over each entry in the results
            for entry in results_array:

                # check to see if the name of the facet is in the group_by array - sometimes,
                # there is a name with extra characters and we don't want that one
                if entry["fq"].split(":")[0] in group_by:

                    # potentially tab again
                    dict_values = put_entries_in_grouped_dict(entry=entry, dict_values=dict_values, expand=expand)

    # return the dictionary values
    return dict_values


def return_total_group_by(total_group_by=None, counts=None):
    """Return the number of rows if someone wants the total number of values"""

    # check to see if user has specified this option
    if total_group_by:
        return pd.DataFrame({"count": [counts.shape[0]]})

    # if option not specified, return the counts given to the function
    return counts


###################################################################################################
# Functions that support the support functions
###################################################################################################


def get_results_array_expand(response_json=None, atlas=None, group_by=None):
    """Return the list of dicts containing the names and counts of facetes"""

    # check for Brazil, since they're handled differently
    if atlas in ["Brazil"]:

        # index is 0 for len(group_by) <=2; else, you have to increment this
        if len(group_by) <= 2:
            return response_json[0]["fieldResult"]
        else:
            return response_json[1]["fieldResult"]

    # for all other atlases, data is in "facetResults" under the first entry and "fieldResult"
    else:
        return response_json["facetResults"][0]["fieldResult"]


def put_entries_in_grouped_dict(entry=None, dict_values=None, expand=None, associated_value=None):
    """Creating dictionaries for galah_group_by"""

    # update dict values with entry
    name, dict_values = get_name_value_grouped_dict(entry=entry, dict_values=dict_values)

    # check for a group_by array with length of 2
    if expand:

        # because it is expanded, loop over all key in dict values
        for key in dict_values:
            if (key != name) and (key != "count"):
                while len(dict_values[key]) < len(dict_values["count"]):
                    dict_values[key].append("-")  # was "-"

    # otherwise, group_by array has length 1
    else:

        # only go over entries because it is not expanded
        for entry in dict_values:
            if (entry != name) and (entry != "count"):
                dict_values[entry].append("-")

    # return the dict_values
    return dict_values


def get_name_value_grouped_dict(entry=None, dict_values=None):
    """Put the values from the provided entry into the dict_values"""

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


def get_tempURL(URL=None, name=None, value=None, group_by=None):
    """Get the tempURL for getting expanded values"""

    # add name and value of facet as filter (for non-authentication procedures)
    tempURL = URL + "%20AND%20%28{}%3A%22{}%22%29".format(name, value)

    # now, loop over the rest of the facets in group_by
    for group in group_by:
        if (group != name) and ("facets={}".format(group) not in URL):
            tempURL += "&facets={}".format(group)

    # finalise the URL for querying
    tempURL += "&flimit=-1&pageSize=0"

    # return tempURL for querying
    return tempURL
