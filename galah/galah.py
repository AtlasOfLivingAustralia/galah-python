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
# write this to parse filters
'''
def filter(filters, profile=None):
    # pseudocode here
    specialChars = re.compile('[@_!#$%^&*()<>?/\|}{~:=]')
    returnstring=""
    if type(filters) == str or type(filters) == list:
        if type(filters) == str:
            filters=[filters]
        for f in filters:
            # need to check for other signs
            specialChar = specialChars.search(f)
            if specialChar[0] is None:
                print("Filter is not correct")
                sys.exit()
            parts=f.split(specialChar[0])
            if specialChar[0] == '=':
                if parts[1].isdigit():
                    returnstring+="fq={}:[{}]".format(parts[0],parts[1])
                else:
                    returnstring += "fq={}:({})".format(parts[0], parts[1])
            elif specialChar[0] == '>':
                returnstring+="fq={}:[{}%20TO%20*]%20AND%20-({}:\"{}\")".format(parts[0], parts[1], parts[0], parts[1])
            elif specialChar[0] == '<':
                returnstring+="fq={}:[*%20TO%20{}]%20AND%20-({}:\"{}\")".format(parts[0], parts[1], parts[0], parts[1])
            elif specialChar[0] == '=>' or specialChar[0] == '>=':
                returnstring+="fq={}:[{}%20TO%20*]".format(parts[0], parts[1])
            elif specialChar[0] == '<=' or specialChar[0] == '=<':
                returnstring+="fq={}:[*%20TO%20{}]".format(parts[0], parts[1])
            elif specialChar[0] == '!=':
                returnstring+="-({}:\"{}\")".format(parts[0], parts[1])
    else:
        print("newp")
        sys.exit()
    return returnstring

'''
add comments here
'''
def groupBy(URL,groups=None,filters=None,expand=False):
    #          year:[2018 TO *] is a translation of year > 2018
    # URL we are after: https://biocache-ws.ala.org.au/ws/occurrences/search?fq=year:[2018%20TO%20*]&facets=year&&pageSize=0
    # special characters
    # first, put filters in
    if filters is not None:
        if type(filters) == str or type(filters) == list:
            if type(filters) == str:
                filters = [filters]
        for f in filters:
            URL += "&" + filter(f)
    else:
        print("write another loop")
        sys.exit()

    # check for groups
    if groups == None:
        pass
    elif type(groups) is str or type(groups) is list:
        if type(groups) is str:
            groups=[groups]
        if expand:
            dict_values=[]
            for i,g in enumerate(groups):
                # for each value in
                # first, show all values to find all values of basisOfRecord
                # then, loop over all values of basisOfRecord (will be separate URL for each value)
                if i != 0:
                    values=search.showAllValues(g)
                    # iterate over pandas table
                    for k,v in values.iterrows():
                        #print(v['field'])
                        #print(v['category'])
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
                                dict_values.append(tempdict)
                else:
                    URL += "&facets={}".format(g)
            return pd.DataFrame.from_dict(dict_values).sort_values(by=groups).reset_index(drop=True)
        else:
            for i, g in enumerate(groups):
                URL += "&facets={}".format(g) + "&pageSize=0"
                response = requests.get(URL)
                # get the json
                json = response.json()
                values = []
                if not expand:
                    for i in range(len(json['facetResults'])):
                        for item in json['facetResults'][i]['fieldResult']:
                            dict_values = {}
                            for g in groups:
                                if g in item['fq']:
                                    dict_values[g] = item['label']
                                else:
                                    dict_values[g] = "-"
                            dict_values['count'] = item['count']
                            values.append(dict_values)
                    return pd.DataFrame.from_dict(values)
    else:
        print("Newp")
        sys.exit()


'''
def geolocate():
    # pseudocode here

def downTo():
    # pseudocode here
'''
