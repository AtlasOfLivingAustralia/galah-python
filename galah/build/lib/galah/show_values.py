import requests
import pandas as pd

from .get_api_url import get_api_url,readConfig

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

    # check to see if field is input correctly
    if field is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field=\"basisOfRecord\"")
    elif type(field) is not str:
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field=\"basisOfRecord\"")

    # get configurations
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas']

    headers = {}

    # get headers
    #if atlas in ["Australia","ALA"]:
    #    headers = {"x-api-key": configs["galahSettings"]["ALA_API_key"]}
    #else:
    #    headers = {}

    # get base URL for querying
    if atlas in ["Global","GBIF"]:
        baseURL,method = get_api_url(column1='api_name',column1value='records_counts')
        URL = baseURL + "?facet=" + field + "&flimit=-1"
        '''
        url,chosen_title,column_titles

        # get parameters from website
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')

        # find the title of table and get title
        table_titles = soup.select('h3')
        for i,title in enumerate(table_titles):
            if title.text == chosen_title:
                index=i
        table_to_parse = soup.find_all('table')[index]
        '''
    else:
        baseURL,method = get_api_url(column1='api_name',column1value='records_facets')
        URL = baseURL + "?facets=" + field + "&flimit=-1"

    # check to see if the user wants the URL for querying
    if verbose:
        print("URL for querying:\n\n{}\n".format(URL))

    # query the API
    response = requests.request(method,URL,headers=headers)
    response_json = response.json()
    
    # create empty dataFrame to concatenate results to
    dataFrame = pd.DataFrame()

    # loop over results - look to see if GBIF is being used
    if atlas in ["Global","GBIF"]:
        result = response_json['facets'][0]['counts']
        for entry in result:
            tempdf = pd.DataFrame({'field': response_json['facets'][0]['field'], 'category': entry['name']},index=[0]) # facets
            dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)
    
    # otherwise, assume it is other atlases
    else:
        result = response_json[0]['fieldResult']
        for i,entry in enumerate(result):
            # check if last character is a full stop
            if entry['i18nCode'][-1] == ".":
                # check to see if the length is more than 2
                if len(entry['i18nCode'].split('.')) > 2:
                    temparray = entry['i18nCode'].split('.')
                    name = " ".join(temparray[1:])
                    tempdf = pd.DataFrame([[temparray[0],name]],columns=['field','category'])
                else:
                    tempdf = pd.DataFrame([entry['i18nCode'][0:-1].split('.')], columns=['field', 'category'])
                dataFrame = pd.concat([dataFrame, tempdf], ignore_index=True)
            elif len(entry['i18nCode'].split('.')) > 2:
                temparray = entry['i18nCode'].split('.')
                name = " ".join(temparray[1:])
                tempdf = pd.DataFrame([[temparray[0],name]],columns=['field','category'])
                dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)
            else:
                tempdf = pd.DataFrame([entry['i18nCode'].split('.')],columns=['field','category'])
                dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

    # return dataFrame
    return dataFrame

    '''
    # add checks to make sure that the field they entered actually is something they can query
    ### TODO: brainstorm
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