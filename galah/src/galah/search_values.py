from .show_values import show_values


def search_values(field=None, value=None, lists=False, all_fields=False, column_name=None, config_file=None):
    """
    Users may wish to see the specific values within a chosen field, profile or list to narrow queries or understand
    more about the information of interest. ``search_values()`` allows users for search for specific values within
    a specified field.

    Parameters
    ----------
        field : string
            A string to specify what type of parameters should be searched.
        value : string
            A string specifying a search term. Not case sensitive.
        lists : logical
            This lets ``show_values()`` know if you want to look up fields, or if you want to look up species in lists.  Default is False.
        all_fields : logical
            For threatened and sensitive lists, this argument will give you the option of downloading species statuses.  Default is False.
        verbose : logical
            This option is available for users who want to know what URLs this function is using to get the value. Default to False.

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.search_values(field='basisOfRecord',value='OBS')

    #.. program-output:: python -c 'import galah; print(galah.search_values(field=\\\'basisOfRecord\\\',value=\\\'obs\\\'))'
    """

    if value is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field='basisOfRecord'")

    if not isinstance(value, str):
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field='basisOfRecord'")

    if column_name is not None and not isinstance(column_name, str):
        raise ValueError("Only strings are a valid query for the column_name variable")

    # get initial data frame
    dataFrame = show_values(field=field, lists=lists, all_fields=all_fields, config_file=config_file)

    if column_name is None:
        column_name = dataFrame.columns[-1]

    # check to see if the user input the correct variable type; else, throw value error
    return (
        dataFrame.loc[dataFrame[column_name].astype(str).str.contains(value, case=False, na=False)]
        .sort_values(column_name, key=lambda x: x.str.len())
        .reset_index(drop=True)
    )
