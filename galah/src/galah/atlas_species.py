import requests,urllib.parse,io
import pandas as pd

from .search_taxa import search_taxa
from .get_api_url import get_api_url,readConfig
from .atlas_occurrences import atlas_occurrences
from .common_dictionaries import ATLAS_KEYWORDS,ATLAS_SPECIES_FIELDS,atlases
from .common_functions import add_filters

# this function looks for all species with the associated name
def atlas_species(taxa=None,
                  rank="species",
                  filters=None,
                  verbose=False,
                  status_accepted=True):
    """
    While there are reasons why users may need to check every record meeting their search criteria (i.e. using ``galah.atlas_occurrences()``), 
    a common use case is to simply identify which species occur in a specified region, time period, or taxonomic group. 
    This function returns a ``pandas.DataFrame`` with one row per species, and columns giving associated taxonomic information.

    Parameters
    ----------
        taxa : string / list
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.  
        rank : string
            the rank you ultimately want to get names for, i.e. "genus" or "species".  Default is ``species``.
        filters : string
            filters, in the form ``field`` ``logical`` ``value`` (e.g. ``"year=2021"``)
        verbose : logical
            If ``True``, galah gives you the URLs used to query all the data.  Default to ``False``.
        status_accepted : logical
            If ``True``, galah gives you only the accepted taxonomic ranks. Default is ``False``.  **FOR GBIF ONLY

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        galah.atlas_species(taxa="Heleioporus")

    .. program-output:: python -c "import galah; print(galah.atlas_species(taxa=\\\"Heleioporus\\\"))"
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas'] 

    # first, check if the user has specified a taxa and if it is of the right variable type
    if type(taxa) is not str and type(taxa) is not list and taxa is not None:
        raise ValueError("Only a string or list can be specified for taxa names")

    # check to see if rank is in possible ranks for atlas
    if rank.lower() not in ATLAS_SPECIES_FIELDS[atlas]:
        raise ValueError("{} is not a valid rank for the {} atlas.  Possible ranks are:\n\n{}\n".format(rank,atlas,", ".join(ATLAS_SPECIES_FIELDS[atlas])))

    # get the ID of the rank to use to facet the data
    rankID = ATLAS_SPECIES_FIELDS[atlas][rank]
    
    # get initial url
    if atlas not in ["Global","GBIF"]:
        baseURL = get_api_url(column1='api_name', column1value='records_species')
    else:
        baseURL = get_api_url(column1='api_name', column1value='records_occurrences')

    # raise warning - not sure how to fix it
    if atlas in ["Spain"]:
        print("There have been some issues getting all species when using a genus name.  If genus doesn't work, either use a species name or anything of family or higher order.")
    if atlas in ["Sweden"]:
        print("There have been some issues getting taxonomy from the Swedish atlas, as they don't store names of taxon higher than species.")

    # get the taxonConceptID for taxa
    if atlas in ["Australia","Austria","Brazil","France","Guatemala","Spain","Sweden"]:

        # if there is no taxa, just add question mark
        if taxa is None:
            
            # remember to add question mark
            URL = baseURL + "?"

        # if there is taxa, add these as fields on the URL
        else:
            
            # get the taxonConceptID for taxa - first check for extant atlas
            if atlas in atlases:
                taxonConceptID = list(search_taxa(taxa)[ATLAS_KEYWORDS[atlas]])
            else:
                raise ValueError("Atlas {} is not taken into account".format(atlas))

            # add taxon IDs to the URL
            if atlas in ["Global","GBIF"]:
                URL = baseURL + "".join(["taxonKey={}&".format(
                    urllib.parse.quote(str(tid))) for tid in taxonConceptID])
            else:
                URL = baseURL + "?fq=%28lsid%3A" + "%20OR%20lsid%3A".join(
                    urllib.parse.quote(str(tid)) for tid in taxonConceptID) + "%29"
        
        # check if filters are specified
        if filters is not None:

            # check the type of variable filters is
            if type(filters) is list or type(filters) is str:

                # add filters to URL
                if taxa is None:
                    URL = add_filters(URL=URL+"fq=",atlas=atlas,filters=filters) + "&facets={}".format(rankID)
                else:
                    URL = add_filters(URL=URL+"AND",atlas=atlas,filters=filters) + "&facets={}".format(rankID) #%29

            # else, make sure that the filters is in the following format
            else:
                raise TypeError("filters should only be a list, and are in the following format:\n\nfilters=[\'year:2020\']")
        
        else:
             
            # add facets into URL
            URL += "&facets={}".format(rankID)

        # set lookup=True to get all species data
        URL += "&lookup=True"

        # check to see if user wants the query URL
        if verbose:
            print("URL for querying:\n\n{}\n".format(URL))

        # get url and transform from a text string to a list
        response = requests.get(URL)
        return pd.read_csv(io.StringIO(response.text))
        
    # GBIF is treated differently, as it gives us a species list
    elif atlas in ["Global","GBIF"]:

        # get the initial list
        test_list = atlas_occurrences(taxa=taxa,filters=filters,species_list=True,verbose=verbose,status_accepted=status_accepted)
        
        # get the species fields for the data frame to check against
        species_fields = list(ATLAS_SPECIES_FIELDS[atlas].keys())

        # get the index of your rank, and the one below it
        index = species_fields.index(rank)
        
        # if rank is not species, only select for rank user has specified
        if rank != "species":

            rank_below = species_fields[index+1]

            # only select ranks user is interested in
            curated_list = test_list[test_list[rank_below].map(type) == float]
            
            # remove unnecessary fields
            for i in species_fields[index+1:]:
                del curated_list[i]
                del curated_list["{}Key".format(i)]

            # return the curated list
            return curated_list.reset_index(drop=True)
        
        # else, return everything
        return test_list.reset_index(drop=True)
    
    # else, this atlas hasn't been integrated into atlas_species yet
    else:
        raise ValueError("Atlas {} is not taken into account".format(atlas))