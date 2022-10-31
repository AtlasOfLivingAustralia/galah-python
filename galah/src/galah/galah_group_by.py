import requests,re
import pandas as pd
from .galah_filter import galah_filter
from .show_values import show_values

'''
group_by
-------
group_by the

arguments
---------
URL: the starting URL to add filters and group_by to; will ultimately query the API for counts
group_by: what to group the data by (i.e. year, basisOfRecord)
filters: a string or a list of strings with filters (i.e. "year>2018" or ["year>2018", "basisOfRecord=HUMAN_OBSERVATION"])
expand: False=default, whether or not to include all possible combinations of the group_by in your query

returns
-------
dataFrame: a pandas dataframe containing the counts of species, including filters and organised by group_by (i.e. year,
           basisOfRecord, etc.)

TODO
----
1. Generalise this to N group_by, where N>2
'''
def galah_group_by(URL,group_by=None,filters=None,expand=True,verbose=False):

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

            if len(group_by) == 1:
                raise ValueError("You cannot use the expand=True option when you only have one group")

            # create empty list for pandas later
            dictValues=[]

            # loop over group_by
            for i,g in enumerate(group_by):

                # check to see if this is not the first variable in group_by
                if i != 0:

                    # get all possible values for this group
                    values=show_values(field=g)

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
                                for gg in group_by:
                                    tempDict[gg]=e['label']
                                    tempDict[g]=v['category']
                                    tempDict['count']=e['count']
                                dictValues.append(tempDict)

                # else, this is the first variable and needs to be treated differently
                else:
                    URL += "&facets={}".format(g)

            # return a sorted dataFrame with all counts values
            return pd.DataFrame.from_dict(dictValues).sort_values(by=group_by).reset_index(drop=True)

        # else, expand is False
        else:

            # loop over all of the group_by
            for i, g in enumerate(group_by):

                # create the URL and get results
                URL += "&facets={}".format(g)

            URL += "&pageSize=0"

            # tab this if this doesn't work
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
                    for g in group_by:
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