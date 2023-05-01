import requests
import pandas as pd
from .galah_filter import galah_filter

'''
TODO
----
1. Generalise this to N group_by, where N>2


'''
def galah_group_by(URL,
                   group_by=None,
                   filters=None,
                   expand=True,
                   verbose=False
                   ):
    """
    Used for grouping counts by a specific query, i.e. "year" or "basisOfRecord".  It's mainly utilized in atlas_counts.
    """

    # check if expand option works
    if expand:
        ifGroupBy = True
    else:
        ifGroupBy = False

    # first, check for filters
    if filters is not None:

        # check type of filter
        if type(filters) == str or type(filters) == list:

            # change type of filters to list for easy looping
            if type(filters) == str:
                filters = [filters]

            URL += "%28"

            # loop over filters
            for f in filters:
                
                URL += galah_filter(f,ifgroupBy=ifGroupBy) + "%20AND%20"
                   
            URL = URL[:-len("%20AND%20")] + "%29" 

        # else, raise a TypeError because this variable needs to be either a string or a list
        else:
            raise TypeError("Your filters need to either be a string (for one filter), or a list of strings.")

    # check for group_by
    if group_by is None:

        # raise error, as you want this specified for this function
        raise ValueError("Please specify how to group your results.  Examples are: \'year\', \'basisOfRecord\'")

    # check for variable type
    elif type(group_by) is str or type(group_by) is list:

        # change to list for easy looping
        if type(group_by) is str:
            group_by=[group_by]

        # check to see if the expand option is true
        if expand:

            # check to see if you can expand upon this
            if len(group_by) == 1:
                raise ValueError("You cannot use the expand=True option when you only have one group")

            # create a base URL
            startingURL = URL

            # loop over group_by
            for g in group_by:

                startingURL += "&facets={}".format(g)

            # round out the URL
            startingURL += "&flimit=10000&pageSize=0"

            # check to see if the user wants the URL for querying
            if verbose:
                print("URL for querying:\n\n{}\n".format(startingURL))

            # tab this if this doesn't work
            response = requests.get(startingURL)
            json = response.json()
            facets_array=[]
            # try to make it generalised
            # add a check to see if a single value is there for filters; otherwise, can do this?
            for i in range(1,len(group_by)):
                temp_array=[]
                # how to ensure we catch the 
                for entry in json['facetResults'][i]['fieldResult']:
                    temp_array.append(entry['fq'])
                facets_array.append(temp_array)

            # get all counts for each value
            dict_values = {entry: [] for entry in [*group_by,'count']}
            for f in facets_array:
                for facet in f:
                    name,value = facet.split(':')
                    value = value.replace('"', '')
                    if name in group_by:
                        tempURL = URL + "%20AND%20%28{}%3A%22{}%22%29".format(name,value)
                    else:
                        continue
                    for group in group_by:
                        if (group != name) and ("facets={}".format(group) not in URL):
                            tempURL += "&facets={}".format(group)
                    tempURL += "&flimit=10000&pageSize=0"

                    # check to see if the user wants the URL for querying
                    if verbose:
                        print("URL for querying:\n\n{}\n".format(tempURL))

                    # get data
                    response=requests.get(tempURL)
                    json = response.json()

                    # put data in table
                    for entry in json['facetResults'][0]['fieldResult']:
                        # generalise this for more than one thing
                        if entry['fq'].split(":")[0] == group_by[0]:
                            name2,value2 = entry['fq'].split(":")
                            value2 = value2.replace('"', '')
                            if value2.isdigit():
                                value2 = int(value2)
                            dict_values[name2].append(value2)
                            dict_values['count'].append(int(entry['count']))
                            dict_values[name].append(value)
                            for key in dict_values:
                                if (key != name2) and (key != name) and (key != 'count'):
                                    dict_values[key].append("-")

            # format table
            return pd.DataFrame(dict_values) #, columns=[*group_by,'count'])

        # else, expand is False
        else:

            # add facets to make sure you get results
            for g in group_by:

                URL += "&facets={}".format(g)

            # round out the URL
            URL += "&flimit=10000&pageSize=0"

            # check to see if the user wants the URL for querying
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))

            # tab this if this doesn't work
            response = requests.get(URL)
            json = response.json()

            # get all counts for each value
            dict_values = {entry: [] for entry in [*group_by,'count']}
            for i in range(len(json['facetResults'])):
                for item in json['facetResults'][i]['fieldResult']:
                    for g in group_by:
                        if g in item['fq'] and item['fq'].split(':')[0] == g:
                            name,value=item['fq'].split(':')
                            value=value.replace('"','')
                            if value.isdigit():
                                value = int(value)
                            dict_values[name].append(value)
                            dict_values['count'].append(int(item['count']))
                            for entry in dict_values:
                                if (entry != name) and (entry != 'count'):
                                    dict_values[entry].append("-")

            counts = pd.DataFrame(dict_values) #, columns=[*group_by,'count'])

            # return dataFrame with all counts values
            return counts

    # need to make sure that the filter is a string or a lsid
    else:
        raise TypeError("Your filters need to either be a string (for one filter), or a list of strings.")