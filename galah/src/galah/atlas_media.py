import json
import os
import re
import shutil

import pandas as pd
import requests
from tqdm import tqdm

from .atlas_occurrences import atlas_occurrences
from .common_checks import check_atlas, check_for_non_working_atlases, check_string_list
from .common_dictionaries import FIELD_SELECTIONS, IMAGE_COLUMN_NAMES, IMAGE_MERGE_NAMES, IMAGE_NAMES, MM_EXTENSIONS
from .common_functions import print_if_verbose, set_bool_argument
from .galah_config import get_api_url, readConfig
from .version import __version__


def atlas_media(
    taxa=None,
    scientific_name=None,
    filters=None,
    fields=None,
    multimedia=None,
    use_data_profile=False,
    polygon=None,
    bbox=None,
    simplify_polygon=False,
    collect=False,
    path=None,
    thumbnail=False,
    progress_bar=True,
    config_file=None,
    mint_doi=False,
    doi=None,
    tolerance=0.05,
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
        config_file : string
            If you want to specify your own config file, put the path and name of the file here.  This is applicable when you are running on a server and each user has different configurations.  Defaults to ``None``.

    Returns
    -------
        An object of class ``pandas.DataFrame``. If ``collect=True``, available image & media files are downloaded to a user local directory.

    Examples
    --------

    .. prompt:: python

        galah.galah_config(atlas="Australia",email="youremail@example.com")
        galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=["year=2020","decimalLongitude>153.0")

    .. program-output:: python -c "import galah; import pandas as pd;pd.set_option('display.max_columns', None);galah.galah_config(atlas=\\\"Australia\\\",email=\\\"ala4r@ala.org.au\\\");print(galah.atlas_media(taxa=\\\"Ornithorhynchus anatinus\\\",filters=[\\\"year=2020\\\",\\\"decimalLongitude>153.0\\\"]))"

    """

    # get configs
    configs = readConfig(config_file=config_file)

    # get atlas
    atlas = configs["galahSettings"]["atlas"]
    timeout = int(configs["galahSettings"]["timeout"])
    verbose = set_bool_argument(arg=configs["galahSettings"]["verbose"], name_arg="verbose")
    authenticate = set_bool_argument(arg=configs["galahSettings"]["authenticate"], name_arg="authenticate")
    access_token = configs["galahSettings"]["access_token"]
    client_id = configs["galahSettings"]["client_id"]

    # check to see if atlas is in list of non-functioning atlases
    check_for_non_working_atlases(atlas=atlas)

    # check atlas is valid
    check_atlas(atlas=atlas, function="atlas_media")

    # check the type of filters
    filters = check_string_list(filters, "filters")

    # get headers
    headers = {
        "User-Agent": "galah-python/{}".format(__version__),
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    # check for fields
    if fields is None:
        if atlas in ["Kew"]:
            fields = ["basic", "multimedia", "images"] # try this
        elif atlas in ["Austria"]:
            fields = ["basic", "multimedia", "image_url"]
        else:
            fields = ["basic", "media"]

    # get multimedia fields
    multimedia = check_multimedia(multimedia=multimedia, atlas=atlas)

    if "basic" in fields:
        fields.remove("basic")
        fields += FIELD_SELECTIONS["basic"]
        if atlas in ["Austria", "Brazil"]:
            fields = ["data_resource" if x == "dataResourceName" else x for x in fields]

    if "media" in fields:
        fields.remove("media")
        fields += FIELD_SELECTIONS["media"]
        if atlas in ["Brazil"]:
            fields.remove("videos")

    # get occurrence data from atlas_occurrences
    dataFrame = atlas_occurrences(
        taxa=taxa,
        filters=filters,
        fields=fields,
        use_data_profile=use_data_profile,
        polygon=polygon,
        bbox=bbox,
        tolerance=tolerance,
        simplify_polygon=simplify_polygon,
        scientific_name=scientific_name,
        mint_doi=mint_doi,
        doi=doi,
        config_file=config_file,
    )

    if dataFrame.empty:
        raise ValueError(
            "There are no occurrences or media associated with your query.  Please try your query on atlas_counts before trying it again on atlas_media."
        )

    # loop through all possible media
    for media in multimedia:

        # get all occurrences with multimedia files
        if type(dataFrame[media][0]) is str:
            # remove all "None" entries; may have to update this with different atlases
            media_array = dataFrame.loc[~dataFrame[media].str.contains("None", case=True, na=False)]
        else:
            media_array = dataFrame[~dataFrame[media].isnull()]

        # get media metadata url
        if authenticate:
            basemediaURL, method = get_api_url(
                column1="api_name", column1value="image_bulk_metadata", config_file=config_file
            )

            # add authorization token and client id for authentication
            headers["Authorization"] = "Bearer {}".format(access_token)
            headers["client_id"] = client_id

        else:
            basemediaURL, method = get_api_url(
                column1="called_by", column1value="media_metadata", config_file=config_file
            )

        # check to see which occurrence entries have
        if not media_array.empty:

            # filter by NaNs
            filtered_media_array = media_array.loc[
                media_array[media].notnull(),
                fields,
            ]

            # put the longest strings (so the duplicates) at the end
            filtered_media_array = filtered_media_array.sort_values(by=media, key=lambda x: x.str.len())

            # reset the indices for better looping
            filtered_media_array = filtered_media_array.reset_index(drop=True)

            # get duplicate rows and top index
            duplicate_rows = filtered_media_array[
                filtered_media_array[media].astype(str).str.contains(r"[,|]", regex=True)
            ]  # try this

            if not duplicate_rows.empty:
                top_index = duplicate_rows.index[0]

                # split out all the images for each occurrence
                duplicate_dict = {k: [] for k in fields}
                duplicate_dict = get_duplicate_images(
                    duplicate_rows=duplicate_rows,
                    media=media,
                    fields=fields,
                    duplicate_dict=duplicate_dict,
                )

                # insert the duplicate rows into the array (need to ensure that, in the case they aren't sequential, to take that into consideration)
                filtered_media_array = pd.concat(
                    [filtered_media_array.head(top_index), pd.DataFrame(duplicate_dict)]
                ).reset_index(drop=True)

            # get image metadata
            media_metadata_df = get_image_metadata(
                new_filtered_media_array=filtered_media_array,
                media=media,
                atlas=atlas,
                basemediaURL=basemediaURL,
                method=method,
                headers=headers,
                timeout=timeout,
                authenticate=authenticate,
                verbose=verbose,
            )

            # if you want to collect media, use this loop
            if collect:

                download_media(
                    progress_bar=progress_bar,
                    media_metadata_df=media_metadata_df,
                    headers=headers,
                    thumbnail=thumbnail,
                    path=path,
                    timeout=timeout,
                    atlas=atlas,
                )

            # return pandas dataframe with metadata
            return media_metadata_df


def write_image_to_file(image=None, headers=None, path=None, thumbnail=False, timeout=600, atlas=None):

    # set extension variable
    ext = ""

    # replace extensions in mimetype with actual filenames
    if image["mimeType"] in MM_EXTENSIONS:
        ext = MM_EXTENSIONS[image["mimeType"]]
    else:
        raise ValueError("Extension {} is not in our list of extensions.".format(image["mimeType"]))

    # check if they want the thumbnail vs. original
    if thumbnail:
        data = requests.get(
            url=image["imageUrl"].replace("original", "thumbnail"), headers=headers, stream=True, timeout=timeout
        )
    else:
        data = requests.get(url=image["imageUrl"], headers=headers, stream=True, timeout=timeout)

    # write image to file
    with open("{}/{}.{}".format(path, image[IMAGE_MERGE_NAMES[atlas]], ext), "wb") as f:
        data.raw.decode_content = True
        shutil.copyfileobj(data.raw, f)


def check_multimedia(multimedia=None, atlas=None):
    # make an array for multimedia
    if multimedia is not None:
        if type(multimedia) is list or type(multimedia) is str:
            if type(multimedia) is str:
                multimedia = [multimedia]
        else:
            raise ValueError('multimedia argument should either be a string or a list, i.e. multimedia="images"')
    else:
        if (
            atlas in ["Australia", "Flanders", "Spain", "Sweden", "United Kingdom", "UK"] and multimedia is None
        ):  # try Spain here
            multimedia = ["images", "videos", "sounds"]
        elif atlas in ["Austria", "Kew"]:
            multimedia = ["multimedia"]
        elif atlas in ["Brazil"]:
            multimedia = ["images", "sounds"]  # videos
        else:
            raise ValueError("Atlas {} is not taken into account".format(atlas))

    return multimedia


def get_image_metadata(
    new_filtered_media_array=None,
    media=None,
    atlas=None,
    basemediaURL=None,
    method=None,
    headers=None,
    timeout=600,
    authenticate=False,
    verbose=False,
):

    # first, get dictionary ready
    metadata_keys = ["imageIdentifier", "creator", "license", "mimeType", "width", "height", "imageUrl"]
    media_metadata = {x: [] for x in metadata_keys}

    if authenticate:
        payload = {"imageIds": list(new_filtered_media_array["images"])}  # json.dumps()

        # uncomment for debugging purposes
        print_if_verbose(verbose=verbose, headers=headers, URL=basemediaURL, method=method, payload=payload)

        # send the request for image metadata
        response = requests.request(
            method=method, url=basemediaURL, headers=headers, timeout=timeout, data=json.dumps(payload)
        )

        # get metadata here
        response_json = response.json()
        if response_json["success"]:
            for id in response_json["results"]:
                for key in metadata_keys:
                    if key in response_json["results"][id].keys():
                        media_metadata[key].append(response_json["results"][id][key])
                    elif key == "imageIdentifier":
                        media_metadata["imageIdentifier"].append(response_json["results"][id]["imageId"])
                    elif key == "mimeType":
                        media_metadata["mimeType"].append(response_json["results"][id]["mimetype"])
                    else:
                        media_metadata[key].append("")

    else:
        # loop over data
        for i, row in new_filtered_media_array.iterrows():

            if "[" in row[IMAGE_COLUMN_NAMES[atlas]]:
                image = re.sub(r"[\[\"\([{})\]]", "", row[IMAGE_COLUMN_NAMES[atlas]])
                # try this
                new_filtered_media_array.at[i, IMAGE_COLUMN_NAMES[atlas]] = image
            else:
                image = row[IMAGE_COLUMN_NAMES[atlas]]

            # replace the imageID word with actual ID
            mediaURL = basemediaURL.replace("{" + IMAGE_NAMES[atlas] + "}", image)

            # uncomment for debugging purposes
            print_if_verbose(verbose=verbose, headers=headers, URL=mediaURL, method=method)

            # send the request for image metadata
            response = requests.request(method=method, url=mediaURL, headers=headers, timeout=timeout)

            # get metadata here
            response_json = response.json()

            if response_json["success"]:

                # go through metadata
                for key in metadata_keys:
                    if key in response_json:
                        media_metadata[key].append(response_json[key])
                    else:
                        media_metadata[key].append("")

            else:
                for key in media_metadata.keys():
                    if key == "imageIdentifier":
                        if atlas in ["Austria"]:
                            media_metadata[key].append(row["multimedia"])
                        else:
                            media_metadata[key].append(row["images"])
                    elif key == "imageUrl":
                        media_metadata[key].append(response_json["message"])
                    else:
                        media_metadata[key].append("")

    # now get the metadata into a dataframe and merge it with the filtered array
    df_metadata = pd.DataFrame(media_metadata)
    if atlas in ["Austria"]:
        df_metadata = df_metadata.rename(columns={"imageIdentifier": "image_url"})

    # print(list(new_filtered_media_array["images"]))
    df_metadata = df_metadata.rename(columns={"imageIdentifier": "images"})
    return pd.merge(
        new_filtered_media_array,
        df_metadata,
        left_on=IMAGE_MERGE_NAMES[atlas],
        right_on=IMAGE_MERGE_NAMES[atlas],
        how="left",
    )


def download_media(
    progress_bar=None, media_metadata_df=None, headers=None, thumbnail=None, path=None, timeout=600, atlas=None
):

    if path is None:
        print("setting the path to your current directory...")
        path = "./"
    else:
        if not os.path.exists(path):
            os.mkdir(path)

    # loop over images - have progress bar if user wants it
    if progress_bar:

        for i, image in tqdm(media_metadata_df.iterrows(), total=media_metadata_df.shape[0]):

            write_image_to_file(
                image=image, headers=headers, path=path, thumbnail=thumbnail, timeout=timeout, atlas=atlas
            )

    else:

        for i, image in media_metadata_df.iterrows():

            write_image_to_file(image=image, headers=headers, path=path, thumbnail=thumbnail)

    # Let user know where media has been written to
    print("Media written to {}".format(path))


def get_duplicate_images(duplicate_rows=None, media=None, duplicate_dict=None, fields=None):
    for i, row in duplicate_rows.iterrows():
        m = row[media].split(" | ")
        for entry in m:
            duplicate_dict[media].append(entry)
            for name in fields:
                if name not in media:
                    duplicate_dict[name].append(row[name])
