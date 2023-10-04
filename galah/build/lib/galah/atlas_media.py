import requests,os
import pandas as pd

from .atlas_occurrences import atlas_occurrences
from .get_api_url import get_api_url
from .get_api_url import readConfig
from .apply_data_profile import apply_data_profile
from .atlas_occurrences import atlas_occurrences
from .show_all import show_all

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
    In addition to text data describing individual occurrences and their attributes, ALA stores images, sounds and videos 
    associated with a given record. ``galah.atlas_media()`` displays metadata for any and all of the media types.

    Parameters
    ----------
        taxa : string / list
            one or more scientific names. Use ``galah.search_taxa()`` to search for valid scientific names.  
        filters : string / list
            filters, in the form ``field`` ``logical`` ``value`` (e.g. ``"year=2021"``)
        fields : string / list
            Name of one or more column groups to include. Valid options are "basic", "event" and "assertions"
            Default is set to ``"fields=basic"``, which returns:

                - decimalLatitude, decimalLongitude, eventDate, scientificName, taxonConceptID, recordID, dataResourceName, occurrenceStatus

            Using ``"fields="event"`` returns:

                - eventRemarks, eventTime, eventID, eventDate, samplingEffort, samplingProtocol

            Using ``fields="media"`` returns:

                - multimedia, multimediaLicence, images, videos, sounds

            See ``galah.show_all()`` and ``galah.search_all()`` to see all valid fields.
        verbose : logical
            If ``True``, galah gives more information like URLs queried. Defaults to ``False``
        multimedia : string / list
            This is for specifying what types of multimedia you would like, i.e "images".  Defaults to ['images','videos','sounds']
        assertions : string
            Using "assertions" returns all quality assertion-related columns. These columns are data quality checks run by each living atlas. The list of assertions is shown by ``galah.show_all(assertions=True)``.
        use_data_profile : logical
            if ``True``, uses data profile set in ``galah_config()``. Valid values can be seen using ``galah.show_all(profiles=True)``. Default is ``False``
        collect : logical
            if ``True``, downloads full-sized images and media files returned to a local directory.
        path : string
            path to directory where downloaded media will be stored.  Defaults to current directory.

    Returns
    -------
        An object of class ``pandas.DataFrame``. If ``collect=True``, available image & media files are downloaded to a user local directory.

    Examples
    --------

    .. prompt:: python

        galah.galah_config(atlas="Australia",email="youremail@example.com")
        galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=["year=2020","decimalLongitude>153.0")

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);galah.galah_config(atlas=\\\"Australia\\\",email=\\\"amanda.buyan@csiro.au\\\");print(galah.atlas_media(taxa=\\\"Ornithorhynchus anatinus\\\",filters=[\\\"year=2020\\\",\\\"decimalLongitude>153.0\\\"]))"
    
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas']

    headers = {}

    # check for fields
    if fields is None:
        fields = ["decimalLatitude", "decimalLongitude", "eventDate", "scientificName", "taxonConceptID", "recordID",
                  "dataResourceName", "occurrenceStatus", "multimedia", "multimedialicense", "images", "videos",
                  "sounds"]

    # get occurrence data from atlas_occurrences
    dataFrame = atlas_occurrences(taxa=taxa,filters=filters,fields=fields,assertions=assertions,
                                  use_data_profile=use_data_profile,verbose=verbose)
    if dataFrame.empty:
        raise ValueError("There are no occurrences or media associated with your query.  Please try your query on atlas_counts before trying it again on atlas_media.")

    #if atlas in ["Australia","ALA"]:
    #    headers = {"x-api-key": configs["galahSettings"]["ALA_API_key"]}
    #else:
    #    headers = {}

    # create the output data frame
    if atlas == "Australia":
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
    elif atlas == "Austria":
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
        raise ValueError("Atlas {} is not taken into account".format(atlas))

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
        if atlas == "Australia":
            multimedia=['images','videos','sounds']
        elif atlas == "Austria":
            multimedia = ['multimedia']
        else:
            raise ValueError("Atlas {} is not taken into account".format(atlas))

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
            data_profile_list = list(show_all(profiles=True)['shortName'])
            basemediaURL, method = get_api_url(column1='called_by', column1value='media_metadata')
            basemediaURL = apply_data_profile(baseURL=basemediaURL,data_profile_list=data_profile_list)
        elif not use_data_profile:
            basemediaURL, method = get_api_url(column1='called_by', column1value='media_metadata')
        else:
            raise ValueError("True and False are the only values accepted for data_profile.  Your data profile is \n"
                             "set in your config file.  To see valid data quality profiles, run:\n"
                             "profiles = galah.show_all(profiles=True)\n\n"
                             "and then type\n\n"
                             "profiles['shortName']\n\n"
                             "To set your data profile, type\n"
                             "galah.galah_config(data_profile=\"NAME FROM SHORTNAME HERE\")"
                             "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
                             "galah.galah_config(data_profile=\"None\")"
                             )

        if atlas == "Australia":
            columns_media=['decimalLatitude', 'decimalLongitude', 'eventDate', 'scientificName', 'recordID',
                           'dataResourceName', 'occurrenceStatus', 'multimedia']
        elif atlas == "Austria":
            columns_media=['decimalLatitude', 'decimalLongitude', 'eventDate', 'scientificName', 'recordID',
                           'occurrenceStatus', 'multimedia']
        else:
            raise ValueError("Atlas {} is not taken into account".format(atlas))

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
                        response = requests.request(method,URL,headers=headers)
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
            print("setting the path to your current directory...")
            path="./"
        else:
            if not os.path.exists(path):
                os.mkdir(path)
        for i,image in enumerate(image_urls):
            ext = image.split(".")[-1]
            if verbose:
                print("\nURL being queried:\n\n{}\n".format(image))
            response = requests.get(image,stream=True,headers=headers)
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