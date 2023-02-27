import requests

from .get_api_url import get_api_url
from .search_taxa import search_taxa

import sys

# create class for this
class Node:
    def __init__(self,name,rank):
        self.children = []
        self.name = name
        self.rank = rank
    def print_name(self):
        print(self.name)
    def print_rank(self):
        print(self.rank)

# printing the tree recursively
def print_tree(tree_or_leaf, level=0):
    head = tree_or_leaf.name
    rank = tree_or_leaf.rank
    tail = tree_or_leaf.children

    print('    ' * (level - 1) + ' |--' * (level > 0) + head + ' (' + rank + ')')

    for tree_or_leaf in tail:
        print_tree(tree_or_leaf, level + 1)

# this function prints out taxonomic trees for particular taxa
### TODO: Make sure I get the right answer for this
def atlas_taxonomy(taxa = None,
                   down_to = None):
    """
    The ALA has its' own internal taxonomy that is derived from authoritative sources. ``galah.atlas_taxonomy()`` provides a means to query 
    that taxonomy, returning a tree (class Node) showing which lower clades are contained within the specified taxon.

    Parameters
    ----------
        taxa : string
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.  
        down_to : string
            The identity of the clade at which the downwards search should stop. (e.g. ``"order"``)

    Returns
    -------
        An object of class ``tree``.

    Examples
    --------
        Return total records in your chosen atlas

        .. prompt:: python

            galah.atlas_taxonomy(taxa="fungi", down_to="phylum")

    """

    # check if taxa is None
    if taxa is None:
        raise ValueError("Please provide the name of a taxa")

    # list of taxonomic tree
    taxonomic_list = ['domain','kingdom','phylum','subphylum','class','order','family','genus','species']

    # get the initial
    response_lookup = requests.get(
        get_api_url(column1='called_by', column1value='atlas_taxonomy',column2='api_name',
                    column2value='species_lookup').replace("{id}",search_taxa(taxa=taxa)['taxonConceptID'][0]))

    # get starting point
    json = response_lookup.json()
    starting_rank = json['taxonConcept']['rankString']
    starting_index = taxonomic_list.index(starting_rank)

    # set the first node
    root = Node(taxa.lower().capitalize(),starting_rank)

    # figure out how far down to go
    if down_to is None:
        down_to = "species"
        end_index = taxonomic_list.index(down_to)
    elif down_to in taxonomic_list:
        end_index = taxonomic_list.index(down_to)
    else:
        raise ValueError("You can only specify one of the following in down_to argument:\n\n{}\n".format(taxonomic_list))

    # starting branch
    branches = [root]

    for i in range(starting_index+1,end_index+1):

        # get children up to a certain point
        new_branches = []

        # loop over branches in tree
        for branch in branches:

            taxon_check = search_taxa(taxa=branch.name)
            if taxon_check.empty:
                break
            taxonConceptID = search_taxa(taxa=branch.name)['taxonConceptID'][0]

            # get the children of the branch
            response_children = requests.get(
            get_api_url(column1='called_by', column1value='atlas_taxonomy', column2='api_name',
                        column2value='species_children').replace("{id}", taxonConceptID))

            # get all of the relevant children
            json = response_children.json()

            print("current branch: {}\n".format(branch.name))

            # loop over all the children
            for entry in json:
                # check to see if this is the right way to go about it
                #if entry['rank'] != "unranked" and entry['rank'] != "informal":
                if entry['rank'] == taxonomic_list[i]:
                    branch.children.append(Node(entry['name'].lower().capitalize(),entry['rank']))
                else:
                    print("entry that didn't make it: \n\t{} \n\t{}\n".format(entry['name'],entry['rank']))

        # get the new branches
        for branch in branches:
            for child in branch.children:
                new_branches.append(child)

        # reset branches
        branches = new_branches

    # doing all the printing
    print_tree(root)
