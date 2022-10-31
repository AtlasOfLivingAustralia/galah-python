import galah,requests,urllib.parse,configparser,os,time,zipfile,io,shutils,tempfile
import pandas as pd
from .atlas_occurrences import atlas_occurrences
from .search_taxa import search_taxa
from .galah_select import galah_select
from .galah_filter import galah_filter

import sys

def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

# this function parses everything to atlas_occurrences first, and it adds something to the galah_filter argument to say
# that the multimedia field is not empty
# then, gets the multimedia column, which contains unique identifiers for media files
# then, hits different API and gets metadata of media
# next step is collect_media hits all URLs and drops it into my machine
def atlas_media(taxa=None,
                filters=None,
                fields=None,
                verbose=False,
                multimedia=None,
                collect=False,
                path=None
                ):

    # make a call to atlas_occurrences???
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig()
    specific_atlas = atlaslist[atlaslist['atlas'] == configs['galahSettings']['atlas']]

    # download sound, images etc.
    media_rows = specific_atlas[specific_atlas['called_by'] == 'atlas_occurrences']
    index = media_rows[media_rows['called_by'] == "atlas_occurrences"].index[0]
    baseURL = "{}?".format(media_rows[media_rows['called_by'] == 'atlas_occurrences']['api_url'][index])

    # email for querying
    if configs['galahSettings']['email'] is None:
        raise ValueError("You need to provide a valid email address for occurrences to be able to download data")

    # adding a few things to baseURL
    # TODO: refine this and make sure the user can specify all of these things
    baseURL += "disableAllQualityfilters=true" #&fields=decimalLatitude%2CdecimalLongitude%2CeventDate%2CscientificName%2CtaxonConceptID%2CrecordID%2CdataResourceName&qa=nonesourceTypeId=2004&reasonTypeId=4"
    baseURL += "&email={}&dwcHeaders=True&emailNotify=false&".format(configs['galahSettings']['email'])
    #baseURL += urllib.parse.quote("fields=multimedia,") #,multimedialicence,images,videos,sounds)")
    # removing all assertions (these would appear in caps)
    baseURL += "qa=none&" #"&{}&".format(urllib.parse.quote("(multimedia:\"Image\" OR multimedia:\"Sound\" OR multimedia:\"Video\")"))
    # add media to fields, as they are column names

    # implement galah.select - choose which columns you download
    # goes to the 'fields' argument in occurrence download (csv list, commas between)
    if fields is not None:
        baseURL += galah_select(fields) + "&"
    else:
        fields = ["decimalLatitude", "decimalLongitude", "eventDate", "scientificName","taxonConceptID","recordID",
                  "dataResourceName","occurrenceStatus","multimedia", "multimedialicense", "images", "videos", "sounds"]
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
                tempdf = pd.read_csv(zipfile.ZipFile(io.BytesIO(zipURL.content)).open('data.csv'),low_memory=False)

                # append the data onto one big dataFrame for returning
                dataFrame = pd.concat([dataFrame,tempdf],ignore_index=True)

       # else, the user needs to specify the taxa in the correct format
        else:
            raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: taxa.taxa(\"Vulpes vulpes\")"
                        "\n         taxa.taxa([\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")
    else:
        raise Exception('You cannot get all 10 million records for the ALA.  Please specify at least one taxa and/or '
                        'filters to get occurrence records associated with the taxa.')

    # create the output data frame
    data_columns={
        'decimalLatitude': [],
        'decimalLongitude': [],
        'eventDate': [],
        'scientificName': [],
        'recordID': [],
        'dataResourceName': [],
        'occurrenceStatus': [],
        'multimedia': [],
        'imageIdentifier': [],
        'mimeType': [],
        'sizeInBytes': [],
        'dateUploaded': [],
        'dateTaken': [],
        'height': [],
        'width': [],
        'creator': [],
        'license': [],
        'dataResourceUid': [],
        'occurrenceID': []
        }

    # for if the user wants to collect the urls
    image_urls=[]

    # make an array for multimedia
    if multimedia is not None:
        if type(multimedia) is list or type(multimedia) is str:
            if type(multimedia) is str:
                multimedia = [multimedia]
        else:
            raise ValueError("multimedia argument should either be a string or a list, i.e. multimedia=\"images\"")
    else:
        multimedia=['images','videos','sounds']

    # loop through all possible media
    for media in multimedia:

        # get all occurrences with multimedia files
        media_array = dataFrame[~dataFrame[media].isnull()]

        # get media metadata url
        # https://images.ala.org.au/ws#/Image%20metadata/getImageInfoForIdList
        media_rows = specific_atlas[specific_atlas['called_by'] == 'media_metadata']
        index = media_rows[media_rows['called_by'] == "media_metadata"].index[0]
        basemediaURL = media_rows[media_rows['called_by'] == 'media_metadata']['api_url'][index]

        # loop over arrays
        ### TODO: figure out how to make this faster?
        if not media_array.empty:
            for i,m in enumerate(media_array[media]):
                if "|" in m:
                    m=m.split(" | ")
                else:
                    m=[m]
                for j,entry in enumerate(m):
                    for e in ['decimalLatitude', 'decimalLongitude', 'eventDate', 'scientificName', 'recordID',
                             'dataResourceName', 'occurrenceStatus', 'multimedia']:
                        data_columns[e].append(media_array[e].iloc[i])
                    URL = basemediaURL.replace("{id}",entry)
                    response = requests.get(URL)
                    temp_dict = {k: [float("nan")] if not v else [v] for k, v in response.json().items()}
                    if collect:
                        #print(temp_dict['originalFileName'])
                        #print(temp_dict['source'])
                        #print(temp_dict['imageUrl'])
                        image_urls.append(temp_dict['originalFileName'][0])
                    for entry in ['imageIdentifier','mimeType', 'sizeInBytes', 'dateUploaded', 'dateTaken','height',
                                          'width','creator','license','dataResourceUid','occurrenceID']:
                        if entry not in temp_dict:
                            data_columns[entry].append(float("nan"))
                        else:
                            data_columns[entry].append(temp_dict[entry][0])

    # third, if option is true, collect data
    if collect:
        if path is None:
            # need to actually read about how to cache files
            tfd, tfname = tempfile.mkstemp(
                prefix='image-'.format(path,data_columns['imageIdentifier'][i],ext),
                suffix='.tif',
            )
            raise ValueError("The default path isn't currently set - please provide a path name")
        else:
            if not os.path.exists(path):
                os.mkdir(path)
        for i,image in enumerate(image_urls):
            ext = image.split(".")[-1]
            response = requests.get(image,stream=True)
            if response.status_code == 200:
                f = open("{}/image-{}.{}".format(path,data_columns['imageIdentifier'][i],ext), 'wb')
                f.write(response.content)
                f.close()
            else:
                print("Image {} couldn't be retrieved".format(image))
        print("Media written to {}".format(path))
        return pd.DataFrame.from_dict(data_columns)
    else:
        #return image metadata
        return pd.DataFrame.from_dict(data_columns)