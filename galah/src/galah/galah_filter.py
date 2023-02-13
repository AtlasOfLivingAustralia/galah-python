import re

def galah_filter(f, ifgroupBy=False):
    """
    This takes

    To know how many total records are in your chosen atlas, type

    .. prompt:: python

        import galah
        galah.galah_filter(filters="year=2020")

    which returns

    .. program-output:: python3 -c "import galah; print(galah.galah_filter(filters=\\\"year=2020\\\"))"
    """

    ## TODO: check for year - might not be working with expand group_by

    # first, check for special characters
    specialChars = re.compile('[@!#$%^&*()<>?}{~:=]') #/\|
    returnString=""

    # check to make sure the filter type is correct
    if type(f) == str:

        # need to check for special characters
        specialChar = specialChars.findall(f)
        if specialChar is None:
            raise ValueError("Either your filters does not have the correct special characters [@_!#$%^&*()<>?}{~:=], "
                            "or we need to include another special character we have forgotten about.")
        else:
            specialChar = "".join(specialChar)

        # split filter into parts
        parts = f.split(specialChar)

        # remove leading and trailing white spaces from each filter part
        for i, p in enumerate(parts):
            parts[i] = p.strip()

        # start checking for different logical operators, starting with equals
        if specialChar == '=' or specialChar == '==':

            # check if the filter is a number or a string and if there is a group by
            if parts[1].isdigit() and ifgroupBy:
                # this one is square brackets
                #returnString += "%5B{}:%22{}%22%5d".format(parts[0], parts[1])
                returnString += "%28{}%3A%22{}%22%29".format(parts[0], parts[1].replace(" ", "%20"))
            # if filter is querying a field that has no value
            elif parts[1] == '':
                returnString += "%28{}%3A%28*%29%29".format(parts[0])
            else:
                # added quotes
                returnString += "%28{}%3A%22{}%22%29".format(parts[0], parts[1].replace(" ", "%20"))

        elif specialChar == '>':
            returnString+="%28{}:%5B{}%20TO%20*%5d%20AND%20-%28{}%3A%22{}%22%29%29".format(parts[0], parts[1], parts[0], parts[1])

        # less than
        elif specialChar == '<':
            returnString += "%28{}%3A%5B*%20TO%20{}%5d%20AND%20-%28{}%3A\"{}\"%29%29".format(parts[0], parts[1], parts[0], parts[1])

        # greater than or equal to
        elif specialChar == '=>' or specialChar == '>=':
            returnString += "%28{}%3A%5B{}%20TO%20%2A%5d%29".format(parts[0], parts[1])

        # less than or equal to
        elif specialChar == '<=' or specialChar == '=<':
            returnString += "%28{}%3A%5B*%20TO%20{}%5d%29".format(parts[0], parts[1])

        # not equal to
        elif specialChar == '!=' or specialChar == '=!':
            returnString += "-%28{}%3A%22{}%22%29".format(parts[0], parts[1])

        # filters with numerical operators are being used with a non-numeric type
        elif not isinstance(parts[1], int):
            raise ValueError("Numeric types can only be used with filters that include the <, >, <=, or => operators.")

        # else, there is either an error in the filters or a missing case
        else:
            raise ValueError("The special character {} is not included in the filters function.  Either it is not a logical operator, or it has not been included yet.".format(specialChar[0]))

    # let the user know that their variable is not of the correct type
    else:
        raise TypeError("Your filters need to either be a string (for one filters), or a list of strings.")

    # return a string to be added to the URL
    return returnString