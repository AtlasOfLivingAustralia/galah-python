'''
select
------
takes a list of selections, and converts it into URL-compatible language to query the API

arguments
---------
select: a string or a list of strings with filters (i.e. "year>2018" or ["year>2018", "basisOfRecord=HUMAN_OBSERVATION"])

returns
------- 
returnString: a string to add to the URL to query the API
'''
def galah_select(select=None,atlas=None):

    # generate a temporary string for fields to return to another function
    tempstring="fields="

    # check if this argument is provided
    if select is None:
        raise ValueError("You need to provide one argument: category(ies) to get from the ALA API as a string or list.")
    
    # otherwise, create a URL string and return it
    elif type(select) is str or type(select) is list:
        if type(select) is str:
            select=[select]
        for selection in select:
            if selection == "basic":
                tempstring += "%2C".join(["decimalLatitude","decimalLongitude","eventDate","scientificName","taxonConceptID","recordID","dataResourceName","occurrenceStatus"]) + "%2C"
            elif selection == "event":
                tempstring += "%2C".join(["eventRemarks","eventTime","eventID","eventDate","samplingEffort","samplingProtocol"]) + "%2C"
            elif selection == "media":
                tempstring += "%2C".join(["multimedia","multimediaLicence","images","videos","sounds"]) + "%2C"
            else:
                tempstring+="{}%2C".format(selection)
        if tempstring[-3:] == "%2C":
            tempstring = tempstring[:-3]
        return tempstring

    # else, throw an error
    else:
        raise ValueError("This function only takes strings or lists as its arguments")
