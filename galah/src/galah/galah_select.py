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
                for s in ["decimalLatitude","decimalLongitude","eventDate","scientificName","taxonConceptID","recordID","dataResourceName","occurrenceStatus"]:
                    tempstring+="{}%2C".format(s)
            elif selection == "event":
                for s in ["eventRemarks","eventTime","eventID","eventDate","samplingEffort","samplingProtocol"]:
                    tempstring+="{}%2C".format(s)
            elif selection == "media":
                for s in ["multimedia","multimediaLicence","images","videos","sounds"]:
                    tempstring+="{}%2C".format(s)
            else:
                tempstring+="{}%2C".format(selection)
        return tempstring

    # else, throw an error
    else:
        raise ValueError("This function only takes strings or lists as its arguments")
