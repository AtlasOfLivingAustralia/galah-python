import io
import json
import time
import zipfile

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

from .common_add_functions import add_extras_to_URL, add_filters, add_predicates, add_spatial_shapes, add_taxa
from .common_checks import check_atlas, check_email_empty, check_string_list
from .common_dictionaries import (
    ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS,
    ATLAS_OCCURRENCES_ERROR_MESSAGES,
    ATLAS_SELECTIONS,
)
from .common_functions import print_if_verbose
from .galah_config import get_api_url, readConfig
from .galah_select import galah_select
from .show_all import show_all
from .version import __version__


def atlas_occurrences(
    taxa=None,
    scientific_name=None,
    filters=None,
    verbose=False,
    fields=None,
    use_data_profile=False,
    species_list=False,
    status_accepted=True,
    polygon=None,
    bbox=None,
    simplify_polygon=False,
    mint_doi=False,
    doi=None,
    config_file=None,
    tolerance=0.05,
):
    """
    The most common form of data stored by living atlases are observations of individual life forms, known as 'occurrences'.
    This function allows the user to search for occurrence records that match their specific criteria, and return them as a
    ``pandas.DataFrame`` for analysis. Optionally, the user can also request a DOI for a given download to facilitate
    citation and reuse of specific data resources.

    Parameters
    ----------
        taxa : string
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.
        filters : string / list
            filters, in the form ``field`` ``logical`` ``value`` (e.g. ``"year=2021"``)
        test : logical
            Test if the API is up and running correctly.  Prints status of Atlas and returns.
        verbose : logical
            If ``True``, galah gives more information like URLs of your queries. Defaults to ``False``
        fields : string / list
            Name of one or more column groups to include. Valid options are "basic", "event" and "assertions"
            Default is set to ``"fields=basic"``, which returns:

                - decimalLatitude, decimalLongitude, eventDate, scientificName, taxonConceptID, recordID, dataResourceName, occurrenceStatus

            Using ``"fields="event"`` returns:

                - eventRemarks, eventTime, eventID, eventDate, samplingEffort, samplingProtocol

            Using ``fields="media"`` returns:

                - multimedia, multimediaLicence, images, videos, sounds

            Using ``fields="assertions`` returns:

                - all available assertions from the ALA

            See ``galah.show_all()`` and ``galah.search_all()`` to see all valid fields.
        assertions : string / list
            Using "assertions" returns all quality assertion-related columns. These columns are data quality checks run by each living atlas. The list of assertions is shown by ``galah.show_all(assertions=True)``.
        use_data_profile : string
            A profile name. Should be a string - the name or abbreviation of a data quality profile to apply to the query. Valid values can be seen using ``galah.show_all(profiles=True)``
        species_list : logical
            Denotes whether or not you want a species list for GBIF.  Default to ``False``.  For species lists, refer to ``atlas_species``
        status_accepted : logical
            Denotes whether or not you want only accepted taxonomic ranks for GBIF.  Default to ``True``.  For species lists, refer to ``atlas_species``
        polygon : shapely Polygon
            A polygon shape denoting a geographical region.  Defaults to ``None``.
        bbox : dict or shapely Polygon
            A polygon or dictionary type denoting four points, which are the corners of a geographical region.  Defaults to ``None``.
        simplify_polygon : logical
            When using the ``polygon`` argument of ``galah.atlas_counts()``, specifies whether or not to draw a bounding box around the polygon and use this instead.  Defaults to ``True``.
        config_file : string
            If you want to specify your own config file, put the path and name of the file here.  This is applicable when you are running on a server and each user has different configurations.  Defaults to ``None``.

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    Download records of Vulpes vulpes in 2023

    .. prompt:: python

        import galah
        galah.galah_config(atlas="Australia",email="your-email@example.com")
        galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2023")

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);galah.galah_config(atlas=\\\"Australia\\\",email=\\\"amanda.buyan@csiro.au\\\");print(galah.atlas_occurrences(taxa=\\\"Vulpes vulpes\\\",filters=\\\"year=2023\\\"))"

    Download records of Vulpes vulpes in 2023, returning only ``eventDate`` field

    .. prompt:: python

        import galah
        galah.galah_config(atlas="Australia",email="your-email@example.com")
        galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2023",fields="eventDate")

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);galah.galah_config(atlas=\\\"Australia\\\",email=\\\"amanda.buyan@csiro.au\\\"); print(galah.atlas_occurrences(taxa=\\\"Vulpes vulpes\\\",filters=\\\"year=2023\\\",fields=\\\"eventDate\\\"))"

    """

    # get configs
    configs = readConfig(config_file=config_file)

    # get atlas
    atlas = configs["galahSettings"]["atlas"]

    # check atlas is valid
    check_atlas(atlas=atlas, function="atlas_occurrences")
    check_for_Portugal(atlas=atlas)

    # check for email
    check_email_empty()

    # check variables to see if they are strings/lists
    taxa = check_string_list(taxa, "taxa")
    filters = check_string_list(filters, "filters")

    # checks for fields
    if atlas not in ["Global", "GBIF"] and fields is None:
        fields = "basic"
    fields = check_string_list(fields, "fields")

    # check for Global atlas
    if atlas in ["Global", "GBIF"] and filters is not None:
        if "!=" in filters or "=!" in filters:
            raise ValueError("The current iteration of GBIF and galah does not support != as an option.")

    # for every atlas except for GBIF
    headers = {"User-Agent": "galah-python {}".format(__version__)}
    authentication = None

    if doi is not None:

        if atlas not in ["Australia", "Spain"]:
            raise ValueError("DOIs are only implemented for Australia and Spain.")

        # get URL
        baseURL, method = get_api_url(column1="called_by", column1value="doi_download", config_file=config_file)
        doi_string = doi.split("/")[-1]
        doi_string = doi_string.split(".")[-1]
        URL = baseURL.replace("{doi_string}", doi_string)

        # check for verbose argument
        print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

        # get data and return
        response = requests.request(method, URL)
        return pd.read_csv(
            zipfile.ZipFile(io.BytesIO(response.content)).open("data.csv"),
            sep=ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS[atlas]["separator"],
            low_memory=False,
        )

    if atlas in ["Global", "GBIF"]:

        URL, method = get_api_url(
            column1="called_by",
            column1value="atlas_occurrences",
            column2="api_name",
            column2value="records",
            config_file=config_file,
        )

        headers = {
            "User-Agent": "galah-python/{}".format(__version__),
            "X-USER-AGENT": "galah-python/{}".format(__version__),
            "Content-type": "application/json",
            "Accept": "application/json",
        }

        authentication = HTTPBasicAuth(
            configs["galahSettings"]["usernameGBIF"],
            configs["galahSettings"]["passwordGBIF"],
        )

        URL = add_question_mark(URL)

        URL = add_taxa(taxa=taxa, atlas=atlas, URL=URL, scientific_name=scientific_name)

        # GBIF takes predicates - initialise variable in case GBIF is their desired atlas
        predicates = add_predicates(predicates=[], filters=filters, occurrencesGBIF=True)

        if fields is not None:
            print(
                "GBIF, unfortunately, does not support choosing your desired data fields before download.  You will have to download them and then get categories you want."
            )

        # check if user wants species list
        if species_list:
            format = "SPECIES_LIST"
            if status_accepted:
                predicates.append(
                    {
                        "type": "equals",
                        "key": "TAXONOMIC_STATUS",
                        "value": "ACCEPTED",
                    }
                )
        else:
            format = "SIMPLE_CSV"

        # create payload
        payload = json.dumps(
            {
                "creator": configs["galahSettings"]["usernameGBIF"],  # username
                "notificationAddresses": [configs["galahSettings"]["email"]],  # change from hard-coded
                "sendNotification": "false",
                "format": format,
                "predicate": {"type": "and", "predicates": predicates},
            }
        )

        # check to see if user wants the query URL
        print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method, payload=payload)

        # get response
        response = requests.request(method, URL, headers=headers, auth=authentication, data=payload)

        # get job number
        job_number = response.text

        # make the download url
        statusURL = URL.replace("request", job_number)

        return get_data(
            response=response,
            atlas=atlas,
            statusURL=statusURL,
            authentication=authentication,
            headers=headers,
            verbose=verbose,
            filename="{}.csv".format(job_number),
            mint_doi=mint_doi,
        )

    else:

        URL, method = get_api_url(
            column1="called_by",
            column1value="atlas_occurrences",
            column2="api_name",
            column2value="records_occurrences",
            config_file=config_file,
        )

        URL = add_taxa(taxa=taxa, atlas=atlas, URL=URL, scientific_name=scientific_name)

        if URL is None:
            return None

        URL = add_filters(filters=filters, atlas=atlas, URL=URL)
        URL = add_spatial_shapes(
            polygon=polygon, bbox=bbox, URL=URL, simplify_polygon=simplify_polygon, tolerance=tolerance
        )

        # check for no filters
        var_list = [taxa, filters, polygon, bbox, scientific_name]
        check_for_no_filters(var_list=var_list, atlas=atlas)

        # add fields for the user to download
        URL = add_fields(fields=fields, atlas=atlas, URL=URL)

        # mint a DOI if requested
        if mint_doi:
            URL += "&mintDoi=TRUE"

        # check if a user wants to use a data profile
        # add other things to URL
        URL += "&dwcHeaders=True"

        # add last things to URL
        if atlas in ["Australia", "ALA"]:
            URL += add_extras_to_URL(
                add_email=True,
                use_data_profile=use_data_profile,
                data_profile_list=list(show_all(profiles=True)["shortName"]),
                atlas=atlas,
            )
        else:
            URL += add_extras_to_URL(add_email=True, atlas=atlas)

        # check to see if user wants the query URL
        print_if_verbose(verbose=verbose, headers=headers, URL=URL, method=method)

        # get the request
        response = requests.request(method, URL, headers=headers)

        # Austria returns zipfile from URL; have to return it straight away
        if atlas in ["Austria", "United Kingdom", "UK"]:
            return pd.read_csv(
                zipfile.ZipFile(io.BytesIO(response.content)).open("data.csv"),
                sep=ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS[atlas]["separator"],
                low_memory=False,
            )

        # get the data and return it to the user
        return get_data(
            response=response,
            atlas=atlas,
            statusURL=response.json()["statusUrl"],
            authentication=authentication,
            headers=headers,
            verbose=verbose,
            filename="data.csv",
            mint_doi=mint_doi,
        )


