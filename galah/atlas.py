'''
This is a collection of the atlas functions from the R galah package

Each function has a description of what it does and what its arguments are
'''

# import necessary packages
import sys,requests,urllib.parse,time,zipfile,io
import pandas as pd
import galah.search as search
import galah.galah as ggalah
from galah.galah import filter

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
def occurrences(species=None,filters=None,geolocate=None,test=False,verbose=False):

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
    email = "amanda.buyan@csiro.au"

    # adding a few things to baseURL
    # TODO: refine this and make sure the user can specify all of these things
    baseURL += "disableAllQualityFilters=true&fields=decimalLatitude%2CdecimalLongitude%2CeventDate%2CscientificName%2CtaxonConceptID%2CrecordID%2CdataResourceName&qa=none&emailNotify=false&sourceTypeId=2004&reasonTypeId=4"
    baseURL += "&email={}&dwcHeaders=True&".format(email)

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

'''
counts
------
get the count of the number of records of specified specie(s).  Filters can be applied, such as year of occurrence.

arguments
---------
species: a string or a list of species to get the number of counts for 
         (example: "Vulpes vulpes" or ["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
separate: boolean argument used if the user wants separate counts when they are querying multiple species
verbose: boolean argument used to get URLs used for the query
filter: list of filters as text

returns
------- 
dataFrame: a pandas dataframe containing the species name and total number of records for that species.  Can be separated 
           into multiple species with the separate argument
           
TODO
----
1. Test more filters available on the ALA
'''
def counts(species=None,separate=False,verbose=False,filters=None,groups=None,expand=False):

    # get the baseURL for getting total number of records
    baseURL = "https://biocache-ws.ala.org.au/ws/occurrence/search?"

    # if there is no species, assume you will get the total number of records in the ALA
    if species is None:

        # check if groups exist
        if groups is None:

            # check if filters are specified
            if filters is not None:

                # check the type of variable filters is
                if type(filters) is list or type(filters) is str:

                    # change to list for easier looping
                    if type(filters) is str:
                        filters=[filters]

                    # loop over filters
                    for f in filters:
                        URL += "&" + filter(f)

                    # add the final part of the URL
                    URL += "&pageSize=0"

                # else, make sure that the filters is in the following format
                else:
                    raise TypeError(
                        "Filters should only be a list, and are in the following format:\n\nfilter=[\'year:2020\']")

            # else, add the final bit of the URL
            else:
                URL = baseURL + "pageSize=0"

            # check to see if the user wantw the querying URL
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))

            # get the response and data
            response = requests.get(URL)
            json = response.json()

            # return dataFrame with total number of records
            return pd.DataFrame({'totalRecords': [json['totalRecords']]})

        # else, the user wants a grouped dataFrame
        else:

            #return a grouped dataFrame
            return ggalah.groupBy(baseURL,groups,filters,expand)

    # if there is a single species, get
    elif type(species) is str or type(species) is list:

        # change species into list for easier looping
        if type(species) is str:
            species=[species]

        # set these variables to 0 and empty initially
        totalRecords=0
        tempTotalRecords=[]

        # get the number of records associated with each species
        for name in species:

            # get the taxonConceptID for species
            taxonConceptID = search.taxa(name)['taxonConceptID'][0]

            # add this ID to the URL
            URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"

            # check to see if filters exist
            if filters is not None:

                # check the type of variable filters is
                if type(filters) is list or type(filters) is str:

                    # change to list for easier looping
                    if type(filters) is str:
                        filters = [filters]

                    # loop over filters
                    for f in filters:
                        # TODO: implement "or"?
                        URL += "AND" + filter(f)

                    # add the final part of the URL
                    URL += "&pageSize=0"

                # else, make sure that the filters is in the following format
                else:
                    raise TypeError(
                        "Filters should only be a list, and are in the following format:\n\nfilter=[\'year:2020\']")

            # add the last bit of the URL
            else:
                URL += "pageSize=0"

            # check to see if the user wants the URL for querying
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))

            # get results form the URL
            response = requests.get(URL)
            json = response.json()

            # if the user wants them separated, add counts to a temporary array to make a dataframe with
            if separate:
                tempTotalRecords.append(int(json['totalRecords']))

            # if the user doesn't want them separate, then add them to the existing counts
            else:
                totalRecords += int(json['totalRecords'])

        # make a dataframe with the total records for each species separate
        if separate:
            dataFrame = pd.DataFrame({'Species': species, 'totalRecords': tempTotalRecords})

        # make a dataframe with the total number of records
        else:
            dataFrame = pd.DataFrame({'totalRecords': [totalRecords]})

        # return the dataFrame with the specified counts
        return dataFrame

    # if the species variable isn't a string or a list, raise an exception
    else:
        raise TypeError("The species argument can only be a string or a list."
                        "\nExample: atlas.counts(\"Vulpes vulpes\")"
                        "\n         atlas.counts[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")

'''
# this function does X
def species():
    # search taxonomic trees
    
# this function does X
def taxonomy():
    # search taxonomic trees

# this function does X    
def media():
    # download sound, images etc.

# this function does X    
def citation():
    # generate citation for occurrence data
'''
