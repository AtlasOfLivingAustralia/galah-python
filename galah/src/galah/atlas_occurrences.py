import sys,requests,urllib.parse,time,zipfile,io,configparser,glob
import pandas as pd
from .galah_filter import galah_filter
from .galah_select import galah_select
from .search_taxa import search_taxa
from .get_api_url import get_api_url
from .show_all import show_all
from .get_api_url import readConfig

import os

'''
occurrences
------
get the records of specified specie(s), including latitude, longitude, year etc..  filters can be applied, such as year 
of occurrence.

arguments
---------
taxa: a string or a list of taxa to get the number of counts for 
         (example: "Vulpes vulpes" or ["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
filters: list of filters as a string or list
geolocate: [fill in when I write it]
test: boolean argument to test if the ALA is working
verbose: boolean argument used to get URLs used for the query

returns
------- 
dataFrame: a pandas dataframe containing the taxa name and records for that taxa.  

TODO
----
2. Test more filters available on the ALA
3. Write geolocate part of this function
4. Understand what doi is and implement it
5. Understand what doi is and implement it
'''
# def atlas_occurrences(request=None,
#                      identify=None,
#                      filters=None,
#                      geolocate=None,
#                      select=galah_select(group="basic"),
#                      mint_doi=False,
#                      doi=None,
#                      refresh_cache=False):

# geolocate=None,
def atlas_occurrences(taxa=None,
                      filters=None,
                      test=False,
                      verbose=False,
                      fields=None,
                      doi=False,
                      assertions=None,
                      ):

    # test to check if ALA is working
    requestURL = "{}?pageSize=0".format(get_api_url(column1='called_by',column1value='atlas_counts'))

    # check if the ALA is working - if not, let the user know
    response = requests.get(requestURL)
    try:
        response.raise_for_status()
        if test:
            return
    except requests.exceptions.HTTPError as e:
        print("The ALA might be down...")
        print("Error: " + str(e))
        sys.exit()

    # now, figure out how to formulate queries
    # q <== queries, i.e. q=rk_genus:Macropus; q = Macropus is a free text search
    # fq <== filters to be applied to the original query in form fq=INDEXEDFIELD:VALUE, i.e. fq=rank:kingdom

    # get base URL
    baseURL = "{}?".format(get_api_url(column1='called_by', column1value='atlas_occurrences',column2='api_name',column2value='records_occurrences'))

    # first, get configurations and check for configurations
    configs = readConfig()

    # email for querying
    if configs['galahSettings']['email'] is None:
        raise ValueError("You need to provide a valid email address for occurrences to be able to download data")

    # adding a few things to baseURL
    # TODO: refine this and make sure the user can specify all of these things
    if configs['galahSettings']['data_profile'].lower() == "none":
        baseURL += "disableAllQualityfilters=true"
    else:
        data_profile_list = list(show_all(profiles=True)['shortName'])
        if configs['galahSettings']['data_profile'] in data_profile_list:
            baseURL += "&qualityProfile={}".format(configs['galahSettings']['data_profile'])
        else:
            raise ValueError("The data quality profile you've chosen is not one of the ones used - run \n\n"
                             "profiles = galah.show_all(profiles=True)\n\n"
                             "and then type\n\n"
                             "profiles['shortName']\n\n"
                             "to get the names of the data quality profiles you can use.  If you don't want to use a data"
                             " quality profile, set it to None by typing the following:\n\n"
                             "galah.galah_config(data_profile=\"None\")")
    baseURL += "&email={}&dwcHeaders=True".format(configs['galahSettings']['email'])
    if configs['galahSettings']['email_notify'].lower() == "false":
        baseURL += "&emailNotify=false"
    elif configs['galahSettings']['email_notify'].lower() == "true":
        baseURL += "&emailNotify=True" # check if this is correct
    else:
        raise ValueError("email_notify option should be set to either True or False - please set that with "
                         "galah_config(email_notify=\"False\") or galah_config(email_notify=\"True\")")

    # removing all assertions (these would appear in caps)
    if assertions is not None:
        raise ValueError("Assertions is not coded at this point - Amanda needs to code it")
    baseURL += "&qa=none&"

    # implement galah.select - choose which columns you download
    # goes to the 'fields' argument in occurrence download (csv list, commas between)
    if fields is not None:
        baseURL += galah_select(fields) + "&"

    if filters is not None:
        baseURL += galah_filter(filters) + "&"

    # check if taxa is specified
    if taxa is not None:

        # check variable type
        if type(taxa) == list or type(taxa) is str:

            # make taxa a list for easier looping
            if type(taxa) is str:
                taxa=[taxa]

            # create empty dataFrame
            dataFrame = pd.DataFrame()

            # loop over all taxa and add data to it
            for name in taxa:

                # get taxon concept ID
                taxonConceptID = search_taxa(name)['taxonConceptID'][0]

                # generate the desired URL and get a response from the API
                URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
                response = requests.get(URL)

                # check to see if user wants the query URL
                if verbose:
                    print("URL for querying:\n\n{}\n".format(URL))

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
                #if doi:
                #    print(zipfile.ZipFile(io.BytesIO(zipURL.content)))
                #    print(io.BytesIO(zipURL.content))
                #    #print(zipURL.content)
                #    for z in zipfile.ZipFile(io.BytesIO(zipURL.content)):
                #        print(z)
                tempdf = pd.read_csv(zipfile.ZipFile(io.BytesIO(zipURL.content)).open('data.csv'),low_memory=False)

                # append the data onto one big dataFrame for returning
                dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

            # return the dataFrame
            return dataFrame

        # else, the user needs to specify the taxa in the correct format
        else:
            raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: taxa.taxa(\"Vulpes vulpes\")"
                        "\n         taxa.taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")
    else:
        raise Exception('You cannot get all 10 million records for the ALA.  Please specify at least one taxa and/or '
                        'filters to get occurrence records associated with the taxa.')

