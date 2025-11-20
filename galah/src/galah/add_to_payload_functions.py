import urllib

import geopandas as gpd
import shapely
from shapely import MultiPolygon, Polygon

from .common_dictionaries import ATLAS_KEYWORDS, atlases
from .galah_filter import galah_filter
from .galah_geolocate import galah_geolocate
from .search_taxa import search_taxa


def generate_list_taxonConceptIDs(taxa=None, scientific_name=None, atlas=None, verbose=None):
    """Function for getting more than one taxonConceptIDs"""

    if taxa is None and scientific_name is None:
        raise ValueError("Please provide either a taxa or scientific_name for this information")

    if atlas is None:
        raise ValueError("Please provide an atlas to this function")

    # change taxa into list for easier looping and check if type of variable is correct
    if scientific_name is not None:

        # check for correct dictionary
        lens = [None for i in range(len(scientific_name))]
        for i, key in enumerate(scientific_name):
            lens[i] = len(scientific_name[key])
        if len(set(lens)) > 1:
            raise ValueError(
                "Please provide a correctly formatted dictionary with scientific_name - you are missing one or more taxonomic keys."
            )
        keys = scientific_name.keys()
        for i in range(lens[0]):
            tempdf = search_taxa(scientific_name=dict({key: [scientific_name[key][i]] for key in keys}))
            if tempdf.empty:
                print("No taxon matches were found for {} in the selected atlas ({})".format(scientific_name, atlas))
                if len(scientific_name) == 1:
                    return None
                continue

    else:

        if type(taxa) is str:
            taxa = [taxa]
        elif type(taxa) is list:
            pass
        else:
            raise TypeError(
                "The taxa argument can only be a string or a list."
                '\nExample: galah.atlas_counts("Vulpes vulpes")'
                '\n         galah.atlas_counts["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])'
            )

        # get the number of records associated with each taxa
        for name in taxa:

            # create temporary dataframe for taxon id
            tempdf = search_taxa(taxa=name, verbose=verbose)

            # check if dataframe is empty - if so, return None; else, continue
            if tempdf.empty:
                print("No taxon matches were found for {} in the selected atlas ({})".format(name, atlas))
                if len(taxa) == 1:
                    return None
                continue

    # get the taxonConceptID for taxa while checking for extant atlas
    if atlas in atlases:
        if scientific_name is not None:
            taxonConceptID = list(search_taxa(scientific_name=scientific_name)[ATLAS_KEYWORDS[atlas]])
        else:
            taxonConceptID = list(search_taxa(taxa=taxa)[ATLAS_KEYWORDS[atlas]])
    else:
        raise ValueError("Atlas {} is not taken into account".format(atlas))

    # add taxon IDs to URL, but first check for GBIF
    if atlas in ["Global", "GBIF"]:

        # add using taxonKey
        # return taxonConceptID
        return "".join(["taxonKey={}&".format(urllib.parse.quote(str(tid))) for tid in taxonConceptID])

    # for Australia
    elif atlas in ["Australia", "ALA"]:

        # try adding %22
        return (
            "fq=%28lsid%3A%22"
            + "%22%20OR%20lsid%3A%22".join(urllib.parse.quote(str(tid)) for tid in taxonConceptID)
            + "%29"
        )

    else:

        return "fq=%28lsid%3A" + "%20OR%20lsid%3A".join(urllib.parse.quote(str(tid)) for tid in taxonConceptID) + "%29"


