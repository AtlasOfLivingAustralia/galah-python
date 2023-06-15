import requests
import pandas as pd
from .get_api_url import readConfig
from .common_functions import add_filters

def galah_group_by(URL,
                   group_by=None,
                   total_group_by=False,
                   filters=None,
                   expand=True,
                   verbose=False
                   ):
    """
    Used for grouping counts by a specific query, i.e. "year" or "basisOfRecord".  It's mainly utilized in atlas_counts.
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas']

    # check if expand option works
    if expand:
        ifGroupBy = True
    else:
        ifGroupBy = False

    # first, check for filters
    if filters is not None:

        # check type of filter
        if type(filters) == str or type(filters) == list:

            URL = add_filters(URL=URL,atlas=atlas,filters=filters,ifGroupBy=ifGroupBy)

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

                if atlas in ["Global","GBIF"]:
                    startingURL += "&facet={}".format(g)
                else:
                    startingURL += "&facets={}".format(g)

            # round out the URL
            startingURL += "&flimit=10000&pageSize=0"

            # check to see if the user wants the URL for querying
            if verbose:
                print("URL for querying:\n\n{}\n".format(startingURL))

            # get thing
            response = requests.get(startingURL)
            response_json = response.json()
            facets_array=[]

            # try this
            if atlas in ["Global","GBIF"]:
                group_by = sorted(group_by)
                response_json['facets'] = sorted(response_json['facets'],key = lambda d: d['field'])
                length = len(response_json['facets'])
                results_array = response_json['facets']
                field_name = 'counts'
                facet_name = 'name'
            elif atlas in ["Brazil"]:
                length = len(response_json)
                results_array = response_json 
                field_name = 'fieldResult' 
                facet_name = 'fq'
            else:
                length = len(response_json['facetResults'])
                results_array = response_json['facetResults']
                field_name = 'fieldResult' #i18nCode
                facet_name = 'fq'

            # add a check to see if a single value is there for filters; otherwise, can do this?
            for i in range(1,len(group_by)):
                temp_array=[]
                for entry in results_array[i][field_name]:
                    temp_array.append(entry[facet_name])
                facets_array.append(temp_array)

            # get all counts for each value
            dict_values = {entry: [] for entry in [*group_by,'count']}
            for i,f in enumerate(facets_array):
                if atlas in ["Global","GBIF"]:
                    for facet in f:

                        if group_by[i+1] == "scientificName":
                            tempURL = URL + "&{}={}".format(group_by[i+1],"%20".join(facet.split(" ")[0:2])) + "&facet=" + group_by[i] + "&pageSize=0"
                        else:
                            tempURL = URL + "&{}={}".format(group_by[i+1],"%20".join(facet.split(" "))) + "&facet=" + group_by[i] + "&pageSize=0"

                        # print the URL
                        if verbose:
                            print("URL for querying:\n\n{}\n".format(tempURL))

                        # get the data
                        response=requests.get(tempURL)
                        response_json = response.json()

                        # put data in dict
                        for entry in response_json['facets'][0]['counts']:
                            dict_values[group_by[i]].append(entry['name'])
                            dict_values['count'].append(int(entry['count']))
                            dict_values[group_by[i+1]].append(facet)
                            for key in dict_values:
                                if (key != group_by[i+1]) and (key != group_by[i]) and (key != 'count'):
                                    dict_values[key].append("-")
                else:
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
                        response_json = response.json()

                        if response_json is None:
                            continue

                        # put data in table
                        if atlas in ["Brazil"]:
                            results_array = response_json[0]['fieldResult']
                        else:
                            results_array = response_json['facetResults'][0]['fieldResult']

                        for entry in results_array:
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
            counts = pd.DataFrame(dict_values).reset_index(drop=True)
            counts.sort_values(by=group_by)

            # if user wants total, return total number of rows
            if total_group_by:
                return pd.DataFrame({'count': [counts.shape[0]]})

            # return dataFrame with all counts values
            return counts

        # else, expand is False
        else:

            # add facets to make sure you get results
            for g in group_by:

                if atlas in ["Global","GBIF"]:
                    URL += "&facet={}".format(g)
                else:
                    URL += "&facets={}".format(g)

            # round out the URL
            URL += "&flimit=10000&pageSize=0"

            # check to see if the user wants the URL for querying
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))

            # tab this if this doesn't work
            response = requests.get(URL)
            response_json = response.json()

            # get name of results
            if atlas in ["Global","GBIF"]:
                length = len(response_json['facets'])
                name_results = response_json['facets']
                field_name = 'counts'
            elif atlas in ["Brazil"]:
                length = len(response_json)
                name_results = response_json 
                field_name = 'fieldResult' 
                facet_name = 'fq'
            else:
                length = len(response_json['facetResults'])
                name_results = response_json['facetResults']
                field_name = 'fieldResult'

            # get all counts for each value
            dict_values = {entry: [] for entry in [*group_by,'count']}
            for i in range(length):
                if atlas in ["Global","GBIF"]:
                    for g in group_by:
                        if "_" in name_results[i]['field']:
                            test_name = name_results[i]['field'].split("_")
                            for k in range(len(test_name)):
                                test_name[k] = test_name[k].lower()
                                if k > 0:
                                    test_name[k] = test_name[k].capitalize()
                            test_name = "".join(test_name)
                        else:
                            test_name = name_results[i]['field'].lower()
                        if test_name == g:
                            for item in name_results[i][field_name]:
                                dict_values[g].append(item['name'])
                                dict_values['count'].append(int(item['count']))
                                for entry in dict_values:
                                    if (entry != g) and (entry != 'count'):
                                        dict_values[entry].append("-")
                else:
                    for item in name_results[i][field_name]:
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

            # get all counts into a dictionary and sort them
            counts = pd.DataFrame(dict_values).reset_index(drop=True)
            counts.sort_values(by=group_by)

            # if user wants total, return total number of rows
            if total_group_by:
                return pd.DataFrame({'count': [counts.shape[0]]})

            # return dataFrame with all counts values
            return counts

    # need to make sure that the filter is a string or a lsid
    else:
        raise TypeError("Your filters need to either be a string (for one filter), or a list of strings.")