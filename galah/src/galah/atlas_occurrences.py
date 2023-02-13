import sys,requests,urllib.parse,time,zipfile,io
import pandas as pd
from .galah_filter import galah_filter
from .galah_select import galah_select
from .search_taxa import search_taxa
from .get_api_url import get_api_url, readConfig
from .apply_data_profile import apply_data_profile

ATLAS_KEYWORDS = {
    "Australia": "taxonConceptID",
    "Austria": "guid",
    "Brazil": "guid", #speciesGuid
    "Canada": "usageKey",
    "Estonia": "guid",
    "France": "usageKey",
    "Guatemala": "guid",
    "Portugal": "usageKey",
    "Spain": "taxonConceptID",
    "Sweden": "guid",
    "United Kingdom": "guid",
}

ATLAS_SELECTIONS = {
    "Australia": ["decimalLatitude","decimalLongitude","eventDate","scientificName",
                 "taxonConceptID","recordID","dataResourceName","occurrenceStatus"],
    "Austria": [],
    "Brazil": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Canada": [],
    "Estonia": [],
    "France": [],
    "Guatemala": [],
    "Portugal": [],
    "Spain": ["latitude","longitude","occurrence_date","taxon_name","common_name",
                "taxon_concept_lsid","occurrence_id","data_resource_uid","occurrence_status"],
    "Sweden": [],
    "United Kingdom": [],
}

#atlases = ["Australia","Austria","Brazil","Canada","Estonia","France","Guatemala","Portugal","Sweden","Spain","United Kingdom"]

atlases = ["Australia","Brazil","Spain"]

