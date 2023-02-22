from .show_all import show_all

'''
function is meant to search all values for possible query fields - they are defined as None so you can narrow down the
large list of all the potential variables to add to your atlas query.  Choosing which column you query is also an option
'''
def search_all(assertions=None,
               atlases=None,
               apis=None,
               collection=None,
               datasets=None,
               fields=None,
               licences=None,
               lists=None,
               profiles=None,
               providers=None,
               reasons=None,
               ranks=None,
               column_name=None
               ):
    """
    Used for getting and searching various amounts of information about the chosen atlas you want to
    get counts and occurrences from.

    To find a list of endpoints in your chosen api, type

    .. prompt:: python

        import galah
        galah.search_all(apis="Australia")

    which returns

    .. program-output:: python -c "import galah; print(galah.search_all(apis=\\\"Australia\\\"))"
    """

    # set up the option for getting back multiple values
    return_array=[]

    # search options for assertions
    if assertions is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(assertions=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name='description'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(assertions) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(assertions, case=True, na=False)].sort_values('id', key=lambda x: x.str.len()))
        else:
            raise ValueError("You can only pass one string to your search parameter = run show_all(assertions=True) to get strings to pass")

    # search options for atlases
    if atlases is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(atlases=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name='atlas'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(atlases) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(atlases, case=True, na=False)].sort_values('atlas', key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(atlases=True) to get strings to pass")

    # search options for apis
    if apis is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(apis=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name='atlas'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(apis) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(apis, case=True, na=False)].sort_values('atlas', key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(apis=True) to get strings to pass")

    # search options for collection
    if collection is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(collection=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name = 'description'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(collection) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(collection, case=True, na=False)].sort_values('id',
                                                                                                      key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(apis=True) to get strings to pass")

    # search options for datasets
    if datasets is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(datasets=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name = 'description'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(datasets) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(datasets, case=True, na=False)].sort_values('id',
                                                                                                      key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(datasets=True) to get strings to pass")

    # search options for fields
    if fields is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(fields=True)

        # check to see if user wants default column name
        if column_name is None:
            column_name = 'description'

        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(fields, case=True, na=False)].sort_values('id',
                                                                                                      key=lambda x: x.str.len()).reset_index(drop = True, inplace = True))
    else:
        raise ValueError(
            "You can only pass one string to your search parameter = run show_all(fields=True) to get strings to pass")
    
    # search options for licences
    if licences is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(licences=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name = 'description'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(licences) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(licences, case=True, na=False)].sort_values('id',
                                                                                                      key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(licences=True) to get strings to pass")

    # search options for lists
    if lists is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(lists=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name = 'listName'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(lists) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(lists, case=True, na=False)].sort_values('listName',
                                                                                                      key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(lists=True) to get strings to pass")

    # search options for profiles
    if profiles is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(profiles=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name = 'description'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(profiles) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(profiles, case=True, na=False)].sort_values('id',
                                                                                                      key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(profiles=True) to get strings to pass")

    # search options for providers
    if providers is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(providers=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name = 'description'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(providers) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(providers, case=True, na=False)].sort_values('id',
                                                                                                      key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(providers=True) to get strings to pass")

    # search options for ranks
    if ranks is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(ranks=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name = 'description'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(ranks) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(ranks, case=True, na=False)].sort_values(
                    'description',key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(ranks=True) to get strings to pass")

    # search options for reasons
    if reasons is not None:
        # call show_all to get all the possible values
        dataFrame = show_all(reasons=True)
        # check to see if user wants default column name
        if column_name is None:
            column_name = 'description'
        # throw ValueError if column_name variable is not a string
        elif type(column_name) is not str:
            raise ValueError("Only strings are a valid query for the column_name variable")
        # check to see if the user input the correct variable type; else, throw value error
        if type(reasons) is str:
            return_array.append(
                dataFrame.loc[dataFrame[column_name].astype(str).str.contains(reasons, case=True, na=False)].sort_values('id',
                                                                                                      key=lambda x: x.str.len()))
        else:
            raise ValueError(
                "You can only pass one string to your search parameter = run show_all(reasons=True) to get strings to pass")

    # return a single data frame if only one query was flagged; otherwise, return array
    if len(return_array) == 1:
        return return_array[0]
    return return_array
