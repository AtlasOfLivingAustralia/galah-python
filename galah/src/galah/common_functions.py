from .galah_filter import galah_filter

# for adding filters specifically to atlas_occurrences
def add_predicates(predicates=None,
                   filters=None):

    if type(filters) == str:
        filters = [filters]

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
        for f in filters:
            URL += "&{}".format(galah_filter(f,ifgroupBy=ifGroupBy))

    # filters for all other atlases
    else:

        # check to see if taxa are already in the URL - if not, add fq
        if "fq=" not in URL:
            print("here")
            URL += "fq=%28"
        else:
            URL += "%28"

        # loop over filters
        for f in filters:
            URL += galah_filter(f,ifgroupBy=ifGroupBy) + "%20AND%20"
                    
        # remove last AND and add a closing parenthesis
        URL = URL[:-len("%20AND%20")] + "%29" 

    return URL