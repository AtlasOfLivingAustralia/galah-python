'''
select
------
takes a list of selections, and converts it into URL-compatible language to query the API

arguments
---------
selectionList: a string or a list of strings with filters (i.e. "year>2018" or ["year>2018", "basisOfRecord=HUMAN_OBSERVATION"])

returns
------- 
returnString: a string to add to the URL to query the API

TODO
----
1. Test more filters
'''
def galah_select(selectionList=None):
    # pseudocode here
    tempstring="fields="
    if selectionList is None:
        return ValueError("You need to provide one argument: category(ies) to get from the ALA API as a string or list.")
    elif type(selectionList) is str or type(selectionList) is list:
        if type(selectionList) is str:
            selectionList=[selectionList]
        for selection in selectionList:
            tempstring+="{}%2C".format(selection)
        return tempstring