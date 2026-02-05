def print_if_verbose(verbose=False, headers=None, URL=None, method=None, payload=None):
    """Print the headers, URL, method and payload for debugging"""
    if verbose:
        print()
        print("headers: {}".format(headers))
        print()
        print("URL for querying: {}".format(URL))
        print("Method: {}".format(method))
        print()

    if verbose and payload is not None:
        print("Payload: \n\n{}\n".format(payload))
        print()


def kvp_to_columns(kvp_values):
    """
    All data is in the KVP for lists.  Make sure the KVP data is in a pandas dataframe by itself.
    """
    return_dict = {}
    for entry in kvp_values:
        return_dict[entry["key"]] = entry["value"]
    return return_dict


def group_by_atlas_species(group_by=None, rankID=None, URL=None):
    """Tell atlas_species how to group the results"""
    if group_by is not None:

        # add facets into URL
        URL += "&facets={}".format(group_by)

    else:

        # add facets into URL
        URL += "&facets={}".format(rankID)

    return URL


def set_bool_argument(arg=None, name_arg=None):
    # set boolean dict for more efficient variable setting
    boolean_dict = {"True": True, "False": False}

    if isinstance(arg, str) and arg in ["True", "False"]:
        return boolean_dict[arg]
    elif isinstance(arg, bool):
        return arg
    else:
        raise ValueError("Only True/False or boolean values are accepted for {}".format(name_arg))


def is_bool_argument(arg=None, arg_name=None):
    if arg is not None and not isinstance(arg, bool):
        raise ValueError("The {} option only accepts True or False.".format(arg_name))
