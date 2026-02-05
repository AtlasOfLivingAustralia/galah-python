import geopandas as gpd
import shapely
from shapely import MultiPolygon, Polygon

from .galah_filter import galah_filter
from .galah_geolocate import galah_geolocate
from .search_taxa import generate_list_taxonConceptIDs


def add_to_payload_ALA(
    payload=None,
    taxa=None,
    atlas=None,
    scientific_name=None,
    filters=None,
    polygon=None,
    bbox=None,
    simplify_polygon=False,
    authenticate=False,
):
    """Function for adding variables to the payload when we cache (post) data to the ALA"""

    if taxa is not None:
        taxa_list = generate_list_taxonConceptIDs(taxa=taxa, atlas=atlas, authenticate=authenticate)
        fq = [" OR ".join("lsid:{}".format(id) for id in taxa_list)]
        payload = add_individual_to_payload(payload=payload, fq=fq)

    if scientific_name is not None:
        taxa_list = generate_list_taxonConceptIDs(
            scientific_name=scientific_name, atlas=atlas, authenticate=authenticate
        )
        fq = [" OR ".join("lsid:{}".format(id) for id in taxa_list)]
        payload = add_individual_to_payload(payload=payload, fq=fq)

    if filters is not None:
        if isinstance(filters, str):
            filters = [filters]

        for f in filters:
            filters_check = galah_filter(f=f, authenticate=authenticate)
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
