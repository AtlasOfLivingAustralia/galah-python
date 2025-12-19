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

    for selection in select:
        if selection in ["basic", "event", "media"]:
            fields_string += "%2C".join(FIELD_SELECTIONS[selection]) + "%2C"
        else:
            fields_string += "{}%2C".format(selection)
    if fields_string[-3:] == "%2C":
        fields_string = fields_string[:-3]
    return fields_string
