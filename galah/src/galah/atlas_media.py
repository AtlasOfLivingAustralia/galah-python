import requests,os
import pandas as pd
import json
from tqdm import tqdm

from .atlas_occurrences import atlas_occurrences
from .get_api_url import get_api_url
from .get_api_url import readConfig
from .apply_data_profile import apply_data_profile
from .atlas_occurrences import atlas_occurrences
from .show_all import show_all
from .common_functions import write_image_to_file
from .version import __version__

# this function parses everything to atlas_occurrences first, and it adds something to the galah_filter argument to say
# that the multimedia field is not empty
# then, gets the multimedia column, which contains unique identifiers for media files
# then, hits different API and gets metadata of media
# next step is collect_media hits all URLs and drops it into my machine
def atlas_media(taxa=None,
                scientific_name=None,
                filters=None,
                fields=None,
                verbose=False,
                multimedia=None,
                assertions=None,
                use_data_profile=False,
                polygon=None,
                bbox=None,
                simplify_polygon=False,
                collect=False,
                path=None,
                thumbnail=False,
                progress_bar=True
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
        polygon : shapely Polygon
            A polygon shape denoting a geographical region.  Defaults to ``None``.
        bbox : dict or shapely Polygon
            A polygon or dictionary type denoting four points, which are the corners of a geographical region.  Defaults to ``None``.        
        simplify_polygon : logical
            When using the ``polygon`` argument of ``galah.atlas_counts()``, specifies whether or not to draw a bounding box around the polygon and use this instead.  Defaults to ``False``.
        collect : logical
            if ``True``, downloads full-sized images and media files returned to a local directory.
        path : string
            path to directory where downloaded media will be stored.  Defaults to current directory.
        thumbnail : logical
            if ``True``, downloads thumbnail images rather than the full image. Defaults to ``False``.
        progress_bar : logical
            if ``True``, shows a progress bar while images are downloading.  Defaults to ``True``.

    Returns
    -------
        An object of class ``pandas.DataFrame``. If ``collect=True``, available image & media files are downloaded to a user local directory.

    Examples
    --------

    .. prompt:: python

        galah.galah_config(atlas="Australia",email="youremail@example.com")
        galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=["year=2020","decimalLongitude>153.0")

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);galah.galah_config(email=\\\"ala4r@ala.org.au\\\");print(galah.atlas_media(taxa=\\\"Ornithorhynchus anatinus\\\",filters=[\\\"year=2020\\\",\\\"decimalLongitude>153.0\\\"]))"
    
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas']

    # get headers
    headers = {"User-Agent": "galah-python/{}".format(__version__)}

    # check for fields
    if fields is None:
        fields = ["basic","media"]

    # get occurrence data from atlas_occurrences
    dataFrame = atlas_occurrences(taxa=taxa,filters=filters,fields=fields,assertions=assertions,
                                  use_data_profile=use_data_profile,polygon=polygon,bbox=bbox,
                                  simplify_polygon=simplify_polygon,verbose=verbose,
                                  scientific_name=scientific_name)
    if dataFrame.empty:
        raise ValueError("There are no occurrences or media associated with your query.  Please try your query on atlas_counts before trying it again on atlas_media.")

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
        if atlas == "Australia" and multimedia is None:
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

        # check to see which occurrence entries have 
        if not media_array.empty:

            # filter by NaNs
            filtered_media_array = media_array.loc[media_array[media].notnull(), ['decimalLatitude', 'decimalLongitude', 'eventDate', 
                                                                                  'scientificName', 'recordID','dataResourceName', 
                                                                                  'occurrenceStatus', 'multimedia', 'images','videos',
                                                                                  'sounds']]
            
            # put the longest strings (so the duplicates) at the end
            filtered_media_array = filtered_media_array.sort_values(by=media,key=lambda x: x.str.len())

            # reset the indices for better looping
            filtered_media_array = filtered_media_array.reset_index(drop=True)

            # get duplicate rows and top index
            duplicate_rows = filtered_media_array[filtered_media_array[media].astype(str).str.contains(" | ")]
            top_index = duplicate_rows.index[0]

            # split out all the images for each occurrence
            duplicate_dict = {k: [] for k in ['decimalLatitude', 'decimalLongitude', 'eventDate', 'scientificName', 'recordID',
                           'dataResourceName', 'occurrenceStatus', 'multimedia', 'images','videos','sounds']}
            for i,row in duplicate_rows.iterrows():
                m=row[media].split(" | ")
                for entry in m:
                    duplicate_dict[media].append(entry)
                    for name in ['decimalLatitude', 'decimalLongitude', 'eventDate', 'scientificName', 'recordID',
                           'dataResourceName', 'occurrenceStatus', 'multimedia', 'images','videos','sounds']:
                        if name not in media:
                            duplicate_dict[name].append(row[name])

            # insert the duplicate rows into the array (need to ensure that, in the case they aren't sequential, to take that into consideration)
            new_filtered_media_array = pd.concat([filtered_media_array.head(top_index),pd.DataFrame(duplicate_dict)]).reset_index(drop=True)
            response = requests.request(method,basemediaURL,data=json.dumps({"imageIds": new_filtered_media_array[media].to_list()}),headers=headers)
            
            # get metadata here
            response_json = response.json()
            media_metadata = {
                "images": [],
                "creator": [],
                "license": [],
                "mimetype": [],
                "width": [],
                "height": [],
                "imageUrl": []
            }
            keys = list(response_json['results'].keys())
            for key in keys:
                media_metadata["images"].append(key)
                metadata = response_json['results'][key]

                for term in ["creator","license","mimetype","width","height","imageUrl"]:
                    if term in metadata:
                        media_metadata[term].append(metadata[term])
                    else:
                        media_metadata[term].append(None)
            df_metadata = pd.DataFrame(media_metadata)
            media_metadata_df = pd.merge(new_filtered_media_array,df_metadata,left_on='images', right_on='images', how='left')

            # if you want to collect media, use this loop
            if collect:
                if path is None:
                    print("setting the path to your current directory...")
                    path="./"
                else:
                    if not os.path.exists(path):
                        os.mkdir(path)

                # loop over images - have progress bar if user wants it
                if progress_bar:

                    for i,image in tqdm(media_metadata_df.iterrows(),total=media_metadata_df.shape[0]):

                        write_image_to_file(image=image,headers=headers,path=path,thumbnail=thumbnail)
                
                else:

                    for i,image in media_metadata_df.iterrows():

                        write_image_to_file(image=image,headers=headers,path=path,thumbnail=thumbnail)

                # Let user know where media has been written to
                print("Media written to {}".format(path))

                # return pandas dataframe with metadata
                return media_metadata_df
            else:

                # return pandas dataframe with metadata
                return media_metadata_df