'''
This is a collection of the filtering functions available on galah
'''

import requests,re,sys
import pandas as pd
import galah.search as search

'''
Function comments here

arguments: one or more scientific names (search=True) or taxonomic identifiers
               (search=False)
def identify([arguments here], search=True):
    #if search=True, look for scientific names
    #if search=False, look for taxonomic names

arguments: filter in the form "field logical value"

def select():
    # pseudocode here
'''

'''
filter
------
takes a filter that the user wants to filter their data with, and converts it into URL-compatible language to query the API

arguments
---------
filters: a string or a list of strings with filters (i.e. "year>2018" or ["year>2018", "basisOfRecord=HUMAN_OBSERVATION"])
profile: fill in later

returns
------- 
returnString: a string to add to the URL to query the API

TODO
----
1. Test more filters
'''
def filter(filters, profile=None):

    # first, check for special characters
    specialChars = re.compile('[@_!#$%^&*()<>?/\|}{~:=]')
    returnString=""

    # check to make sure the filter types are correct
    if type(filters) == str or type(filters) == list:

        # change to a list for ease of processing
        if type(filters) == str:
            filters=[filters]

        # loop over all filters
        for f in filters:

            # need to check for special characters
            specialChar = specialChars.search(f)
            if specialChar[0] is None:
                raise ValueError("Either your filter does not have the correct special characters [@_!#$%^&*()<>?/\|}{~:=], "
                                 "or we need to include another special character we have forgotten about.")

            # get the parts of the filter
            parts=f.split(specialChar[0])

            # start checking for different logical operators, starting with equals
            if specialChar[0] == '=':

                # check if the filter is a number or a string
                if parts[1].isdigit():
                    returnString+="fq={}:[{}]".format(parts[0],parts[1])
                else:
                    returnString += "fq={}:({})".format(parts[0], parts[1])

            # greater than
            elif specialChar[0] == '>':
                returnString+="fq={}:[{}%20TO%20*]%20AND%20-({}:\"{}\")".format(parts[0], parts[1], parts[0], parts[1])

            # less than
            elif specialChar[0] == '<':
                returnString+="fq={}:[*%20TO%20{}]%20AND%20-({}:\"{}\")".format(parts[0], parts[1], parts[0], parts[1])

            # greater than or equal to
            elif specialChar[0] == '=>' or specialChar[0] == '>=':
                returnString+="fq={}:[{}%20TO%20*]".format(parts[0], parts[1])

            # less than or equal to
            elif specialChar[0] == '<=' or specialChar[0] == '=<':
                returnString+="fq={}:[*%20TO%20{}]".format(parts[0], parts[1])

            # not equal to
            elif specialChar[0] == '!=':
                returnString+="-({}:\"{}\")".format(parts[0], parts[1])

            # else, there is either an error in the filter or a missing case
            else:
                raise ValueError("The special character {} is not included in the filters function.  Either it is not a logical operator, or it has not been included yet.".format(specialChar[0]))

    # let the user know that their variable is not of the correct type
    else:
        raise TypeError("Your filters need to either be a string (for one filter), or a list of strings.")

    # return a string to be added to the URL
    return returnString

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
def groupBy(URL,groups=None,filters=None,expand=False):

    # first, check for filters
    if filters is not None:

        # check type of filter
        if type(filters) == str or type(filters) == list:

            # change type of filters to list for easy looping
            if type(filters) == str:
                filters = [filters]

            # loop over filters
            for f in filters:
                URL += "&" + filter(f)

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

            # create empty list for pandas later
            dictValues=[]

            # loop over groups
            for i,g in enumerate(groups):

                # check to see if this is not the first variable in groups
                if i != 0:

                    # get all possible values for this group
                    values=search.showAllValues(g)

                    # iterate over these values, and get a count for every single one and add it to dictValues list
                    for k,v in values.iterrows():

                        # get a URL and query each possibility
                        tempURL = URL + "&fq=({}:\"{}\")".format(v['field'],v['category']) + "&pageSize=0"
                        response=requests.get(tempURL)
                        json=response.json()

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

'''
def geolocate():
    # pseudocode here

def downTo():
    # pseudocode here
'''
