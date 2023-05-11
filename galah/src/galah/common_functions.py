from .galah_filter import galah_filter

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
        for f in filters:
            URL += "&{}".format(f,ifgroupBy=ifGroupBy)

    # filters for all other atlases
    else:

        # add parenthesis
        URL += "%28"

        # loop over filters
        for f in filters:
            URL += galah_filter(f,ifgroupBy=ifGroupBy) + "%20AND%20"
                    
        # remove last AND and add a closing parenthesis
        URL = URL[:-len("%20AND%20")] + "%29" 

    return URL