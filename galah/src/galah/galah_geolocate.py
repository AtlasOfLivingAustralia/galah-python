import urllib
import shapely
import shapely.wkt
from shapely.ops import unary_union
import pandas as pd
from shapely import Polygon,MultiPolygon
from .get_api_url import readConfig
import geopandas as gpd

def galah_geolocate(polygon=None,
                    bbox=None,
                    simplify_polygon=True):
    """
    Restrict results to those from a specified area. Areas can be specified as 
    either polygons or bounding boxes, depending on type.
    
    Parameters
    ----------
        polygon : string, polygon object
            one polygon used to search (can be file name or polygon object).
        bbox : list, string
            list containing [xmin, ymin, xmax, ymax] or a polygon object.

    Returns
    -------
        Either a string or a polygon object.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.search_taxa(taxa="Vulpes vulpes",polygon=)

    .. program-output:: python -c "import galah; print(galah.search_taxa(taxa=\\\"Vulpes vulpes\\\"))"
    """

    # get configs
    configs = readConfig()

    # get atlas
    atlas = configs['galahSettings']['atlas']

    # check for atlas first
    if atlas in ["Australia","ALA"]:

        if polygon is not None:

            if type(polygon) is str:
                if "POLYGON" not in polygon and "MULTIPOLYGON" not in polygon:
                    if "shp" not in polygon:
                        raise ValueError("Only a shape file or wkt should be passed to polygon")
                    else:
                        print("Amanda write this loop")
                if simplify_polygon:
                    polygon_shape = shapely.box(polygon.bounds)
                    return str(shapely.box(xmin=polygon_shape.bounds[0],xmax=polygon_shape.bounds[2],
                                          ymin=polygon_shape.bounds[1],ymax=polygon_shape.bounds[3]))
                return shapely.wkt.loads(polygon)
            elif type(polygon) is Polygon or MultiPolygon:
                if simplify_polygon:
                    return str(shapely.box(xmin=polygon.bounds[0],xmax=polygon.bounds[2],ymin=polygon.bounds[1],ymax=polygon.bounds[3]))
                return str(polygon)
            else:
                print(polygon)
                print(type(polygon))
                raise ValueError("The only types of variables geolocate takes are str and polygons")

        elif bbox is not None:

            if type(bbox) is dict:
                #xmin, ymin, xmax, ymax
                return str(shapely.box(xmin=bbox["xmin"],xmax=bbox["xmax"],ymin=bbox["ymin"],ymax=bbox["ymax"]))
            elif type(bbox) is Polygon or type(bbox) is MultiPolygon:
                bounds=list(bbox.bounds)
                new_bbox = shapely.box(bounds[0],bounds[1],bounds[2],bounds[3])
                return str(new_bbox)
            elif type(bbox) is pd.core.frame.DataFrame:
                return str(shapely.box(xmin=bbox["minx"][0],xmax=bbox["maxx"][0],ymin=bbox["miny"][0],ymax=bbox["maxy"][0]))
            else:
                print(bbox)
                print(type(bbox))
                raise ValueError("The only types of variables geolocate takes for bounding box are dicts and polygons")
            
    else:

        '''
        # bits of code to add to URL
        #polygon_string = ""
        #polygon_string += "wkt={}&".format(urllib.parse.quote(str(new_geom))) # geometry
        #polygon_string += "wkt={}&".format(urllib.parse.quote(str(p)))
        #return polygon_string              
        '''
        raise ValueError("Only the Australian atlas has a geolocate option for now.")