def add_to_payload_ALA(
    payload=None,
    atlas=None,
    taxa=None,
    scientific_name=None,
    filters=None,
    polygon=None,
    bbox=None,
    simplify_polygon=False,
):
    """Function for adding variables to the payload when we cache (post) data to the ALA"""

    if taxa is not None:
        taxa_list = generate_list_taxonConceptIDs(taxa=taxa, atlas=atlas)
        fq = [" OR ".join("lsid:{}".format(id) for id in taxa_list)]
        payload = add_individual_to_payload(payload=payload, fq=fq)

    if scientific_name is not None:
        taxa_list = generate_list_taxonConceptIDs(scientific_name=scientific_name, atlas=atlas)
        fq = [" OR ".join("lsid:{}".format(id) for id in taxa_list)]
        payload = add_individual_to_payload(payload=payload, fq=fq)

    if filters is not None:
        if isinstance(filters, str):
            filters = [filters]

        for f in filters:
            filters_check = galah_filter(f)
            if " AND " in filters_check:
                filters_check = filters_check.split(" AND ")
            payload = add_filter_to_payload(filters_check, payload=payload)

    if polygon is not None or bbox is not None:
        wkts = galah_geolocate(polygon=polygon, bbox=bbox, simplify_polygon=simplify_polygon)
        fq = [" OR ".join("lsid:{}".format(id) for id in taxa_list)]
        payload = add_individual_to_payload(payload=payload, wkt=wkts)

    return payload


def add_individual_to_payload(payload=None, fq=None, wkt=None):

    if fq is not None and "fq" not in payload:
        payload["fq"] = fq
    elif fq is not None:
        payload["fq"] += fq

    if wkt is not None and "wkt" not in payload:
        if isinstance(wkt, str):
            payload["wkt"] = [wkt]
        else:
            payload["wkt"] = wkt
    elif wkt is not None:
        if type(wkt) is str:
            payload["wkt"].append(wkt)
        else:
            payload["wkt"] += wkt

    return payload


def add_filter_to_payload(f, payload):
    """Checks for less than or greater than syntax and returns two strings"""
    if "fq" not in payload:
        if type(f) is list:
            payload["fq"] = f
        else:
            payload["fq"] = [f]
    else:
        if type(f) is list:
            for f in f:
                payload["fq"].append(f)
        else:
            payload["fq"].append(f)
    return payload


def add_buffer(polygon=None, bbox=None, buffer=None, crs_deg=4326, crs_meters=3577):
    """DEPRECATED? function to add buffer to shapefile"""

    if buffer is None:
        raise ValueError("You need to include a buffer with this function")

    # make sure buffer is in meters
    if buffer > 1000:
        raise ValueError(
            "Currently `galah-python` doesn't support buffers greater than 1000km.  Enter a number between 0 and 1000."
        )
    buffer = buffer * 1000

    if polygon is not None:

        # make sure polygon is the correct type
        if type(polygon) is str or type(polygon) is Polygon or type(polygon) is MultiPolygon:
            polygon_df = gpd.GeoDataFrame(
                {"name": "user_defined_polygon", "geometry": polygon},
                index=[0],
                crs="EPSG:{}".format(crs_deg),
            )
        else:
            raise ValueError("The polygon must be either of type string or type Polygon/MultiPolygon")

        # change Coordinate Reference System, add buffer, and change it back to
        polygon_meters = polygon_df.to_crs(crs_meters)
        polygon_meters_buffer = polygon_meters.buffer(buffer)
        polygon_buffer = polygon_meters_buffer.to_crs(crs_deg)

        # return the polygon
        return polygon_buffer[0]

    if bbox is not None:

        # make sure polygon is the correct type
        if type(bbox) is str or type(bbox) is dict or type(bbox) is Polygon or type(bbox) is MultiPolygon:
            if type(bbox) is dict:
                bbox = shapely.box(bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"])
            bbox_df = gpd.GeoDataFrame(
                {"name": "user_defined_bbox", "geometry": bbox},
                index=[0],
                crs="EPSG:{}".format(crs_deg),
            )
        else:
            raise ValueError("The polygon must be either of type string or type Polygon/MultiPolygon")

        # change Coordinate Reference System, add buffer, and change it back to
        bbox_meters = bbox_df.to_crs(crs_meters)
        bbox_meters_buffer = bbox_meters.buffer(buffer)
        bbox_buffer = bbox_meters_buffer.to_crs(crs_deg)

        # return the polygon
        return bbox_buffer[0]