def atlas_occurrences(taxa=None,
                      filters=None,
                      test=False,
                      verbose=False,
                      fields=None,
                      assertions=None,
                      use_data_profile=False,
                      ):
    """
    Used for getting occurrence data for your species.  To get occurrences for

    To know how many total records are in your chosen atlas, type

    .. prompt:: python

        import galah
        galah.atlas_occurrences(taxa="Vulpes vulpes")

    which returns

    .. program-output:: python3 -c "import galah; print(galah.atlas_occurrences(taxa=\\\"Vulpes vulpes\\\"))"
    """

    # get configs
    configs = readConfig()

    # test to check if ALA is working
    requestURL = "{}?pageSize=0".format(get_api_url(column1='called_by',column1value='atlas_counts',column2="api_name",
                                                    column2value="records_counts"))

    # check if the ALA is working - if not, let the user know
    response = requests.get(requestURL)
    try:
        response.raise_for_status()
        if test:
            return
    except requests.exceptions.HTTPError as e:
        print("The Atlas might be down...")
        print("Error: " + str(e))
        sys.exit()

    # now, figure out how to formulate queries
    # q <== queries, i.e. q=rk_genus:Macropus; q = Macropus is a free text search
    # fq <== filters to be applied to the original query in form fq=INDEXEDFIELD:VALUE, i.e. fq=rank:kingdom

    # get base URL
    if use_data_profile and configs['galahSettings']['atlas'] == "Australia":
        baseURL = apply_data_profile("{}".format(get_api_url(column1='called_by', column1value='atlas_occurrences',
                                                              column2='api_name',column2value='records_occurrences',
                                                              add_email=True)))
    elif not use_data_profile:
        # check for these atlases
        if configs['galahSettings']['atlas'] in ["Australia","Austria","Brazil","Guatemala","Spain","Sweden","United Kingdom"]:
            baseURL = "{}disableAllQualityfilters=true&".format(get_api_url(column1='called_by', column1value='atlas_occurrences',
                                                                 column2='api_name', column2value='records_occurrences',
                                                                 add_email=True))
        elif configs['galahSettings']['atlas'] in ["Estonia"]:
            baseURL = "{}disableAllQualityfilters=true&".format(get_api_url(column1='called_by',
                                                                                column1value='atlas_occurrences',
                                                                                column2='api_name',
                                                                                column2value='records',
                                                                                add_email=True))
        elif configs['galahSettings']['atlas'] in ["France","Portugal"]:
            baseURL = "{}disableAllQualityfilters=true&".format(get_api_url(column1='called_by',
                                                                                column1value='atlas_occurrences',
                                                                                column2='api_name',
                                                                                column2value='records_query',
                                                                                add_email=True))
        else:
            raise ValueError("Atlas {} not taken into account".format(configs['galahSettings']['atlas']))
    else:
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

    # removing all assertions (these would appear in caps)
    if assertions is not None:
        raise ValueError("Assertions is not coded at this point - Amanda needs to code it")
    baseURL += "&qa=none&"

    # implement galah.select - choose which columns you download
    # goes to the 'fields' argument in occurrence download (csv list, commas between)
    if fields is not None:
        baseURL += galah_select(selectionList=fields) + "&"
    elif configs['galahSettings']['atlas'] in ["Australia","Brazil"]:
        baseURL += galah_select(selectionList=ATLAS_SELECTIONS[configs['galahSettings']['atlas']])
    else:
        raise ValueError("We currently cannot get occurrences from the {} atlas.".format(configs['galahSettings']['atlas']))

    # check if taxa is specified
    if taxa is not None:

        # check variable type
        if type(taxa) == list or type(taxa) is str:

            # make taxa a list for easier looping
            if type(taxa) is str:
                taxa=[taxa]

            # create empty dataFrame
            dataFrame = pd.DataFrame()

            # get the taxonConceptID for taxa - first check for extant atlas
            if configs['galahSettings']['atlas'] in atlases:
                taxonConceptID = list(search_taxa(taxa)[ATLAS_KEYWORDS[configs['galahSettings']['atlas']]])
            else:
                raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

            # generate the desired URL and get a response from the API - add taxonConceptIDs to the URL
            URL = baseURL + "&fq=%28lsid%3A" + "%20OR%20lsid%3A".join(
                urllib.parse.quote(str(tid)) for tid in taxonConceptID) + "%29"

            # check what type of variable filters is; handle accordingly
            if filters is not None:
                URL += "%20AND%20%28"
                if type(filters) is str:
                    URL += galah_filter(filters) + "%20AND%20"
                elif type(filters) is list:
                    for f in filters:
                        URL += galah_filter(f) + "%20AND%20"
                else:
                    raise ValueError("The filters argument needs to be either a string or a list")

                # add final part of URL
                URL = URL[:-len("%20AND%20")] + "%29&"

            # check to see if user wants the query URL
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))

            # query the api
            response = requests.get(URL)
            if response.status_code == 403:
                # TODO: write more exceptions to make sure contact details are ok
                if configs['galahSettings']['atlas'] == "Brazil":
                    raise ValueError("It appears that you are not registered as a user on the Brazilian atlas.  Please email X to register.")
            if response.json()['status'] == "skipped":
                raise ValueError(response.json()["error"])

            # this may take a while - occasionally check if status has changed
            statusURL = requests.get(response.json()['statusUrl'])
            while statusURL.json()['status'] == 'inQueue':
                time.sleep(5)
                statusURL = requests.get(response.json()['statusUrl'])
            while statusURL.json()['status'] == 'running':
                time.sleep(5)
                statusURL = requests.get(response.json()['statusUrl'])
            zipURL = requests.get(statusURL.json()['downloadUrl'])

            # check to see if the user wants the zip URL
            if verbose:
                print("Data for download:\n\n{}\n".format(statusURL.json()['downloadUrl']))

            # create a temporary dataFrame
            tempdf = pd.read_csv(zipfile.ZipFile(io.BytesIO(zipURL.content)).open('data.csv'),low_memory=False)

            # append the data onto one big dataFrame for returning
            return pd.concat([dataFrame,tempdf],ignore_index=True)

        # else, the user needs to specify the taxa in the correct format
        else:
            raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: taxa.taxa(\"Vulpes vulpes\")"
                        "\n         taxa.taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")
    else:
        raise Exception('You cannot get all 10 million records for the ALA.  Please specify at least one taxa and/or '
                        'filters to get occurrence records associated with the taxa.')

