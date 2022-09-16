import requests,re
import pandas as pd
from .galah_filter import galah_filter
from .show_all_values import show_all_values

'''
groupBy
-------
groups the

arguments
---------
URL: the starting URL to add filters and groups to; will ultimately query the API for counts
groups: what to group the data by (i.e. year, basisOfRecord)
filters: a string or a list of strings with filters (i.e. "year>2018" or ["year>2018", "basisOfRecord=HUMAN_OBSERVATION"])
expand: False=default, whether or not to include all possible combinations of the groups in your query

returns
-------
dataFrame: a pandas dataframe containing the counts of species, including filters and organised by groups (i.e. year,
           basisOfRecord, etc.)

TODO
----
1. Generalise this to N groups, where N>2
'''
def galah_group_by(URL,groups=None,filters=None,expand=False,verbose=False):

    # first, check for filters
    if filters is not None:

        # check type of filter
        if type(filters) == str or type(filters) == list:

            # change type of filters to list for easy looping
            if type(filters) == str:
                filters = [filters]

            # loop over filters
            for f in filters:
                URL += "&" + galah_filter(f,ifgroupBy=True)

        # else, raise a TypeError because this variable needs to be either a string or a list
        else:
            raise TypeError("Your filters need to either be a string (for one filter), or a list of strings.")

    # check for groups
    if groups is None:

        # raise error, as you want this specified for this function
        raise ValueError("Please specify how to group your results.  Examples are: \'year\', \'basisOfRecord\'")

    # check for variable type
    elif type(groups) is str or type(groups) is list:

        # change to list for easy looping
        if type(groups) is str:
            groups=[groups]

        # check to see if the expand option is true
        if expand:

            if len(groups) == 1:
                raise ValueError("You cannot use the expand=True option when you only have one group")

            # create empty list for pandas later
            dictValues=[]

            # loop over groups
            for i,g in enumerate(groups):

                # check to see if this is not the first variable in groups
                if i != 0:

                    # get all possible values for this group
                    values=show_all_values(g)

                    # iterate over these values, and get a count for every single one and add it to dictValues list
                    for k,v in values.iterrows():

                        # get a URL and query each possibility
                        tempURL = URL + "&fq=({}:\"{}\")".format(v['field'],v['category']) + "&pageSize=0"
                        response=requests.get(tempURL)
                        json=response.json()

                        # check to see if the user wants the URL for querying
                        if verbose:
                            print("URL for querying:\n\n{}\n".format(tempURL))

                        # loop over results and add a dictionary to the dictValues list
                        for entry in json['facetResults']:
                            for e in entry['fieldResult']:
                                tempDict={}
                                for gg in groups:
                                    tempDict[gg]=e['label']
                                    tempDict[g]=v['category']
                                    tempDict['count']=e['count']
                                dictValues.append(tempDict)

                # else, this is the first variable and needs to be treated differently
                else:
                    URL += "&facets={}".format(g)

            # return a sorted dataFrame with all counts values
            return pd.DataFrame.from_dict(dictValues).sort_values(by=groups).reset_index(drop=True)

        # else, expand is False
        else:

            # loop over all of the groups
            for i, g in enumerate(groups):

                # create the URL and get results
                URL += "&facets={}".format(g) + "&pageSize=0"
                response = requests.get(URL)
                json = response.json()

                # check to see if the user wants the URL for querying
                if verbose:
                    print("URL for querying:\n\n{}\n".format(URL))

                # create dummy values variable to be fed into Pandas later
                dictValues = []

                # get all counts for each value
                for i in range(len(json['facetResults'])):
                    for item in json['facetResults'][i]['fieldResult']:
                        tempDict = {}
                        for g in groups:
                            if g in item['fq']:
                                tempDict[g] = item['label']
                            else:
                                tempDict[g] = "-"
                        tempDict['count'] = item['count']
                        dictValues.append(tempDict)

                # return dataFrame with all counts values
                return pd.DataFrame.from_dict(dictValues)

    # need to make sure that the filter is a string or a lsit
    else:
        raise TypeError("Your filters need to either be a string (for one filter), or a list of strings.")