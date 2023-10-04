from .show_values import show_values
from .get_api_url import readConfig

def search_values(field=None,
                  value=None,
                  column_name=None):
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
        verbose : logical
            This option is available for users who want to know what URLs this function is using to get the value. Default to False.

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.search_values(field="basisOfRecord",value="OBS")

    .. program-output:: python -c "import galah; print(galah.search_values(field=\\\"basisOfRecord\\\",value=\\\"OBS\\\"))"
    """

    if value is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field=\"basisOfRecord\"")
    elif type(value) is not str:
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field=\"basisOfRecord\"")
    
    # get initial data frame
    dataFrame = show_values(field=field)
    
    # check for column name to search by
    if column_name is None:
        column_name = dataFrame.columns[-1]

    # throw ValueError if column_name variable is not a string
    elif type(column_name) is not str:
        raise ValueError("Only strings are a valid query for the column_name variable")
    
    # check to see if the user input the correct variable type; else, throw value error
    if type(value) is str:
        return dataFrame.loc[dataFrame[column_name].astype(str).str.contains(value,case=False, na=False)].sort_values(column_name,key=lambda x: x.str.len()).reset_index(drop=True)
    else:
        raise ValueError(
            "You can only pass one string to your search parameter = run show_all(assertions=True) to get strings to pass")