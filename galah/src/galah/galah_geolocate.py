import pandas as pd
import shapely
import shapely.wkt
from shapely import MultiPolygon, Polygon

from .galah_config import readConfig


def galah_geolocate(polygon=None, bbox=None, simplify_polygon=False, tolerance=10000):
    """
    Restrict results to those from a specified area. Areas can be specified as
    either polygons or bounding boxes, depending on type.

    Parameters
    ----------
        polygon : string, polygon object
            one polygon used to search (can be file name or polygon object).
        bbox : list, string
            list containing [xmin, ymin, xmax, ymax] or a polygon object.
        simplify_polygon : logical
            True/False flag to tell {galah-python} whether to simplify your polygon
        tolerance : float
            float to determine how much the polygon should be simplified.  Default is 0.05.

    Returns
    -------
        Either a string or a polygon object.
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs["galahSettings"]["atlas"]

    # check for atlas first
    if atlas not in ["Australia", "ALA"]:

        raise ValueError("Only the Australian atlas has a geolocate option for now.")

    # now that we have only the australian atlas, check to see if we have a polygon
    if polygon is not None:

        if isinstance(polygon, str):
            if all(x not in polygon for x in ["POLYGON", "MULTIPOLYGON", "shp"]):
                raise ValueError("Only a shape file or wkt should be passed to polygon")
            polygon = check_simplify_polygon(
                simplify_polygon=simplify_polygon, shape=shapely.wkt.loads(polygon), tolerance=tolerance
            )
            return shapely.wkt.loads(polygon)
        elif isinstance(polygon, (Polygon, MultiPolygon)):
            polygon = check_simplify_polygon(simplify_polygon=simplify_polygon, shape=polygon, tolerance=tolerance)
            return str(polygon)
        else:
            raise ValueError("The only types of variables geolocate takes are str and polygons")

    # then, check to see if user has given a bounding box
    if bbox is not None:

        if isinstance(bbox, dict):
            # xmin, ymin, xmax, ymax
            return str(
                shapely.box(
                    xmin=bbox["xmin"],
                    xmax=bbox["xmax"],
                    ymin=bbox["ymin"],
                    ymax=bbox["ymax"],
                )
            )
        elif isinstance(bbox, (Polygon, MultiPolygon)):
            bounds = list(bbox.bounds)
            new_bbox = shapely.box(bounds[0], bounds[1], bounds[2], bounds[3])
            return str(new_bbox)
        elif isinstance(bbox, pd.core.frame.DataFrame):
            return str(
                shapely.box(
                    xmin=bbox["minx"][0],
                    xmax=bbox["maxx"][0],
                    ymin=bbox["miny"][0],
                    ymax=bbox["maxy"][0],
                )
            )
        else:
            raise ValueError("The only types of variables geolocate takes for bounding box are dicts and polygons")


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
        print(shapely.count_coordinates(shape))
        new_shape = shape.simplify(tolerance=tolerance)
        print(shapely.count_coordinates(new_shape))
        print()
        return str(shape.simplify(tolerance=tolerance))
    return shape
