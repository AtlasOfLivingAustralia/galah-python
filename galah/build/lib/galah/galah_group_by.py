import requests
import pandas as pd
import urllib
import copy
import itertools
from .get_api_url import readConfig
from .common_functions import add_filters
from .common_functions import get_api_url,put_entries_in_grouped_dict,add_to_payload_ALA
from .version import __version__

def galah_group_by(URL=None,
                   method=None,
                   group_by=None,
                   total_group_by=False,
                   filters=None,
                   expand=True,
                   payload={},
                   verbose=False
                   ):
    """
    Used for grouping counts by a specific query, i.e. "year" or "basisOfRecord".  It's mainly utilized in atlas_counts.
    """

    if type(group_by) is not str and len(group_by) > 3:
        raise ValueError("Only 3 groups are allowed, as otherwise the queries will get complicated")

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas']

    # get headers
    headers = {"User-Agent": "galah-python {}".format(__version__)}
    
    # check to see if the expand option is true
    if expand:

        # check to see if you can expand upon this
        if (type(group_by) == str) or (type(group_by) == list and len(group_by) == 1):
            raise ValueError("You can only use the expand=False option with one group")

    # check if expand option works
    if expand:
        ifGroupBy = True
    else:
        ifGroupBy = False

    # first, check for filters
    if filters is not None:

        # check type of filter
        if type(filters) == str or type(filters) == list:

            if atlas not in ["Australia","ALA"]:

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

        # create a base URL
        startingURL = URL

        if atlas in ["Australia","ALA"]:
            # try startingURL2
            #startingURL2,method = get_api_url(column1='called_by',column1value='atlas_counts',column2="api_name",
            #                            column2value="records_counts")

            # get response from your query, which will include all available fields
            qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")
            qid = requests.request(method2,qid_URL,data=payload,headers=headers)
            facets = "".join("&facets={}".format(g) for g in group_by)
            if startingURL[-1] == "&":
                URL = startingURL + "fq=%28qid%3A" + qid.text + "%29" + facets + "&flimit=-1&pageSize=0"
            else:
                URL = startingURL + "?fq=%28qid%3A" + qid.text + "%29" + facets + "&flimit=-1&pageSize=0"

            # check to see if the user wants the URL for querying
            if verbose:
                print()
                print("headers: {}".format(headers))
                print()
                print("payload for queryID: {}".format(payload))
                print("queryID URL: {}".format(qid_URL))
                print("method: {}".format(method2))
                print()
                print("qid for query: {}".format(qid.text))
                print("URL for result:{}".format(URL))
                print("method: {}".format(method))
                print()

            response = requests.request(method,URL,headers=headers)
            response_json = response.json()
            facets_array=[]
        
        else:

            # loop over group_by
            for g in group_by:

                # ensure each group is given its own facet
                if atlas in ["Global","GBIF"]:
                    startingURL += "&facet={}".format(g)
                else:
                    startingURL += "&facets={}".format(g)

            # round out the URL
            startingURL += "&flimit=-1&pageSize=0"
            
            # check to see if the user wants the URL for querying
            if verbose:
                print()
                print("headers: {}".format(headers))
                print()
                print("URL for querying: {}".format(startingURL))
                print("Method: {}".format(method))
                print()

            # get response from your query, which will include all available fields
            response = requests.request(method,startingURL,headers=headers)
            response_json = response.json()
            facets_array=[]

        # set some common variables
        if atlas in ["Global","GBIF"]:
            group_by = sorted(group_by)
            length = len(response_json['facets'])
            results_array = response_json['facets']
            field_name = 'counts'
            if expand:
                response_json['facets'] = sorted(response_json['facets'],key = lambda d: d['field'])
                results_array = response_json['facets']
                facet_name = 'name'
        elif atlas in ["Brazil"]:
            length = len(response_json)
            results_array = response_json 
            field_name = 'fieldResult' 
            facet_name = 'fq'
        # elif atlas in ["Guatemala"]:
        #     print(len(response_json))
        #     print(response_json)
        #     import sys
        #     sys.exit()
        else:
            length = len(response_json['facetResults'])
            results_array = response_json['facetResults']
            field_name = 'fieldResult'
            if expand:
                facet_name = 'fq'

        # get all counts for each value
        dict_values = {entry: [] for entry in [*group_by,'count']}

        # do this if the expand option is try
        if expand:

            # was 1,len(group_by)
            ### TRY THIS
            if atlas not in ["Global","GBIF"]:
                start = 0
                end = len(group_by) - 1
            else:
                start = 1
                end = len(group_by)
            
            # now do loop
            for i in range(start,end):
                temp_array=[]
                for entry in results_array[i][field_name]:
                    temp_array.append(entry[facet_name])
                facets_array.append(temp_array)

            combined_facets_array = list(itertools.product(*facets_array))

            # loop over facets array
            # was combined_facets_array
            for f in combined_facets_array:

                # check for GBIF atlas
                if atlas in ["Global","GBIF"]:

                    inc = 0

                    for facet in f:

                        # was i+1
                        tempURL = URL + "&{}={}".format(group_by[start+inc],urllib.parse.quote(facet)) + "&facet=" + group_by[start-1+inc] + "&flimit=-1&pageSize=0"
                    
                        # check if user is grouping by scientific name
                        # i + 1
                        if group_by[start+inc] == "scientificName":
                            tempURL = URL + "&{}={}".format(group_by[start+inc],"%20".join(facet.split(" ")[0:2])) + "&facet=" + group_by[start-1+inc] + "&flimit=-1&pageSize=0"
                        else:
                            tempURL = URL + "&{}={}".format(group_by[start+inc],"%20".join(facet.split(" "))) + "&facet=" + group_by[start-1+inc] + "&flimit=-1&pageSize=0"
        
                        inc += 1

                    if verbose:
                        print()
                        print("URL for querying: {}".format(tempURL))
                        print("Method: {}".format(method))
                        print()

                    # get the data
                    response=requests.request(method,tempURL,headers=headers)
                    response_json = response.json()
                    
                    # put data in dict
                    #### TODO: check if this is correct
                    for entry in response_json['facets'][0]['counts']:
                        dict_values[group_by[start-1]].append(entry['name'])
                        dict_values['count'].append(int(entry['count']))
                        dict_values[group_by[start]].append(facet)
                        for key in dict_values:
                            if (key != group_by[start]) and (key != group_by[start-1]) and (key != 'count'):
                                dict_values[key].append("-")
                
                # do this loop for all other atlases 
                else:

                    # loop over each facet
                    #for facet in f:
                    if atlas in ["Australia","ALA"]:
                    
                        # check for fq in payload
                        if "fq" not in payload:
                            payload["fq"] = [f]
                        else:
                            payload["fq"].append(f)
                            
                        payload_for_querying = copy.deepcopy(payload)
                        
                        # create payload and get qid
                        qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")
                        qid = requests.request(method2,qid_URL,data=payload,headers=headers)
                        if startingURL[-1] == "&":
                            tempURL = startingURL + "fq=%28qid%3A" + qid.text + "%29" 
                        else:
                            tempURL = startingURL + "?fq=%28qid%3A" + qid.text + "%29"
                        if any("lsid" in fq for fq in payload['fq']):
                            index = [idx for idx, s in enumerate(payload['fq']) if 'lsid' in s][0]
                            payload["fq"] = [payload["fq"][index]]
                        else:
                            payload["fq"] = []
                        if filters is not None:
                            payload = add_to_payload_ALA(payload=payload,
                                                         atlas=atlas,
                                                         filters=filters)
                        tempURL += "&facets={}".format(group_by[-1])
                        
                    else:

                        for facet in f:
                        
                            # split each facet to make it human readable
                            name,value = facet.split(':')
                            value = value.replace('"', '')
                            if name in group_by:
                                tempURL = URL + "%20AND%20%28{}%3A%22{}%22%29".format(name,value)
                            else:
                                tempURL = URL
                                # continue
                            for group in group_by:
                                if (group != name) and ("facets={}".format(group) not in URL):
                                    tempURL += "&facets={}".format(group)

                    # finalise the URL for querying
                    tempURL += "&flimit=-1&pageSize=0"

                    # check to see if the user wants the URL for querying
                    if verbose:
                        if atlas in ["Australia","ALA"]:
                            print()
                            print("payload for queryID: {}".format(payload_for_querying))
                            print("queryID URL: {}".format(qid_URL))
                            print("method: {}".format(method2))
                            print()
                            print("qid for query: {}".format(qid.text))
                            print("URL for result:{}".format(tempURL))
                            print("method: {}".format(method))
                            print()
                        else:
                            print()
                            print("URL for querying: {}".format(tempURL))
                            print("Method: {}".format(method))
                            print()

                    # get data
                    response=requests.request(method,tempURL,headers=headers)
                    response_json = response.json()

                    # if there is no data available, move onto next variable
                    if atlas not in ["Brazil"]:
                        if response_json is None or not response_json['facetResults']:
                            continue
                    else:
                        if response_json is None or not response_json[0]['fieldResult']:
                            continue

                    # put data in table (and check if user wants Brazil, because that is an exception)
                    if atlas in ["Brazil"]:
                        if len(group_by) <= 2:
                            results_array = response_json[0]['fieldResult']
                        else:
                            results_array = response_json[1]['fieldResult']
                    else:
                        results_array = response_json['facetResults'][0]['fieldResult']

                    # loop over each entry in the results
                    for entry in results_array:

                        if entry['fq'].split(":")[0] in group_by:

                            # add facet value to dictionary for expand
                            for facet in f:

                                if len(facet.split(':')) > 2:
                                    name_and_values = facet.split(':')
                                    name = name_and_values[0]
                                    value = ":".join(name_and_values[1:])
                                else:
                                    name,value=facet.split(':')
                                value = value.replace('"','')
                                # trying this - potentially remove it
                                if name in group_by and name not in entry['fq'].split(':'):
                                    dict_values[name].append(value)

                        # potentially tab again
                        dict_values = put_entries_in_grouped_dict(entry=entry,dict_values=dict_values,expand=expand)

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
            
            # loop over the array length
            for i in range(length):

                # check if atlas is GBIF
                if atlas in ["Global","GBIF"]:

                    # loop over each group and make sure entry is human readable and have a dash if 
                    # it doesn't have a count
                    for g in group_by:
                        if "_" in results_array[i]['field']:
                            test_name = results_array[i]['field'].split("_")
                            for k in range(len(test_name)):
                                test_name[k] = test_name[k].lower()
                                if k > 0:
                                    test_name[k] = test_name[k].capitalize()
                            test_name = "".join(test_name)
                        else:
                            test_name = results_array[i]['field'].lower()
                        if test_name == g:
                            for item in results_array[i][field_name]:
                                dict_values[g].append(item['name'])
                                dict_values['count'].append(int(item['count']))
                                for entry in dict_values:
                                    if (entry != g) and (entry != 'count'):
                                        dict_values[entry].append("-")
                
                # otherwise, it's all other atlases
                else:

                    # loop over entry in results
                    for entry in results_array[i][field_name]:

                        # loop over each group and make sure entry is human readable and have a dash if 
                        # it doesn't have a count
                        for g in group_by:

                            # check for only itesm you want
                            if g in entry['fq'] and entry['fq'].split(':')[0] == g:

                                # add values to dictionary
                                dict_values = put_entries_in_grouped_dict(entry=entry,dict_values=dict_values,expand=expand)

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