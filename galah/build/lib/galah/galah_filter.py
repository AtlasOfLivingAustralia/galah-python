import requests,re
import pandas as pd

import sys

def galah_filter(filters, ifgroupBy=False):
    """
    This takes

    To know how many total records are in your chosen atlas, type

    .. prompt:: python

        import galah
        galah.galah.galah_filter(filters="year=2020")

    which returns

    .. program-output:: python3 -c "import galah; print(galah.galah_filter(filters=\\\"year=2020\\\"))"
    """

    # first, check for special characters
    specialChars = re.compile('[@!#$%^&*()<>?}{~:=]') #/\|
    returnString=""

    # check to make sure the filters types are correct
    if type(filters) == str or type(filters) == list:

        # change to a list for ease of processing
        if type(filters) == str:
            filters=[filters]

        # TODO: check if there are multiple of the same type of filters what to do?
        #categories=[]
        '''
        for f in filters:
            specialChar = specialChars.search(f)
            if specialChar[0] is None:
                raise ValueError("Either your filters does not have the correct special characters [@_!#$%^&*()<>?}{~:=], "
                                 "or we need to include another special character we have forgotten about.")
            if f.split(specialChar[0])[0] not in categories:
                categories.append(f.split(specialChar[0])[0])
            else:
                # remove duplicates
                print("duplicates")
                print(filters)
                sys.exit()
        #print(categories)
        #sys.exit()
        '''

        # loop over all filters
        for i,f in enumerate(filters):

            # need to check for special characters
            specialChar = specialChars.findall(f)
            if specialChar is None:
                raise ValueError("Either your filters does not have the correct special characters [@_!#$%^&*()<>?}{~:=], "
                                 "or we need to include another special character we have forgotten about.")
            else:
                specialChar = "".join(specialChar)

            # check for spaces
            f = f.replace(" ","")

            # split filters into parts
            parts = f.split(specialChar)

            # start checking for different logical operators, starting with equals
            if specialChar == '=' or specialChar == '==':

                # check if the filters is a number or a string
                if parts[1].isdigit():
                    if ifgroupBy:
                        returnString+="&fq={}:[{}]".format(parts[0],parts[1])
                    else:
                        returnString += "&fq={}:({})".format(parts[0], parts[1])
                else:
                    returnString += "&fq={}:({})".format(parts[0], parts[1])

            # greater than
            elif specialChar == '>':
                returnString+="&fq={}:[{}%20TO%20*]%20AND%20-({}:\"{}\")".format(parts[0], parts[1], parts[0], parts[1])

            # less than
            elif specialChar == '<':
                returnString+="&fq={}:[*%20TO%20{}]%20AND%20-({}:\"{}\")".format(parts[0], parts[1], parts[0], parts[1])

            # greater than or equal to
            elif specialChar == '=>' or specialChar == '>=':
                returnString+="&fq={}:[{}%20TO%20*]".format(parts[0], parts[1])
            # less than or equal to
            elif specialChar == '<=' or specialChar == '=<':
                returnString+="&fq={}:[*%20TO%20{}]".format(parts[0], parts[1])

            # not equal to
            elif specialChar == '!=' or specialChar == '=!':
                returnString+="&fq=(-{}:\"{}\")".format(parts[0], parts[1])

            # else, there is either an error in the filters or a missing case
            else:
                raise ValueError("The special character {} is not included in the filters function.  Either it is not a logical operator, or it has not been included yet.".format(specialChar[0]))

    # let the user know that their variable is not of the correct type
    else:
        raise TypeError("Your filters need to either be a string (for one filters), or a list of strings.")

    # return a string to be added to the URL
    return returnString