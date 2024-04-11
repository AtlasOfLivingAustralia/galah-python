import requests,urllib.parse,io
import pandas as pd
from .search_taxa import search_taxa
from .get_api_url import get_api_url,readConfig
from .atlas_occurrences import atlas_occurrences
from .apply_data_profile import apply_data_profile
from .common_dictionaries import ATLAS_KEYWORDS,ATLAS_SPECIES_FIELDS,atlases
from .common_functions import add_filters,add_to_payload_ALA
from .show_all import show_all
from .version import __version__

import json

def atlas_species(taxa=None,
                  scientific_name=None,
                  rank="species",
                  filters=None,
                  verbose=False,
                  status_accepted=True,
                  use_data_profile=False,
                  counts=False,
                  polygon=None,
                  bbox=None,
                  simplify_polygon=False
                  ):
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
        polygon : shapely Polygon
            A polygon shape denoting a geographical region.  Defaults to ``None``.
        bbox : dict or shapely Polygon
            A polygon or dictionary type denoting four points, which are the corners of a geographical region.  Defaults to ``None``.
        simplify_polygon : logical
            When using the ``polygon`` argument of ``galah.atlas_counts()``, specifies whether or not to draw a bounding box around the polygon and use this instead.  Defaults to ``False``.

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        galah.atlas_species(taxa="Heleioporus")

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.atlas_species(taxa=\\\"Heleioporus\\\"))"
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas'] 

    # get headers
    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # create payload variable so it is available for some atlases
    payload = {}

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
        baseURL,method = get_api_url(column1='api_name', column1value='records_species')
    else:
        baseURL,method = get_api_url(column1='api_name', column1value='records_occurrences')

    # raise warning - not sure how to fix it
    if atlas in ["Spain"]:
        print("There have been some issues getting all species when using a genus name.  If genus doesn't work, either use a species name or anything of family or higher order.")
    if atlas in ["Sweden"]:
        print("There have been some issues getting taxonomy from the Swedish atlas, as they don't store names of taxon higher than species.")

    if atlas in ["Australia","ALA"]:
        
        # create payload and add buffer to polygon if user specifies it
        payload = add_to_payload_ALA(payload=payload,atlas=atlas,taxa=taxa,filters=filters,polygon=polygon,
                                     bbox=bbox,simplify_polygon=simplify_polygon,scientific_name=scientific_name)

        # create the query id
        qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")
        qid = requests.request(method2,qid_URL,data=payload,headers=headers)
        
        # create the URL to grab the species ID and lists
        if use_data_profile:
            data_profile_list = list(show_all(profiles=True)['shortName'])
            baseURL = apply_data_profile(baseURL=baseURL,use_data_profile=use_data_profile,data_profile_list=data_profile_list)
            URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&facets={}&lookup=True".format(rankID)
            if counts:
                URL += "&count=true"
        else:
            URL = baseURL + "?fq=%28qid%3A" + qid.text + "%29&facets={}&lookup=True".format(rankID)
            if counts:
                URL += "&count=true"

        if verbose:
            print()
            print("headers: {}".format(headers))
            print()
            print("payload for queryID: {}".format(payload))
            print("queryID URL: {}".format(qid_URL))
            print("method: {}".format(method2))
            print()
            print("qid for query: {}".format(qid.text))
            print("URL for result:{}".format(URL))
            print("method: {}".format(method))
            print()

        # get data
        response = requests.request(method,URL,headers=headers)

        # check for daily maximum
        if response.status_code == 429:
            raise ValueError("You have reached the maximum number of daily queries for the ALA.")
        
        # return data as pandas dataframe
        return pd.read_csv(io.StringIO(response.text))

    # get the taxonConceptID for taxa
    elif atlas in ["Austria","Brazil","France","Guatemala","Spain","Sweden"]:

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
            print("\nURL being queried:\n\n{}\n".format(URL))

        # get response from url
        response = requests.request(method,URL,headers=headers)

        # check response first to see if user has hit maximum number of queries
        if response.status_code == 429:
            raise ValueError("You have reached the maximum number of daily queries for the ALA.")
        
        # return data as pandas dataframe
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