import requests,os,configparser
import pandas as pd
from .show_values import show_values

def search_values(field=None,value=None,column_name=None):
    """
    Used for getting the values from a field you want to query.  To see how this is used, type

    .. prompt:: python

        import galah
        galah.search_values(field="basisOfRecord",value="OBS")

    which returns

    .. program-output:: python3 -c "import galah; print(galah.search_values(field=\\\"basisOfRecord\\\",value=\\\"OBS\\\"))"
    """

    if value is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field=\"basisOfRecord\"")
    elif type(value) is not str:
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field=\"basisOfRecord\"")

    dataFrame = show_values(field=field)
    
    if column_name is None:
        column_name = dataFrame.columns[-1]
    # throw ValueError if column_name variable is not a string
    elif type(column_name) is not str:
        raise ValueError("Only strings are a valid query for the column_name variable")
    # check to see if the user input the correct variable type; else, throw value error
    if type(value) is str:
        return dataFrame.loc[dataFrame[column_name].astype(str).str.contains(value,case=True, na=False)].sort_values(column_name,key=lambda x: x.str.len())
    else:
        raise ValueError(
            "You can only pass one string to your search parameter = run show_all(assertions=True) to get strings to pass")