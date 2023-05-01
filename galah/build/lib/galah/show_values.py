import requests
import pandas as pd

from .get_api_url import get_api_url

# comment on what this function does later
def show_values(field=None,
                verbose=False):
    """
    Users may wish to see the specific values within a chosen field, profile or list to narrow queries or understand 
    more about the information of interest. ``show_values()`` provides users with these values. 

    Parameters
    ----------
        field : string
            A string to specify what type of parameters should be shown.  
        verbose : logical
            This option is available for users who want to know what URLs this function is using to get the value.  Default is False.

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.show_values(field="basisOfRecord")

    .. program-output:: python -c "import galah; print(galah.show_values(field=\\\"basisOfRecord\\\"))"
    """

    if field is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field=\"basisOfRecord\"")
    elif type(field) is not str:
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field=\"basisOfRecord\"")

    # get base URL for querying
    baseURL = get_api_url(column1='api_name',column1value='records_facets')

    '''
    # add a buttload of checks to make sure that the field they entered actually is something they can query
    ### TODO: talk to Martin about this
    # "field", "profile", "list", "collection", "dataset", "provider")
    #collection,datasets,fields,lists,profiles,providers
    raw_valid_values = show_all(collection=True,datasets=True,fields=True,lists=True,profiles=True,providers=True)
    for i,df in enumerate(raw_valid_values):
        if i == 0:
            if 'listName' in list(df.columns):
                valid_values = df['listName']
            elif 'name' in list(df.columns):
                valid_values = df['name']
            else:
                raise ValueError("Amanda needs to find another name from this list: {}".format(list(df.columns)))
        else:
            if 'listName' in list(df.columns):
                valid_values = pd.concat([valid_values,df['listName']],ignore_index=True)
            elif 'name' in list(df.columns):
                valid_values = pd.concat([valid_values, df['name']], ignore_index=True)
            else:
                raise ValueError("Amanda needs to find another name from this list: {}".format(list(df.columns)))

    # make this a list for easy comparison
    valid_values = list(valid_values)

    if field not in valid_values:
        raise ValueError("{} is not a valid field query.  Use the show_all() function with any of the following set as"
                         "True to show valid values:\n\n"
                         "collection, datasets, fields, lists, profiles, providers\n")
    '''
    # add the field
    URL = baseURL + "?facets=" + field + "&flimit=10000"

    # check to see if the user wants the URL for querying
    if verbose:
        print("URL for querying:\n\n{}\n".format(URL))

    # query the API
    response = requests.get(URL)
    json = response.json()

    # create empty dataFrame to concatenate results to
    dataFrame = pd.DataFrame()

    # loop over results and create dataFrame
    for i,entry in enumerate(json[0]['fieldResult']):
        # check if last character is a full stop
        if entry['i18nCode'][-1] == ".":
            tempdf = pd.DataFrame([entry['i18nCode'][0:-1].split('.')], columns=['field', 'category'])
            dataFrame = pd.concat([dataFrame, tempdf], ignore_index=True)
        else:
            tempdf = pd.DataFrame([entry['i18nCode'].split('.')],columns=['field','category'])
            dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

    # return dataFrame
    return dataFrame