def add_question_mark(URL=None):
    if URL[-1] != "?":
        URL += "?"
    return URL


def get_data(
    response=None,
    atlas=None,
    statusURL=None,
    authentication=None,
    headers=None,
    verbose=None,
    filename=None,
    mint_doi=None,
):

    # check to see if the user has gotten a 403 error
    check_for_403_error(response=response, atlas=atlas)

    # check status of download
    response_download = requests.get(statusURL, headers=headers, auth=authentication)
    while response_download.json()["status"] != ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS[atlas]["finished_status"]:
        time.sleep(5)
        print("still working....")
        response_download = requests.get(statusURL, headers=headers, auth=authentication)
        print(response_download.json()["status"])
    zipURL = response_download.json()[ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS[atlas]["zipURL_arg"]]
    print(response_download.json())
    print(zipURL)

    # check to see if the user wants the zip URL
    print_if_verbose(verbose=verbose, headers=headers, URL=zipURL, method="GET")

    # return dataFrame
    data = requests.get(zipURL, headers=headers)

    if mint_doi:
        zip = zipfile.ZipFile(io.BytesIO(data.content))
        text = zip.read("doi.txt").decode().strip()
        print("DOI:\n")
        print("\t{}\n".format(text))

    # return dataframe
    return pd.read_csv(
        zipfile.ZipFile(io.BytesIO(data.content)).open(filename),
        sep=ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS[atlas]["separator"],
        low_memory=False,
    )


def add_fields(fields=None, atlas=None, URL=None):
    # add fields
    if fields is not None:
        # first, check for assertions
        if "assertions" in fields:
            URL += "&qa=includeall"
        else:
            URL += "&qa=none"

        # check for the "basic" flag
        URL += "&" + galah_select(select=fields)
    else:
        URL += "&qa=none&" + galah_select(select=ATLAS_SELECTIONS[atlas])

    return URL


def check_for_Portugal(atlas=None):
    if atlas in ["Portugal"]:
        raise ValueError("We currently cannot get occurrences from the {} atlas.".format(atlas))


def check_for_no_filters(var_list=None, atlas=None):
    # raise error if user hasn't specified any type of filters

    if all(v is None for v in var_list):
        raise Exception(
            "You cannot get all records for the {} atlas.  Please specify at least one taxa and/or filters to get occurrence records associated with the taxa.".format(
                atlas
            )
        )


def check_for_403_error(response=None, atlas=None):
    if response.status_code == 403:
        print(response.text)
        raise ValueError(
            "It appears that you are not registered as a user on the {} atlas.  Please {}".format(
                atlas, ATLAS_OCCURRENCES_ERROR_MESSAGES[atlas]
            )
        )
