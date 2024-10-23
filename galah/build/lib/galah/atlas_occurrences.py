import sys
import requests
import urllib.parse
import time
import zipfile
import io
import json
from requests.auth import HTTPBasicAuth
import pandas as pd
from .atlas_counts import atlas_counts
from .galah_filter import galah_filter
from .galah_select import galah_select
from .search_taxa import search_taxa
from .get_api_url import get_api_url, readConfig
from .apply_data_profile import apply_data_profile
from .galah_geolocate import galah_geolocate
from .common_dictionaries import ATLAS_KEYWORDS,ATLAS_SELECTIONS, atlases, ATLAS_OCCURRENCES_ERROR_MESSAGES
from .common_dictionaries import ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS
from .common_functions import add_filters,add_predicates,add_to_payload_ALA
from .show_all import show_all
from .version import __version__

def atlas_occurrences(taxa=None,
                      scientific_name=None,
                      filters=None,
                      test=False,
                      verbose=False,
                      fields=None,
                      assertions=None,
                      use_data_profile=False,
                      species_list=False,
                      status_accepted=True,
                      polygon=None,
                      bbox=None,
                      simplify_polygon=False,
                      mint_doi=False,
                      doi=None
                      ):
    """
    The most common form of data stored by living atlases are observations of individual life forms, known as 'occurrences'. 
    This function allows the user to search for occurrence records that match their specific criteria, and return them as a 
    ``pandas.DataFrame`` for analysis. Optionally, the user can also request a DOI for a given download to facilitate 
    citation and re-use of specific data resources.

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
            When using the ``polygon`` argument of ``galah.atlas_counts()``, specifies whether or not to draw a bounding box around the polygon and use this instead.  Defaults to ``False``.

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
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas']

    # check for email
    if configs["galahSettings"]["email"] is None or configs["galahSettings"]["email"] == "email@example.com":
        raise ValueError("Please provide an email for querying")

    # initialise headers
    if atlas in ["GBIF","Global"]:
        headers = {
            "User-Agent": "galah-python/{}".format(__version__),
            "X-USER-AGENT": "galah-python/{}".format(__version__),
            "Content-type": "application/json",
            "Accept": "application/json",
        }
    else:
        # get headers
        headers = {"User-Agent": "galah-python {}".format(__version__)}


    # initialise payload
    payload = {}

    # create authentication key
    if atlas in ["Global","GBIF"]:
        authentication = HTTPBasicAuth(configs['galahSettings']['usernameGBIF'],configs['galahSettings']['passwordGBIF'])
    else:
        authentication = None

    # test to check if atlas is working
    requestURL,method = get_api_url(column1='called_by',column1value='atlas_counts',column2="api_name",column2value="records_counts")
    requestURL += "?pageSize=0"

    # check if the atlas is working - if not, let the user know
    response = requests.request(method,requestURL,headers=headers)
    try:
        response.raise_for_status()
        if test:
            return
    except requests.exceptions.HTTPError as e:
        print("The {} atlas might be down...")
        print("Error: " + str(e))
        sys.exit()

    if doi is not None:

        # get URL
        baseURL,method = get_api_url(column1='called_by',column1value='doi_download')
        doi_string = doi.split('/')[-1]
        doi_string = doi_string.split('.')[-1]
        URL = baseURL.replace('{doi_string}',doi_string)

        # check for verbose argument
        if verbose:
            print()
            print("URL for result:{}".format(URL))
            print("method: {}".format(method))
            print()

        # get data and return
        response = requests.request(method,URL)
        return pd.read_csv(zipfile.ZipFile(io.BytesIO(response.content))
                        .open('data.csv'),sep=ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS[atlas]["separator"],
                        low_memory=False)
    else:

        # get base URL
        if use_data_profile and atlas not in ["Australia","ALA"]:
            raise ValueError("True and False are the only values accepted for data_profile, and the only atlas using a data \n"
                            "quality profile is Australia.  Your atlas and data profile is \n"
                            "set in your config file.  To set your default filter, find out what profiles are on offer:\n"
                            "profiles = galah.show_all(profiles=True)\n\n"
                            "and then type\n\n"
                            "profiles['shortName']\n\n"
                            "to get the names of the data quality profiles you can use.  To set a data profile, type\n" 
                            "galah.galah_config(data_profile=\"NAME FROM SHORTNAME HERE\")"
                            "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
                            "galah.galah_config(data_profile=\"None\")"
                            )
        else:
            # check for these atlases first
            if atlas in ["Australia","Austria","Brazil","France","Guatemala","Spain","Sweden"]: # added Guatemala
                baseURL, method = get_api_url(column1='called_by', column1value='atlas_occurrences',column2='api_name', 
                                            column2value='records_occurrences',add_email=True)
            elif atlas in ["Global","GBIF"]:
                URL,method = get_api_url(column1='called_by',column1value='atlas_occurrences',
                                        column2='api_name',column2value='records',add_email=False)
            else:
                raise ValueError("Atlas {} not taken into account".format(atlas))       

        # goes to the 'fields' argument in occurrence download (csv list, commas between)
        if atlas in ["Australia","ALA"]:
            pass
        elif fields is not None and atlas not in ["Global","GBIF","Australia","ALA"]:
            if fields != "basic":
                baseURL += galah_select(select=fields,atlas=atlas) + "&"
            else:
                baseURL += galah_select(select=ATLAS_SELECTIONS[atlas],atlas=atlas) + "&"
        elif fields is None and atlas in ["Sweden"]:
            baseURL += galah_select(select=ATLAS_SELECTIONS[atlas],atlas=atlas) + "&"
        elif atlas in ["Austria","Brazil","France","Spain","Guatemala"]:
            baseURL += galah_select(select=ATLAS_SELECTIONS[atlas],atlas=atlas) + "&"
        elif fields is not None and atlas in ["Global","GBIF"]:
            print("GBIF, unfortunately, does not support choosing your desired data fields before download.  You will have to download them and then get categories you want.")
        elif atlas in ["Global","GBIF"]:
            pass
        else:
            raise ValueError("We currently cannot get occurrences from the {} atlas.".format(atlas))

        # GBIF takes predicates - initialise variable in case GBIF is their desired atlas
        predicates = []

        if atlas in ["Australia","ALA"]:
            
            # check for assertions and lump them with filters, as filters takes care of these
            if filters is not None and assertions is not None:
                if type(assertions) is list:
                    filters += assertions
                else:
                    filters.append(assertions)
            elif filters is None and assertions is not None:
                filters=assertions

            # create payload
            payload = add_to_payload_ALA(payload=payload,atlas=atlas,taxa=taxa,filters=filters,polygon=polygon,
                                        bbox=bbox,simplify_polygon=simplify_polygon,scientific_name=scientific_name)
            
            # create the query id
            qid_URL, method2 = get_api_url(column1="api_name",column1value="occurrences_qid")
            qid = requests.request(method2,qid_URL,data=payload,headers=headers)
            
            # create the URL to grab your queryID and counts
            if use_data_profile:
                data_profile_list = list(show_all(profiles=True)['shortName'])
                baseURL = apply_data_profile(baseURL=baseURL,data_profile_list=data_profile_list)   

            # Add qa=None to not get any assertions 
            if fields is None:
                selected_fields = galah_select(select="basic",atlas=atlas)
                if mint_doi: 
                    URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&" + selected_fields + "&qa=none&flimit=-1&mintDoi=TRUE"
                else:
                    URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&" + selected_fields + "&qa=none&flimit=-1"
            elif fields == "all":
                if mint_doi:
                    URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&qa=none&flimit=-1&mintDoi=TRUE"
                else:
                    URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&qa=none&flimit=-1"
            else:
                # print("am I here?")
                if mint_doi:
                    URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&" + galah_select(select=fields,atlas=atlas) + "&qa=none&flimit=-1&mintDoi=TRUE"
                else:
                    URL = baseURL + "fq=%28qid%3A" + qid.text + "%29&" + galah_select(select=fields,atlas=atlas) + "&qa=none&flimit=-1"

            if verbose:
                print()
                print("headers: {}".format(headers))
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

        else:

            # check if taxa is specified
            if taxa is not None:

                # check variable type
                if type(taxa) == list or type(taxa) is str:

                    # make taxa a list for easier looping
                    if type(taxa) is str:
                        taxa=[taxa]

                    # get the taxonConceptID for taxa - first check for extant atlas
                    if atlas in atlases:
                        taxonConceptID = list(search_taxa(taxa)[ATLAS_KEYWORDS[atlas]])
                    else:
                        raise ValueError("Atlas {} is not taken into account".format(atlas))

                    # generate the desired URL and get a response from the API - add taxonConceptIDs to the URL
                    if atlas in ["Global","GBIF"]:
                        for tid in taxonConceptID:
                            predicates.append({"type":"equals","key":"TAXON_KEY","value":str(tid)})
                    else:
                        # remove & before fq
                        URL = baseURL + "fq=%28lsid%3A" + "%20OR%20lsid%3A".join(
                            urllib.parse.quote(str(tid)) for tid in taxonConceptID) + "%29"
                    
                # else, the user needs to specify the taxa in the correct format
                else:
                    raise TypeError("The taxa argument can only be a string or a list."
                                "\nExample: taxa.taxa(\"Vulpes vulpes\")"
                                "\n         taxa.taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")
            
            if filters is not None:

                if type(filters) is str or type(filters) is list:
                    if atlas in ["Global","GBIF"] and ("!=" in filters or "=!" in filters):
                        raise ValueError("The current iteration of GBIF and galah does not support != as an option.")
                    elif atlas in ["Global","GBIF"]:
                        predicates = add_predicates(predicates=predicates,filters=filters)
                    else:
                        if taxa is not None:
                            URL += "%20AND%20"
                        URL = add_filters(URL=URL,atlas=atlas,filters=filters)
                else:
                    raise ValueError("The filters argument needs to be either a string or a list")

            # take care of assertions
            if assertions is not None:

                # check type
                if type(assertions) is list or type(assertions) is str:
                    if type(assertions) is str:
                        assertions=[assertions]
                    if atlas in ["Global","GBIF"]:
                        predicates = add_predicates(predicates=predicates,filters=filters)
                    else:
                        for a in assertions:
                            URL += galah_filter(a) + "%20AND%20"
                            URL = URL[:-len("%20AND%20")] + "%29&qa=none&"
                else:
                    raise ValueError("Assertions needs to be a string or a list of strings, i.e. identificationIncorrect == TRUE")
            
            if polygon is not None or bbox is not None:
                URL += "&" + galah_geolocate(polygon=polygon,bbox=bbox,simplify_polygon=simplify_polygon)

            # raise error if user hasn't specified any type of filters
            if taxa is None and filters is None and assertions is None:
                raise Exception('You cannot get all records for the {} atlas.  Please specify at least one taxa and/or filters to get occurrence records associated with the taxa.'.format(atlas))
            
            # add final part of URL
            if atlas not in ["Global","GBIF"]:
                URL += "&qa=none&"

            # download the file after you get the URL
            if atlas in ["Global","GBIF"]:

                # check if user wants species list
                if species_list:
                    format="SPECIES_LIST"
                    if status_accepted:
                        predicates.append({"type": "equals","key":"TAXONOMIC_STATUS","value":"ACCEPTED"})
                else:
                    format="SIMPLE_CSV"

                # create payload
                payload = json.dumps({
                    "creator": configs['galahSettings']['usernameGBIF'], # username
                    "notificationAddresses": [configs['galahSettings']['email']], # change from hard-coded
                    "sendNotification": "false",
                    "format": format,
                    "predicate": {
                        "type": "and",
                        "predicates": predicates
                    }
                })

                # check to see if user wants the query URL
                if verbose:
                    print("URL for querying:\n\n{}\n".format(URL))
                    print("headers: {}\n".format(headers))
                    print("payload: \n\n{}\n".format(payload))

                # check counts
                counts = atlas_counts(taxa,filters=filters)
                if not species_list:
                    print("total records for occurrences: {}\n".format(counts['totalRecords'][0]))
                    if int(counts['totalRecords'][0]) > 101000:
                        raise ValueError("Your data request of {} is too large. \nThe maximum number of requests is 101,000.\nPlease filter your data and use atlas_counts() to get the counts to a reasonable number.".format(counts['totalRecords'][0]))
                
                # get response
                response = requests.request(method,URL,headers=headers,auth=authentication,data=payload)
                
            # else, get response from other APIs
            else:

                # check to see if user wants the query URL
                if verbose:
                    print("\nURL being queried:\n\n{}\n".format(URL))

                response = requests.request(method,URL,headers=headers)

        # query the api
        if response.status_code == 403:
            raise ValueError("It appears that you are not registered as a user on the {} atlas.  Please {}".format(
                atlas,
                ATLAS_OCCURRENCES_ERROR_MESSAGES[atlas]
            ))
        
        # raise an error if user has exceeded the limit of number of daily queries
        if response.status_code == 429:
            raise ValueError("You have reached the maximum number of daily queries for the ALA.")
        
        # this may take a while - occasionally check if status has changed
        if atlas in ["Global","GBIF"]:

            # get job number
            job_number = response.text

            # make the download url
            statusURL = URL.replace("request",job_number)

        else:

            statusURL = response.json()['statusUrl']

    # check status of download
    response_download = requests.get(statusURL,headers=headers,auth=authentication)
    while response_download.json()["status"] != ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS[atlas]["finished_status"]:
        time.sleep(5)
        response_download = requests.get(statusURL,headers=headers,auth=authentication)
    zipURL = response_download.json()[ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS[atlas]["zipURL_arg"]]

    # check to see if the user wants the zip URL
    if verbose:
        print("Data for download:\n\n{}\n".format(zipURL))

    # return dataFrame
    data = requests.get(zipURL,headers=headers)

    # check filename
    if atlas in ["Global","GBIF"]:
        filename = '{}.csv'.format(job_number)
    else:
        filename = 'data.csv'

    if mint_doi:
        zip = zipfile.ZipFile(io.BytesIO(data.content))
        text = zip.read('doi.txt').decode().strip()
        print("DOI:\n")
        print("\t{}\n".format(text))

    # return dataframe
    return pd.read_csv(zipfile.ZipFile(io.BytesIO(data.content))
                        .open(filename),sep=ATLAS_OCCURRENCES_DOWNLOAD_ARGUMENTS[atlas]["separator"],
                        low_memory=False)