import io

import pandas as pd
import requests

from .add_to_payload_functions import add_to_payload_ALA
from .atlas_occurrences import atlas_occurrences, check_for_403_error
from .common_add_functions import add_extras_to_URL, add_filters, add_spatial_shapes, add_taxa
from .common_checks import check_atlas, check_email_empty, check_for_non_working_atlases, check_string_list
from .common_dictionaries import ATLAS_SPECIES_FIELDS
from .common_functions import group_by_atlas_species, print_if_verbose, set_bool_argument
from .galah_config import get_api_url, readConfig
from .show_all import show_all
from .version import __version__


def atlas_species(
    taxa=None,
    scientific_name=None,
    rank="species",
    group_by=None,  # taxonConceptID
    filters=None,
    status_accepted=True,
    use_data_profile=False,
    counts=False,
    polygon=None,
    bbox=None,
    simplify_polygon=False,
    config_file=None,
    tolerance=None,
    mint_doi=None,
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
        status_accepted : logical
            If ``True``, galah gives you only the accepted taxonomic ranks. Default is ``False``.  **FOR GBIF ONLY
        polygon : shapely Polygon
            A polygon shape denoting a geographical region.  Defaults to ``None``.
        bbox : dict or shapely Polygon
            A polygon or dictionary type denoting four points, which are the corners of a geographical region.  Defaults to ``None``.
        simplify_polygon : logical
            When using the ``polygon`` argument of ``galah.atlas_counts()``, specifies whether or not to draw a bounding box around the polygon and use this instead.  Defaults to ``False``.
        config_file : string
            If you want to specify your own config file, put the path and name of the file here.  This is applicable when you are running on a server and each user has different configurations.  Defaults to ``None``.

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        galah.atlas_species(taxa="Heleioporus")


    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);print(galah.atlas_species(taxa=\\\"Heleioporus\\\"))"
    """

    # ---------------------------------------------------------------------------------------------
    # Declare all variables, run checks on compatibility of arguments.
    # ---------------------------------------------------------------------------------------------

    # get configs
    configs = readConfig(config_file=config_file)

    # get atlas
    atlas = configs["galahSettings"]["atlas"]
    verbose = set_bool_argument(arg=configs["galahSettings"]["verbose"], name_arg="verbose")
    timeout = int(configs["galahSettings"]["timeout"])
    authenticate = set_bool_argument(arg=configs["galahSettings"]["authenticate"], name_arg="authenticate")
    access_token = configs["galahSettings"]["access_token"]
    client_id = configs["galahSettings"]["client_id"]

    # check to see if atlas is in list of non-functioning atlases
    check_for_non_working_atlases(atlas=atlas)

    # check atlas is valid
    check_atlas(atlas=atlas, function="atlas_species")

    # check for email
    check_email_empty(config_file=config_file)

    # get headers
    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # check variable types
    filters = check_string_list(filters, "filters")
    taxa = check_string_list(taxa, "taxa")

    atlas_species_error_checks(rank=rank, atlas=atlas)

    # get the ID of the rank to use to facet the data
    rankID = ATLAS_SPECIES_FIELDS[atlas][rank]

    # ---------------------------------------------------------------------------------------------
    # For GBIF, run atlas_occurrences, but with an option to get a species list
    # Then, checks if authenticate option is True and the atlas is ALA
    # Otherwise, go with default workflow
    # ---------------------------------------------------------------------------------------------

    # GBIF is treated differently, as it gives us a species list
    if atlas in ["Global", "GBIF"]:

        # get the initial list
        test_list = atlas_occurrences(
            taxa=taxa,
            filters=filters,
            species_list=True,
            status_accepted=status_accepted,
        )

        # get the species fields for the data frame to check against
        species_fields = list(ATLAS_SPECIES_FIELDS[atlas].keys())

        # get the index of your rank, and the one below it
        index = species_fields.index(rank)

        # if rank is not species, only select for rank user has specified
        if rank != "species":

            rank_below = species_fields[index + 1]

            # only select ranks user is interested in
            curated_list = test_list[test_list[rank_below].map(type) == float]

            # remove unnecessary fields
            for i in species_fields[index + 1 :]:
                del curated_list[i]
                del curated_list["{}Key".format(i)]

            # return the curated list
            return curated_list.reset_index(drop=True)

        # else, return everything
        return test_list.reset_index(drop=True)

    # atlas_species()
    if atlas in ["Australia", "ALA"] and authenticate:

        # create payload and add buffer to polygon if user specifies it
        payload = add_to_payload_ALA(
            payload={},
            atlas=atlas,
            taxa=taxa,
            filters=filters,
            polygon=polygon,
            bbox=bbox,
            simplify_polygon=simplify_polygon,
            scientific_name=scientific_name,
            authenticate=authenticate,
        )

        # add authorization token and client id for authentication
        headers["Authorization"] = "Bearer {}".format(access_token)
        headers["client_id"] = client_id

        # get the query id url
        qid_URL, method2 = get_api_url(column1="api_name", column1value="occurrences_qid")

        # print this information if verbose option is selected
        print_if_verbose(verbose=verbose, headers=headers, URL=qid_URL, method=method2, payload=payload)

        # get qid
        qid = requests.request(method2, qid_URL, data=payload, headers=headers)

        # create the URL to grab the species ID and lists
        baseURL, method = get_api_url(column1="api_name", column1value="records_species", config_file=config_file)
        URL = baseURL + "?fq=%28qid%3A" + qid.text + "%29"
        URL = group_by_atlas_species(group_by=group_by, rankID=rankID, URL=URL)

    else:

        # get initial url
        baseURL, method = get_api_url(column1="api_name", column1value="records_species", config_file=config_file)

        # add information to URL
        URL = add_taxa(taxa=taxa, atlas=atlas, URL=baseURL, scientific_name=scientific_name)
        URL = add_filters(filters=filters, atlas=atlas, URL=URL)
        URL = group_by_atlas_species(group_by=group_by, rankID=rankID, URL=URL)
        URL = add_spatial_shapes(
            polygon=polygon, bbox=bbox, URL=URL, simplify_polygon=simplify_polygon, tolerance=tolerance
        )

    # ---------------------------------------------------------------------------------------------
    # Add common extras to URL
    # ---------------------------------------------------------------------------------------------

    # add this for getting counts
    if counts:

        URL += "&count=true"

    # set lookup=True to get all species data
    URL += "&lookup=True"

    # mint a DOI if requested
    if mint_doi:
        URL += "&mintDoi=TRUE&"

    # add last things to URL
    if atlas in ["Australia", "ALA"]:
        URL += add_extras_to_URL(
            add_email=False,
            use_data_profile=use_data_profile,
            data_profile_list=list(show_all(profiles=True)["shortName"]),
            atlas=atlas,
            config_file=config_file,
        )
    else:
        URL += add_extras_to_URL(add_email=False, atlas=atlas, config_file=config_file)

    # check to see if user wants the query URL
    print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

    # get response from url
    response = requests.request(method=method, url=URL, headers=headers, timeout=timeout)

    # check to see if the user has gotten a 403 error
    check_for_403_error(response=response, atlas=atlas)

    if atlas in ["United Kingdom"]:
        return pd.DataFrame(response.json()[0]["fieldResult"])

    # return data as pandas dataframe
    return pd.read_csv(io.StringIO(response.text))


def atlas_species_error_checks(rank=None, atlas=None):
    """raise all possible exceptions/errors before running the rest of the function"""

    # check to see if rank is in possible ranks for atlas
    if rank.lower() not in ATLAS_SPECIES_FIELDS[atlas]:
        raise ValueError(
            "{} is not a valid rank for the {} atlas.  Possible ranks are:\n\n{}\n".format(
                rank, atlas, ", ".join(ATLAS_SPECIES_FIELDS[atlas])
            )
        )

    # raise warning - not sure how to fix it
    if atlas in ["Spain"]:
        print(
            "There have been some issues getting all species when using a genus name.  If genus doesn't work, either use a species name or anything of family or higher order."
        )
    if atlas in ["Sweden"]:
        print(
            "There have been some issues getting taxonomy from the Swedish atlas, as they don't store names of taxon higher than species."
        )
