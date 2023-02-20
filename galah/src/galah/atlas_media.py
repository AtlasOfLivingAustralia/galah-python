import requests,urllib.parse,os,time,zipfile,io,shutils,tempfile
import pandas as pd
import numpy as np

from .atlas_occurrences import atlas_occurrences
from .search_taxa import search_taxa
from .galah_select import galah_select
from .galah_filter import galah_filter
from .get_api_url import get_api_url
from .get_api_url import readConfig
from .apply_data_profile import apply_data_profile
from .atlas_occurrences import atlas_occurrences

import sys

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
                assertions=None,
                use_data_profile=False,
                collect=False,
                path=None,
                ):
    """
    Used for getting media, such as images, videos and sounds.  An example query (filtering to ensure a small
    nunber of results) is

    .. prompt:: python

        import galah
        filters = ["year=2020","decimalLongitude>153.0"]
        galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=filters)

    which returns

    .. program-output:: python -c "import galah; filters = [\\\"year=2020\\\",\\\"decimalLongitude>153.0\\\"];print(galah.atlas_media(taxa=\\\"Ornithorhynchus anatinus\\\",filters=filters))"
    """

    # get configs
    configs = readConfig()

    # check for fields
    if fields is None:
        fields = ["decimalLatitude", "decimalLongitude", "eventDate", "scientificName", "taxonConceptID", "recordID",
                  "dataResourceName", "occurrenceStatus", "multimedia", "multimedialicense", "images", "videos",
                  "sounds"]

    # get occurrence data from atlas_occurrences
    dataFrame = atlas_occurrences(taxa=taxa,filters=filters,fields=fields,assertions=assertions,
                                  use_data_profile=use_data_profile)

    # create the output data frame
    if configs['galahSettings']['atlas'] == "Australia":
        data_columns = {
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
    elif configs['galahSettings']['atlas'] == "Austria":
        data_columns = {
            'decimalLatitude': [],
            'decimalLongitude': [],
            'eventDate': [],
            'scientificName': [],
            'recordID': [],
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
    else:
        raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

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
        if configs['galahSettings']['atlas'] == "Australia":
            multimedia=['images','videos','sounds']
        elif configs['galahSettings']['atlas'] == "Austria":
            multimedia = ['multimedia']
        else:
            raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

    # loop through all possible media
    for media in multimedia:

        # get all occurrences with multimedia files
        if type(dataFrame[media][0]) is str:
            # remove all "None" entries; may have to update this with different atlases
            media_array = dataFrame.loc[~dataFrame[media].str.contains("None", case=True, na=False)]
        else:
            media_array = dataFrame[~dataFrame[media].isnull()]

        # get media metadata url
        # https://images.ala.org.au/ws#/Image%20metadata/getImageInfoForIdList
        if use_data_profile:
            basemediaURL = apply_data_profile("{}".format(get_api_url(column1='called_by', column1value='media_metadata')))
        elif not use_data_profile:
            basemediaURL = "{}".format(get_api_url(column1='called_by', column1value='media_metadata'))
        else:
            raise ValueError("True and False are the only values accepted for data_profile.  Your data profile is \n"
                             "set in your config file.  To set your default filter, find out what profiles are on offer:\n"
                             "profiles = galah.show_all(profiles=True)\n\n"
                             "and then type\n\n"
                             "profiles['shortName']\n\n"
                             "to get the names of the data quality profiles you can use.  To set a data profile, type\n"
                             "galah.galah_config(data_profile=\"NAME FROM SHORTNAME HERE\")"
                             "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
                             "galah.galah_config(data_profile=\"None\")"
                             )

        if configs['galahSettings']['atlas'] == "Australia":
            columns_media=['decimalLatitude', 'decimalLongitude', 'eventDate', 'scientificName', 'recordID',
                           'dataResourceName', 'occurrenceStatus', 'multimedia']
        elif configs['galahSettings']['atlas'] == "Austria":
            columns_media=['decimalLatitude', 'decimalLongitude', 'eventDate', 'scientificName', 'recordID',
                           'occurrenceStatus', 'multimedia']
        else:
            raise ValueError("Atlas {} is not taken into account".format(configs['galahSettings']['atlas']))

        # loop over arrays
        ### TODO: figure out how to make this faster?
        if not media_array.empty:
            for i,m in enumerate(media_array[media]):
                if type(m) is str:
                    if "|" in m:
                        m=m.split(" | ")
                    else:
                        m=[m]
                    for j,entry in enumerate(m):
                        for e in columns_media:
                            data_columns[e].append(media_array[e].iloc[i])
                        URL = basemediaURL.replace("{id}",entry)
                        if verbose:
                            print("URL for querying:\n\n{}\n".format(URL))
                        response = requests.get(URL)
                        temp_dict = {k: [float("nan")] if not v else [v] for k, v in response.json().items()}
                        if collect:
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
            #tfd, tfname = tempfile.mkstemp(
            #    prefix='image-'.format(path,data_columns['imageIdentifier'][i],ext),
            #    suffix='.tif',
            #)
            print("setting the path to your current directory...")
            path="./"
            #raise ValueError("The default path isn't currently set - please provide a path name")
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