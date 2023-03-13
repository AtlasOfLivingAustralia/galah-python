import re

ATLAS_KEYWORDS = {
    "Australia": "taxonConceptID",
    "Austria": "guid",
    "Brazil": "guid",
    "Canada": "usageKey",
    "Estonia": "guid",
    "France": "usageKey",
    "Guatemala": "guid",
    "Portugal": "usageKey",
    "Spain": "taxonConceptID",
    "Sweden": "guid",
    "United Kingdom": "guid",
}

def galah_filter(f, ifgroupBy=False):
    """
    "Filters" are arguments of the form field logical value that are used to narrow down the number of records returned by 
    a specific query. For example, it is common for users to request records from a particular year (``year=2020``), or 
    to return all records except for fossils (``basisOfRecord!=FossilSpecimen``).

    Filters are passed to ``atlas_occurrences()``, ``atlas_species()``, ``atlas_counts()`` or ``atlas_media()``.

    
    Examples
    --------

    To know how many total records are in your chosen atlas, type

    .. prompt:: python

        import galah
        galah.galah_filter(filters="year=2020")

    which returns

    .. program-output:: python -c "import galah; print(galah.galah_filter(filters=\\\"year=2020\\\"))"
    """

    # first, check for special characters
    char_string='[!=<>]'
    specialChars = re.compile(char_string) #["=","!",">","<"] #/\|:
    returnString=""

    # check to make sure the filter type is correct
    if type(f) is str:

        # need to check for special characters
        specialChar = specialChars.findall(f)
        if specialChar is None:
            raise ValueError("Either your filters does not have the correct special characters {}".format(char_string) 
                             + "or we need to include another special character we have forgotten about.")
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
            elif parts[1] == "True":
                returnString += "%28assertions%3A%22{}%22%29".format(parts[0])
            elif parts[1] == "False":
                returnString += "-%28assertions%3A%22{}%22%29".format(parts[0])
            else:
                # check if this is array
                arrayChars = re.compile('[\[\]]')
                arrayChar = arrayChars.findall(parts[1])
                if arrayChar:
                    returnString += "%28"
                    temp_array = parts[1][1:-1].split(",")
                    for value in temp_array:
                        returnString += "{}%3A22{}%22%20OR%20".format(parts[0], value.replace(" ","%20").replace('\'','').replace('"',''))
                    returnString = returnString[:-8] + "%29"
                # added quotes
                else:
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
        
        # else, there is either an error in the filters or a missing case
        else:
            raise ValueError("The special character {} is not included in the filters function.  Either it is not a logical operator, or it has not been included yet.".format(specialChar[0]))

    # let the user know that their variable is not of the correct type
    else:
        raise TypeError("Your filters need to either be a string (for one filters), or a list of strings.")

    # return a string to be added to the URL
    return returnString