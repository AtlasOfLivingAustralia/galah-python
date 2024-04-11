import re,urllib
from .get_api_url import readConfig
from .common_dictionaries import GBIF_PREDICATE_DEFINITIONS

def galah_filter(f, 
                 ifgroupBy=False,
                 occurrencesGBIF=False):
    """
    "Filters" are arguments of the form field logical value that are used to narrow down the number of records returned by 
    a specific query. For example, it is common for users to request records from a particular year (``year=2020``), or 
    to return all records except for fossils (``basisOfRecord!=FossilSpecimen``).

    Filters are passed to ``atlas_occurrences()``, ``atlas_species()``, ``atlas_counts()`` or ``atlas_media()``.
    """

    # first, check for special characters
    char_string='[!=<>]'
    specialChars = re.compile(char_string) #["=","!",">","<"] #/\|:
    otherSpecialChars = re.compile("withingeoDistanceisNullisNotNull") # not sure about this
    returnString=""

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs["galahSettings"]['atlas']

        # check to make sure the filter type is correct
    if type(f) is str:

        # need to check for special characters
        specialChar = specialChars.findall(f)
        if specialChar is None:
            if ["within","geoDistance","isNull","isNotNull"] not in specialChar:
                raise ValueError("Either your filters does not have the correct special characters {}".format(char_string) 
                                + "or we need to include another special character we have forgotten about.")
            else:
                specialChar = otherSpecialChars.findall(f)
        else:
            specialChar = "".join(specialChar)

        # split filter into parts
        parts = f.split(specialChar)

        # remove leading and trailing white spaces from each filter part
        for i, p in enumerate(parts):
            parts[i] = p.strip()

        if atlas in ["Global","GBIF"] and occurrencesGBIF:

            # how would within even be formatted?
            if specialChar in ["within"]:
                return {
                    "type": specialChar,
                    "geometry": parts[1]
                }
            # how would within even be formatted?
            elif specialChar in ["geoDistance"]:
                return {
                    "type": specialChar,
                    "latitude": parts[0],
                    "longitude": parts[1],
                    "distance": parts[2]
                }
            elif specialChar in ["isNull","isNotNull"]:
                return {
                    "type": specialChar,
                    "parameter": parts[0]
                }
            elif specialChar in GBIF_PREDICATE_DEFINITIONS.keys() and type(GBIF_PREDICATE_DEFINITIONS[specialChar]) is dict:
                parts[0] = "_".join([entry.upper() for entry in re.findall('.[^A-Z]*', parts[0])])
                return {
                    "type": GBIF_PREDICATE_DEFINITIONS[specialChar][0],
                    "predicates": [{
                            "type":GBIF_PREDICATE_DEFINITIONS[specialChar][1],
                            "key":parts[0],
                            "value":parts[1]
                        }
                    ]
                }
            elif specialChar in GBIF_PREDICATE_DEFINITIONS.keys():
                parts[0] = "_".join([entry.upper() for entry in re.findall('.[^A-Z]*', parts[0])])
                return {
                    "type": GBIF_PREDICATE_DEFINITIONS[specialChar],
                    "key":parts[0],
                    "value":parts[1]
                }
            else:
                raise ValueError("{} is not a valid logical filter for GBIF.  For a list of those, go to https://www.gbif.org/developer/occurrence#download".format(f))

        elif atlas in ["Global","GBIF"]:

            # start checking for different logical operators, starting with equals
            if specialChar == '=' or specialChar == '==':
                returnString+="{}={}".format(parts[0],parts[1].replace(" ", "%20"))
            elif specialChar == '>=' or specialChar == '=>':
                returnString+="{}={}%2C%2A".format(parts[0],parts[1].replace(" ", "%20")) #,*
            elif specialChar == '>':
                returnString+="{}={}%2C%2A".format(parts[0],int(parts[1])+1) #,*
            elif specialChar == '<':
                returnString+="{}=%2A%2C{}".format(parts[0],int(parts[1])-1) #,*
            elif specialChar == '!=' or specialChar == '=!': ### NOT SURE ABOUT THIS
                returnString+="{}=%2A%2C{}".format(parts[0],parts[1].replace(" ", "%20")) #,*
            else:
                raise ValueError("The symbol {} is not currently available in galah for atlas {}.".format(specialChar,atlas))

            return returnString

        elif atlas in ["Australia","ALA"]:
            if specialChar == '=' or specialChar == '==':    
                if parts[1].isdigit() and ifgroupBy:
                    return "{}:{}".format(parts[0],parts[1])
                elif parts[1] == '':
                    return "*:* AND -{}:*".format(parts[0])
                elif parts[1] == "True":
                    return"assertions:{}".format(parts[0])
                elif parts[1] == "False":
                    return "-assertions:{}".format(parts[0])
                else:
                    # check if this is array
                    arrayChars = re.compile('[\[\]]')
                    arrayChar = arrayChars.findall(parts[1])
                    if arrayChar:
                        temp_array = parts[1][1:-1].split(",")
                        for value in temp_array:
                            # added quotes here
                            returnString += "{}:\"{}\" OR ".format(parts[0], value)
                        returnString = returnString[:-4]
                        return returnString
                    else:
                        return "{}:\"{}\"".format(parts[0],parts[1])
        
            elif specialChar == '>':
                return "{}:[{} TO *] AND -({}:{})".format(parts[0], parts[1], parts[0], parts[1])

            # less than
            elif specialChar == '<':
                return "{}:[* TO {}] AND -({}:{})".format(parts[0], parts[1], parts[0], parts[1])

            # greater than or equal to
            elif specialChar == '=>' or specialChar == '>=':
                return "{}:[{} TO *]".format(parts[0], parts[1])

            # less than or equal to
            elif specialChar == '<=' or specialChar == '=<':
                return "{}:[* TO {}]".format(parts[0], parts[1])

            # not equal to
            elif specialChar == '!=' or specialChar == '=!':
                print("here")
                return "-{}:{}".format(parts[0], parts[1])
                
            # else, there is either an error in the filters or a missing case
            else:
                raise ValueError("The special character {} is not included in the filters function.  Either it is not a logical operator, or it has not been included yet.".format(specialChar[0]))

        # all other atlases are like this
        else:

            # start checking for different logical operators, starting with equals
            if specialChar == '=' or specialChar == '==':

                # check if the filter is a number or a string and if there is a group by
                if parts[1].isdigit() and ifgroupBy:
                    # this one is square brackets
                    #returnString += "%5B{}:%22{}%22%5d".format(parts[0], parts[1])
                    returnString += "%28{}%3A%22{}%22%29".format(parts[0], parts[1].replace(" ", "%20"))
                # if filter is querying a field that has no value
                elif parts[1] == '':
                    #returnString += "%28{}%3A%28%2A%29%29".format(parts[0])
                    returnString += "%2A%3A%2A%20AND%20-{}%3A%2A".format(parts[0])
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

            # return a string to be added to the URL
            return returnString

    # let the user know that their variable is not of the correct type
    else:
        raise TypeError("Your filters need to either be a string (for one filters), or a list of strings.")