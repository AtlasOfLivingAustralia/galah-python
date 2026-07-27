import geopandas as gpd
import pandas as pd
import shapely
import shapely.wkt
from shapely import MultiPolygon, Polygon

from .common_dictionaries import ATLAS_CRS
from .galah_config import check_atlas


def galah_geolocate(polygon=None, bbox=None, atlas=None, crs=None):
    """
    Restrict results to those from a specified area. Areas can be specified as
    either polygons or bounding boxes, depending on type.

    Parameters
    ----------
        polygon : string, polygon object, GeoPandas dataframe
            one polygon used to search (can be file name or polygon object).
        bbox : list, dict, GeoPandas dataframe
            list containing [xmin, ymin, xmax, ymax] or a polygon object.

    Returns
    -------
        Either a string or a polygon object.
    """

    # check for atlas first
    check_atlas(atlas=atlas, function="galah_geolocate")
    check_polygon_validity(polygon=polygon)
    check_bbox_validity(bbox=bbox)
    check_crs_specified(shape=polygon, crs=crs)
    check_crs_specified(shape=bbox, crs=crs)
    check_crs_validity(shape=polygon, crs=crs)
    check_crs_validity(shape=bbox, crs=crs)
    check_number_vertices(shape=polygon)

    # first, check if polygon is None
    if polygon is not None:

        if isinstance(polygon, str):
            return str(shapely.orient_polygons(shapely.wkt.loads(polygon)))
        elif isinstance(polygon, (Polygon, MultiPolygon)):
            return str(shapely.orient_polygons(polygon))
        elif isinstance(polygon, (gpd.GeoDataFrame, pd.DataFrame)):
            if "geometry" not in polygon.columns:
                raise ValueError("You need to provide a geometry column for polygon.")
            index = polygon["geometry"].index[0]
            return str(shapely.orient_polygons(polygon["geometry"][index]))
        else:
            raise ValueError(
                "You can only pass a string, a GeoDataFrame, a pandas dataframe or a Polygon/Multipolygon object for the polygon variable"
            )

    # then, check to see if user has given a bounding box
    if bbox is not None:

        if isinstance(bbox, dict):
            # xmin, ymin, xmax, ymax
            return str(
                shapely.orient_polygons(
                    shapely.box(
                        xmin=bbox["xmin"],
                        xmax=bbox["xmax"],
                        ymin=bbox["ymin"],
                        ymax=bbox["ymax"],
                    )
                )
            )
        elif isinstance(bbox, (Polygon, MultiPolygon)):
            bounds = list(bbox.bounds)
            new_bbox = shapely.box(bounds[0], bounds[1], bounds[2], bounds[3])
            return str(shapely.orient_polygons(new_bbox))
        elif isinstance(bbox, (gpd.GeoDataFrame, pd.DataFrame)):
            if "xmin" in bbox.columns:
                return str(
                    shapely.orient_polygons(
                        shapely.box(
                            xmin=bbox["xmin"][0],
                            xmax=bbox["xmax"][0],
                            ymin=bbox["ymin"][0],
                            ymax=bbox["ymax"][0],
                        )
                    )
                )
            else:
                return str(
                    shapely.orient_polygons(
                        shapely.box(
                            xmin=bbox["minx"][0],
                            xmax=bbox["maxx"][0],
                            ymin=bbox["miny"][0],
                            ymax=bbox["maxy"][0],
                        )
                    )
                )
        else:
            raise ValueError(
                "You can only pass a string, a GeoDataFrame or a Polygon/Multipolygon object for the bbox variable"
            )


def check_polygon_validity(polygon=None):

    # check the type of variable is correct
    if polygon is not None and not isinstance(
        polygon, (str, gpd.geodataframe.GeoDataFrame, pd.DataFrame, dict, Polygon, MultiPolygon)
    ):
        raise ValueError("The polygon must be of type str, GeoDataFrame, DataFrame, dict, Polygon, MultiPolygon")

    # first, check to make sure string is formatted properly
    if isinstance(polygon, str):
        if all(x not in polygon for x in ["POLYGON", "MULTIPOLYGON"]):
            raise ValueError("The string you passed needs to be a POLYGON or MULTIPOLYGON")

    # next, check to ensure person is only passing one shape at a time
    if isinstance(polygon, gpd.GeoDataFrame):
        indices = polygon["geometry"].index
        if len(indices) > 1:
            raise ValueError("You can only pass one polygon at a time")


