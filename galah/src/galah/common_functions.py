import requests
from .galah_filter import galah_filter
from .get_api_url import get_api_url

# for adding filters specifically to atlas_occurrences
def add_predicates(predicates=None,
                   filters=None):

    if type(filters) == str:
        filters = [filters]

    if any("!=" in f for f in filters):
        raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")

    for f in filters:

        predicates.append(galah_filter(f,occurrencesGBIF=True))

    return predicates

# for adding filters to the URL
def add_filters(URL=None,
                atlas=None,
                filters=None,
                ifGroupBy=False):

    # change type of filters to list for easy looping
    if type(filters) == str:
        filters = [filters]

    # check if the atlas being used is GBIF
    if atlas in ["Global","GBIF"]:

        # check for filters that are not valid with GBIF
        if any("!=" in f for f in filters):
            raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")
        else:
            for f in filters:
                URL += "&{}".format(galah_filter(f,ifgroupBy=ifGroupBy))

    # filters for all other atlases
    else:

        # check to see if taxa are already in the URL - if not, add fq
        if "fq=" not in URL:
            URL += "fq=%28"
        else:
            URL += "%28"

        # loop over filters
        for f in filters:
            URL += galah_filter(f,ifgroupBy=ifGroupBy) + "AND" 
                    
        # remove last AND and add a closing parenthesis
        URL = URL[:-len("AND")] + "%29"
        
    return URL

def get_response_show_all(column1=None,
                      column1value=None,
                      column2=None,
                      column2value=None,
                      atlas=None,
                      headers={},
                      max_entries=-1,
                      offset=None):

    # get data and check for 
    URL,method = get_api_url(column1=column1,column1value=column1value,column2=column2,column2value=column2value)
    if max_entries is not None and offset is not None:
        URL += "?max={}&offset={}".format(max_entries,offset)
    response = requests.request(method,URL,headers=headers)
    if response.status_code == 403:
        raise ValueError("Provide a/an {} API key to get this information".format(atlas))
    if response.status_code == 429:
        raise ValueError("You have reached the maximum number of daily queries for the ALA.")

    # return response
    return response