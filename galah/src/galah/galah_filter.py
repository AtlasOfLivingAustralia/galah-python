import itertools
import re

from .common_dictionaries import GBIF_PREDICATE_DEFINITIONS
from .galah_config import readConfig


def galah_filter(f, occurrencesGBIF=False):
    """
    "Filters" are arguments of the form field logical value that are used to narrow down the number of records returned by
    a specific query. For example, it is common for users to request records from a particular year (``year=2020``), or
    to return all records except for fossils (``basisOfRecord!=FossilSpecimen``).

    Filters are passed to ``atlas_occurrences()``, ``atlas_species()``, ``atlas_counts()`` or ``atlas_media()``.
    """

    # first, check for special characters
    char_string = "[!=<>]"
    specialChars = re.compile(char_string)
    otherSpecialChars = re.compile("withingeoDistanceisNullisNotNull")  # not sure about this
    returnString = ""

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs["galahSettings"]["atlas"]

    # need to check for special characters
    specialChar = specialChars.findall(f)
    if specialChar is None or len(specialChar) == 0:
        if ["within", "geoDistance", "isNull", "isNotNull"] not in specialChar:
            raise ValueError(
                "Either your filters does not have the correct special characters {}".format(char_string)
                + "or we need to include another special character we have forgotten about."
            )
        specialChar = otherSpecialChars.findall(f)
    else:
        specialChar = "".join(specialChar)

    # split filter into parts
    parts = f.split(specialChar)

    # remove leading and trailing white spaces from each filter part
    for i, p in enumerate(parts):
        parts[i] = p.strip()

    # first check if occurrences are being called with GBIF
    if atlas in ["Global", "GBIF"] and occurrencesGBIF:

        occurrences_GBIF_filters = {}

        # check for any logical expressions that are not included
        check_for_characters(specialChar=specialChar, string_dict=GBIF_PREDICATE_DEFINITIONS)

        # return GBIF predicates
        return process_GBIF_predicates(
            specialChar=specialChar, parts=parts, occurrences_GBIF_filters=occurrences_GBIF_filters
        )

    # then, check if your atlas is GBIF
    elif atlas in ["Global", "GBIF"]:

        # all return strings
        return_strings_GBIF = {
            "=": "{}={}".format(parts[0], parts[1].replace(" ", "%20")),
            "==": "{}={}".format(parts[0], parts[1].replace(" ", "%20")),
            ">=": "{}={}%2C%2A".format(parts[0], parts[1].replace(" ", "%20")),
            "=>": "{}={}%2C%2A".format(parts[0], parts[1].replace(" ", "%20")),
            ">": "%28{}:%5B{}%20TO%20*%5d%20AND%20-%28{}%3A%22{}%22%29%29".format(
                parts[0], parts[1], parts[0], parts[1]
            ),
            "<": '%28{}%3A%5B*%20TO%20{}%5d%20AND%20-%28{}%3A"{}"%29%29'.format(parts[0], parts[1], parts[0], parts[1]),
            # ">": "{}={}%2C%2A".format(parts[0], int(parts[1]) + 1),
            # "<": "{}=%2A%2C{}".format(parts[0], int(parts[1]) - 1),
            "!=": "{}=%2A%2C{}".format(parts[0], parts[1].replace(" ", "%20")),
            "=!": "{}=%2A%2C{}".format(parts[0], parts[1].replace(" ", "%20")),
        }

        # check for any logical expressions that are not included
        check_for_characters(specialChar=specialChar, string_dict=return_strings_GBIF)

        # add another filter to the return string
        returnString += return_strings_GBIF[specialChar]

        # return the string
        return returnString

    # all other atlases are like this
    else:

        # strings to return for all other atlases
        return_strings = {
            "=": "{}={}".format(parts[0], parts[1].replace(" ", "%20")),
            "==": "{}={}".format(parts[0], parts[1].replace(" ", "%20")),
            ">=": "%28{}%3A%5B{}%20TO%20%2A%5d%29".format(parts[0], parts[1]),
            "=>": "%28{}%3A%5B{}%20TO%20%2A%5d%29".format(parts[0], parts[1]),
            ">": "%28{}:%5B{}%20TO%20*%5d%20AND%20-%28{}%3A%22{}%22%29%29".format(
                parts[0], parts[1], parts[0], parts[1]
            ),
            "<": '%28{}%3A%5B*%20TO%20{}%5d%20AND%20-%28{}%3A"{}"%29%29'.format(parts[0], parts[1], parts[0], parts[1]),
            "<=": "%28{}%3A%5B*%20TO%20{}%5d%29".format(parts[0], parts[1]),
            "=<": "%28{}%3A%5B*%20TO%20{}%5d%29".format(parts[0], parts[1]),
            "!=": "-%28{}%3A%22{}%22%29".format(parts[0], parts[1]),
            "=!": "-%28{}%3A%22{}%22%29".format(parts[0], parts[1]),
        }

        # check for any logical expressions that are not included
        check_for_characters(specialChar=specialChar, string_dict=return_strings)

        # start checking for different logical operators, starting with equals
        if specialChar == "=" or specialChar == "==":

            returnString = process_equals_filter(parts=parts, returnString=returnString)

        else:

            # create return strings
            returnString += return_strings[specialChar]

        # return a string to be added to the URL
        return returnString


def check_for_characters(specialChar=None, string_dict=None):
    """Check for any logical expressions that aren't included here"""

    if specialChar not in string_dict.keys():
        raise ValueError(
            "The special character {} is not included in the filters function.  Either it is not a logical operator, or it has not been included yet.".format(
                specialChar[0]
            )
        )