def check_bbox_validity(bbox=None):

    # check if variable is correct
    if bbox is not None and not isinstance(bbox, (str, gpd.GeoDataFrame, pd.DataFrame, dict, Polygon, MultiPolygon)):
        raise ValueError("The polygon must be of type str, GeoDataFrame, DataFrame, dict, Polygon, MultiPolygon")

    # set terms to check
    dict_terms = ["xmin", "xmax", "ymin", "ymax"]
    second_dict_terms = ["minx", "maxx", "miny", "maxy"]

    # first, check for dict
    if isinstance(bbox, dict):
        if not all(x in bbox.keys() for x in dict_terms) and not all(x in bbox.keys() for x in second_dict_terms):
            raise ValueError(f"Please include the following terms in your bbox dict: \n{"\n".join(dict_terms)}\n")

    # then, check for GeoDataFrame
    if isinstance(bbox, (gpd.geodataframe.GeoDataFrame, pd.DataFrame)):
        if not all(x in bbox.columns for x in dict_terms) and not all(x in bbox.keys() for x in second_dict_terms):
            raise ValueError(f"Please include the following terms in your bbox dict: \n{"\n".join(dict_terms)}\n")


def check_crs_specified(shape=None, crs=None):
    if shape is not None:
        if not isinstance(shape, gpd.GeoDataFrame) and crs is None:
            print(
                "Warning: A Coordinate Reference System (CRS) is not detected.  Ensure a CRS is specified as an argument, or is part of the variable (i.e. GeoDataFrame.crs)"
            )


def check_crs_validity(shape=None, crs=None):
    if shape is not None:
        if isinstance(shape, gpd.GeoDataFrame):
            if shape.crs not in ATLAS_CRS and crs is None:
                print(
                    f"Warning: The Coordinate Reference System of all atlases is EPSG:4326 (WGS84).  The results from this shape may be incorrect, as its CRS is {shape.crs}"
                )
        elif crs is None:
            print(
                f"Warning: The Coordinate Reference System of all atlases is EPSG:4326 (WGS84).  The results from this shape may be incorrect, as its CRS is {crs}"
            )


def check_number_vertices(shape=None, authenticate=None):

    # if the person isn't authenticating, do this check
    if not authenticate and shape is not None:

        # first, get all the possible data formats and ensure you can get the number of vertices
        if isinstance(shape, (gpd.GeoDataFrame, pd.DataFrame)):
            print()
            if all(x not in shape.columns for x in ["xmin", "xmax", "ymin", "ymax", "geometry"]):
                raise ValueError(
                    'There needs to be either a "geometry" column associated with your shape, or for a bounding box, minx, maxx, miny, maxy.'
                )
            if "geometry" in shape.columns:
                index = shape["geometry"].index[0]
                shape_vertices = shape["geometry"][index]
            else:
                shape_vertices = shape.to_dict()
        elif isinstance(shape, (Polygon, MultiPolygon, str, shapely.box)):
            shape_vertices = shape
        elif isinstance(shape, dict):
            shape_vertices = shape.values()

        # get vertices
        vertices = str(shape_vertices).split(",")

        # check number of vertices
        if len(vertices) > 50:
            raise ValueError(
                "There are more than 50 vertices in your shape, which will throw an error when queried.  Draw a bounding box around your shape, then filter occurrences from the bounding box with that shape."
            )


# simplify_polygon : logical
#     True/False flag to tell {galah-python} whether to simplify your polygon
# tolerance : float
#     float to determine how much the polygon should be simplified.  Default is 0.05.
def check_simplify_polygon(simplify_polygon=False, shape=None, tolerance=10000):
    """
    This function checks to see if the user wants to simplify their polygon (and does so if directed).

    Parameters
    ----------
        shape : string, polygon object
            one polygon used to search (can be file name or polygon object).
        simplify_polygon : logical
            True/False flag to tell {galah-python} whether to simplify your polygon
        tolerance : float
            float to determine how much the polygon should be simplified.  Default is 0.15.

    Returns
    -------
        Either the simplified shape or original.
    """
    if simplify_polygon:
        return str(shape.simplify(tolerance=tolerance))
    return shape
