def print_if_verbose(verbose=False, headers=None, URL=None, method=None, payload=None):
    """Print the headers, URL, method and payload for debugging"""
    if verbose:
        print()
        print("headers: {}".format(headers))
        print()
        print("URL for querying: {}".format(URL))
        print("Method: {}".format(method))
        print()

    if payload is not None:
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
