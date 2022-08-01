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
                sys.exit()
            parts=f.split(specialChar[0])
            if specialChar[0] == '=':
                if parts[1].isdigit():
                    returnString+="fq={}:[{}]".format(parts[0],parts[1])
                else:
                    returnString += "fq={}:({})".format(parts[0], parts[1])
            elif specialChar[0] == '>':
                returnString+="fq={}:[{}%20TO%20*]%20AND%20-({}:\"{}\")".format(parts[0], parts[1], parts[0], parts[1])
            elif specialChar[0] == '<':
                returnString+="fq={}:[*%20TO%20{}]%20AND%20-({}:\"{}\")".format(parts[0], parts[1], parts[0], parts[1])
            elif specialChar[0] == '=>' or specialChar[0] == '>=':
                returnString+="fq={}:[{}%20TO%20*]".format(parts[0], parts[1])
            elif specialChar[0] == '<=' or specialChar[0] == '=<':
                returnString+="fq={}:[*%20TO%20{}]".format(parts[0], parts[1])
            elif specialChar[0] == '!=':
                returnString+="-({}:\"{}\")".format(parts[0], parts[1])
    else:
        raise TypeError("Your filters need to either be a string (for one filter), or a list of strings.")
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
        if type(filters) == str or type(filters) == list:
            if type(filters) == str:
                filters = [filters]
        for f in filters:
            URL += "&" + filter(f)

    # check for groups
    if groups == None:
        raise ValueError("Please specify how to group your results.  Examples are: \'year\', \'basisOfRecord\'")
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
                if i != 0:
                    # get all possible values for this group
                    values=search.showAllValues(g)
                    # iterate over these values, and get a count for every single one and add it to dictValues list
                    for k,v in values.iterrows():
                        tempURL = URL + "&fq=({}:\"{}\")".format(v['field'],v['category']) + "&pageSize=0"
                        response=requests.get(tempURL)
                        json=response.json()
                        for entry in json['facetResults']:
                            for e in entry['fieldResult']:
                                tempdict={}
                                for gg in groups:
                                    tempdict[gg]=e['label']
                                    tempdict[g]=v['category']
                                    tempdict['count']=e['count']
                                dictValues.append(tempdict)
                else:
                    URL += "&facets={}".format(g)
            # return a sorted dataFrame with all counts values
            return pd.DataFrame.from_dict(dictValues).sort_values(by=groups).reset_index(drop=True)
        else:
            # loop over all of the groups
            for i, g in enumerate(groups):
                URL += "&facets={}".format(g) + "&pageSize=0"
                response = requests.get(URL)
                json = response.json()
                values = []
                # get all counts
                for i in range(len(json['facetResults'])):
                    for item in json['facetResults'][i]['fieldResult']:
                        dictValues = {}
                        for g in groups:
                            if g in item['fq']:
                                dictValues[g] = item['label']
                            else:
                                dictValues[g] = "-"
                        dictValues['count'] = item['count']
                        values.append(dictValues)
                # return dataFrame with all counts values
                return pd.DataFrame.from_dict(values)
    else:
        raise TypeError("Your filters need to either be a string (for one filter), or a list of strings.")

'''
def geolocate():
    # pseudocode here

def downTo():
    # pseudocode here
'''