def process_GBIF_predicates(specialChar=None, parts=None, occurrences_GBIF_filters=None):
    """create the GBIF predicates"""

    # occurrences_GBIF_filters = {
    #     "within": {"type": specialChar, "geometry": parts[1]},
    #     "geoDistance": {
    #         "type": specialChar,
    #         "latitude": parts[0],
    #         "longitude": parts[1],
    #         "distance": parts[2],
    #     },
    #     "isNull": {"type": specialChar, "parameter": parts[0]},
    #     "isNotNull": {"type": specialChar, "parameter": parts[0]},
    # }

    # first check for dictionaries in the vocab
    if specialChar in GBIF_PREDICATE_DEFINITIONS.keys() and type(GBIF_PREDICATE_DEFINITIONS[specialChar]) is dict:
        parts[0] = "_".join([entry.upper() for entry in re.findall(".[^A-Z]*", parts[0])])
        return {
            "type": GBIF_PREDICATE_DEFINITIONS[specialChar][0],
            "predicates": [
                {
                    "type": GBIF_PREDICATE_DEFINITIONS[specialChar][1],
                    "key": parts[0],
                    "value": parts[1],
                }
            ],
        }

    # then check if the predicate definitions are what we want
    elif specialChar in GBIF_PREDICATE_DEFINITIONS.keys():
        parts[0] = "_".join([entry.upper() for entry in re.findall(".[^A-Z]*", parts[0])])
        return {
            "type": GBIF_PREDICATE_DEFINITIONS[specialChar],
            "key": parts[0],
            "value": parts[1],
        }

    # else, use the filters provided
    else:
        return occurrences_GBIF_filters[specialChar]


def process_equals_filter(parts=None, returnString=None):

    # check if the filter is a number or a string and if there is a group by
    if parts[1].isdigit():
        # this one is square brackets
        # returnString += "%5B{}:%22{}%22%5d".format(parts[0], parts[1])
        returnString += "%28{}%3A%22{}%22%29".format(parts[0], parts[1].replace(" ", "%20"))
    # if filter is querying a field that has no value
    elif parts[1] == "":
        # returnString += "%28{}%3A%28%2A%29%29".format(parts[0])
        returnString += "%2A%3A%2A%20AND%20-{}%3A%2A".format(parts[0])
    elif parts[1] == "True":
        returnString += "%28assertions%3A%22{}%22%29".format(parts[0])
    elif parts[1] == "False":
        returnString += "-%28assertions%3A%22{}%22%29".format(parts[0])
    else:
        # check if this is array
        arrayChars = re.compile("\]\[")
        arrayChar = arrayChars.findall(parts[1])
        if arrayChar:
            returnString += "%28"
            temp_array = parts[1][1:-1].split(",")
            for value in temp_array:
                returnString += "{}%3A22{}%22%20OR%20".format(
                    parts[0],
                    value.replace(" ", "%20").replace("'", "").replace('"', "").replace("&", "%26").replace(",", "%2C"),
                )
            returnString = returnString[:-8] + "%29"
        # added quotes
        else:
            returnString += "%28{}%3A%22{}%22%29".format(
                parts[0],
                parts[1].replace(" ", "%20").replace("'", "").replace('"', "").replace("&", "%26").replace(",", "%2C"),
            )

    # return the string
    return returnString


def check_for_duplicate_filters(filters=None):

    # first, check if there are any duplicate names
    filter_names = [x.split("=")[0] for x in filters]
    if len(set(filter_names)) == len(filters):
        return filters

    # now, sort filters for easy duplication detection
    filters = sorted(filters)

    # initialise important variables
    # duplicates = {}
    non_duplicates = []

    # find and log duplicates
    duplicates = log_duplicates(filters=filters)

    # get all duplicate values to check for non-duplicates
    duplicate_values = list(itertools.chain.from_iterable([*duplicates.values()]))

    # compile the non duplicate values
    for i in range(len(filters)):
        if i not in duplicate_values:
            non_duplicates.append(i)

    # create new duplicate values
    new_duplicates = []
    for name in duplicates.keys():
        vals = []
        for index in duplicates[name]:
            vals.append(filters[duplicates[name][index]].split("=")[1])
        new_duplicates.append("{}={}".format(name, ",".join(vals)))

    # get the non duplicate values
    non_duplicate_values = [filters[i] for i in non_duplicates]

    # add them together for new filters
    return new_duplicates + non_duplicate_values


def log_duplicates(filters=None):
    """find duplicates and indices in filters"""

    # initialise duplicates dict
    duplicates = {}

    # loop through filters to find duplicates
    for i in range(len(filters) - 1):
        name1 = filters[i].split("=")[0]
        name2 = filters[i + 1].split("=")[0]
        if name1 == name2:
            if name1 not in duplicates:
                duplicates[name1] = [i, i + 1]
            else:
                if i not in duplicates[name1]:
                    duplicates[name1].append(i)
                if i + 1 not in duplicates[name1]:
                    duplicates[name1].append(i + 1)

    # return the duplicates dictionary
    return duplicates


def process_or_filters(or_filters=None, URL=None):

    # loop over all or filters to add to URL
    for f in or_filters:
        new_filters = []
        if "|" in f:
            for x in f.split(" | "):
                new_filters.append(galah_filter(x))
        elif "," in f:
            parts = f.split("=")
            name = parts[0]
            values = parts[1].split(",")
            for x in values:
                new_filters.append(galah_filter("{}={}".format(name, x)))
        URL += "%28" + "%20OR%20".join(new_filters) + "%29%20AND%20"

    # return URL
    return URL
