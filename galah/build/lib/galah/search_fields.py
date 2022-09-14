# returns a data.frame of all fields matching the type specified (columns is id, description, type, link)
# example: search.fields(query,type=["all","fields","layers","assertions","media","other"])
#  query: a search string (not case sensitive) example:
# returns
def search_fields(query=None,type=None):
    # pseudocode here
    n=1