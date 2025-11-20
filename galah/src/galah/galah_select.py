from .common_dictionaries import FIELD_SELECTIONS


def galah_select(select=None):
    """
    This function will take a list of fields to pass to the ALA and put them together in a string

    Parameters
    ----------
        taxa : string / list
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.

    Returns
    -------
        An object of class ``pandas.DataFrame``.
    """
    # generate a temporary string for fields to return to another function
    fields_string = "fields="

    # check if this argument is provided
    if select is None:
        raise ValueError("You need to provide one argument: category(ies) to get from the ALA API as a string or list.")

    # otherwise, create a URL string and return it
    elif type(select) is str or type(select) is list:
        if type(select) is str:
            select = [select]
        for selection in select:
            if selection in ["basic", "event", "media"]:
                fields_string += "%2C".join(FIELD_SELECTIONS[selection]) + "%2C"
            else:
                fields_string += "{}%2C".format(selection)
        if fields_string[-3:] == "%2C":
            fields_string = fields_string[:-3]
        return fields_string

    # else, throw an error
    else:
        raise ValueError("This function only takes strings or lists as its arguments")
