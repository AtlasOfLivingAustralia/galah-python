import sys,requests,urllib.parse,time,zipfile,io,configparser,glob
import pandas as pd
from .galah_filter import galah_filter
from .galah_select import galah_select
from .galah_config import galah_config

import os

'''
for reading the configuration file to feed in email
'''
def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

'''
occurrences
------
get the records of specified specie(s), including latitude, longitude, year etc..  Filters can be applied, such as year 
of occurrence.

arguments
---------
species: a string or a list of species to get the number of counts for 
         (example: "Vulpes vulpes" or ["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
filter: list of filters as a string or list
geolocate: [fill in when I write it]
test: boolean argument to test if the ALA is working
verbose: boolean argument used to get URLs used for the query

returns
------- 
dataFrame: a pandas dataframe containing the species name and records for that species.  

TODO
----
2. Test more filters available on the ALA
3. Write geolocate part of this function
4. Understand what mint_doi is and implement it
5. Understand what doi is and implement it
'''
# def atlas_occurrences(request=None,
#                      identify=None,
#                      filter=None,
#                      geolocate=None,
#                      select=galah_select(group="basic"),
#                      mint_doi=False,
#                      doi=None,
#                      refresh_cache=False):
def atlas_occurrences(species=None,filters=None,geolocate=None,test=False,verbose=False,fields=None):

    # get some arguments for the configuration file
    configs=readConfig()

    # check if the ALA is working - if not, let the user know
    response = requests.get("https://biocache-ws.ala.org.au/ws/occurrences/search?pageSize=0")
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

    # base URL for queries
    baseURL = "https://biocache-ws.ala.org.au/ws/occurrences/offline/download?"

    # email for querying
    # TODO: make this an environmental/global variable the user can set
    if email is None:
        raise ValueError("You need to provide a valid email address for occurrences to be able to download data")

    # adding a few things to baseURL
    # TODO: refine this and make sure the user can specify all of these things
    baseURL += "disableAllQualityFilters=true" #&fields=decimalLatitude%2CdecimalLongitude%2CeventDate%2CscientificName%2CtaxonConceptID%2CrecordID%2CdataResourceName&qa=nonesourceTypeId=2004&reasonTypeId=4"
    baseURL += "&email={}&dwcHeaders=True&emailNotify=false".format(configs['galahSettings']['email'])
    # removing all assertions (these would appear in caps)
    baseURL += "&qa=none&"

    # implement galah.select - choose which columns you download
    # goes to the 'fields' argument in occurrence download (csv list, commas between)
    if fields is not None:
        baseURL += galah_select(fields) + "&"

    # check if species is specified
    if species is not None:

        # check variable type
        if type(species) == list or type(species) is str:

            # make species a list for easier looping
            if type(species) is str:
                species=[species]

            # create empty dataFrame
            dataFrame = pd.DataFrame()

            # loop over all species and add data to it
            for name in species:

                # get taxon concept ID
                taxonConceptID = search.taxa(name)['taxonConceptID'][0]

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
                tempdf = pd.read_csv(zipfile.ZipFile(io.BytesIO(zipURL.content)).open('data.csv'))

                # append the data onto one big dataFrame for returning
                dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

            # return the dataFrame
            return dataFrame

        # else, the user needs to specify the species in the correct format
        else:
            raise TypeError("The species argument can only be a string or a list."
                        "\nExample: species.taxa(\"Vulpes vulpes\")"
                        "\n         species.taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")
    else:
        raise Exception('You cannot get all 10 million records for the ALA.  Please specify at least one species and/or '
                        'filters to get occurrence records associated with the species.')

