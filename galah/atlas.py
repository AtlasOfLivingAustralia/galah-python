'''
This is a collection of the atlas functions from the R galah package

Each function has a description of what it does and what its arguments are
'''

# import necessary packages
import sys,requests,urllib.parse,time,zipfile,io
import pandas as pd
import galah.search as search
import galah.galah as ggalah

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
def occurrences(species=None,filter=None,geolocate=None,test=False,verbose=False):
    # request a link from the ALA website
    # also implement a try/catch loop to make sure that there is a filter applied to
    # HOW TO DO FACETS: LATER

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

    # base response -
    baseURL = "https://biocache-ws.ala.org.au/ws/occurrences/offline/download?"
    email = "amanda.buyan@csiro.au"
    # adding things to baseURL
    baseURL += "disableAllQualityFilters=true&fields=decimalLatitude%2CdecimalLongitude%2CeventDate%2CscientificName%2CtaxonConceptID%2CrecordID%2CdataResourceName&qa=none&emailNotify=false&sourceTypeId=2004&reasonTypeId=4"
    baseURL += "&email={}&dwcHeaders=True&".format(email)

    # check if species is specified
    if species is not None:
        # first test for one species
        if type(species) == str:
            taxonConceptID=search.taxa(species)['taxonConceptID'][1]
            URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))
            response = requests.get(URL)
            statusURL = requests.get(response.json()['statusUrl'])
            while statusURL.json()['status'] == 'inQueue':
                time.sleep(1)
                statusURL = requests.get(response.json()['statusUrl'])
            while statusURL.json()['status'] == 'running':
                time.sleep(5)
                statusURL = requests.get(response.json()['statusUrl'])
            zipURL = requests.get(statusURL.json()['downloadUrl'])
            if verbose:
                print("Data for download:\n\n{}\n".format(statusURL.json()['downloadUrl']))
            return pd.read_csv(zipfile.ZipFile(io.BytesIO(zipURL.content)).open('data.csv'))
        # if not string, then it's multiple species
        elif type(species) == list:
            dataFrame = pd.DataFrame()
            for name in species:
                taxonConceptID = search.taxa(name)['taxonConceptID'][1]
                URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
                response = requests.get(URL)
                if verbose:
                    print("URL for querying:\n\n{}\n".format(URL))
                statusURL = requests.get(response.json()['statusUrl'])
                while statusURL.json()['status'] == 'inQueue':
                    time.sleep(1)
                    statusURL = requests.get(response.json()['statusUrl'])
                while statusURL.json()['status'] == 'running':
                    time.sleep(5)
                    statusURL = requests.get(response.json()['statusUrl'])
                zipURL = requests.get(statusURL.json()['downloadUrl'])
                if verbose:
                    print("Data for download:\n\n{}\n".format(statusURL.json()['downloadUrl']))
                tempdf = pd.read_csv(zipfile.ZipFile(io.BytesIO(zipURL.content)).open('data.csv'))
                dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)
            return dataFrame
        else:
            # potentially Assertion error?
            raise Exception('You cannot get all 10 million records for the ALA.  Please specify at least one species and/or '
                            'filters to get occurrence records associated with the species.')

    # return dataframe
    return dataFrame

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
def counts(species=None,separate=False,verbose=False,filter=None,groups=None,expand=False):
    # example for filters: https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28year%3A2021%29&pageSize=0
    # do this

    # get the baseURL for getting total number of records
    baseURL = "https://biocache-ws.ala.org.au/ws/occurrence/search?"

    # if there is no species, assume you will get the total number of records in the ALA
    if species is None:
        # TODO: filters
        if groups is None:
            print("implement filters")
            print(filter)
            sys.exit()
            URL = baseURL + "pageSize=0"
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))
            response = requests.get(URL)
            # get the json
            json = response.json()
            # return total number of records for the species
            return pd.DataFrame({'totalRecords': [json['totalRecords']]})
        else:
            return ggalah.groupBy(baseURL,groups,filter,expand)
    # if there is a single species, get
    elif type(species) == str:
        # use search.taxa() first, and then get taxonConceptID and pass to URL
        taxonConceptID=search.taxa(species)['taxonConceptID'][1]
        # fq=(lsid:taxonConceptID)
        URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
        if filter is not None:
            URL += ggalah.filter(filter)
            sys.exit()
            URL = URL[:-2] + "&pageSize=0"
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))
            else:
                raise TypeError("Filters should only be a list, and are in the following format:\n\nfilter=[\'year:2020\']")
        # no filters, end the URL
        else:
            URL += "pageSize=0"
        if verbose:
            print("URL for querying:\n\n{}\n".format(URL))
        # query the API
        response = requests.get(URL)
        # get the json
        json = response.json()
        # return total number of records for the species
        #if groups is not None:
        #    return galah.groupBy(pd.DataFrame({'totalRecords': [json['totalRecords']]}),groups)
        return pd.DataFrame({'totalRecords': [json['totalRecords']]})
    # get counts for multiple species
    elif type(species) == list:
        totalRecords=0
        tempTotalRecords=[]
        # get the number of records associated with each species
        for name in species:
            taxonConceptID = search.taxa(name)['taxonConceptID'][1]
            URL = baseURL + "fq=%28lsid%3A" + urllib.parse.quote(taxonConceptID) + "%29&"
            if filter is not None:
                if type(filter) == list:
                    for f in filter:
                        parts = f.split(":")
                        parts[1] = '\"{}\"'.format(parts[1])
                        f2 = ":".join(parts)
                        # could be fq=(year:"2020")
                        URL += "fq=%28{}%29{}".format(urllib.parse.quote(f2), urllib.parse.quote("OR"))
                    URL = URL[:-2] + "&pageSize=0"
                else:
                    raise TypeError(
                        "Filters should only be a list, and are in the following format:\n\nfilter=[\'year:2020\']")
            # tell the API to get only counts
            else:
                URL += "pageSize=0"
            if verbose:
                print("URL for querying:\n\n{}\n".format(URL))
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
        return dataFrame
    # if the variable isn't a string or a list, raise an exception
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
