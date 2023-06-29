import urllib
import shapely
import shapely.wkt
from shapely.geometry import box,shape
from shapely.geometry.polygon import Polygon

def galah_geolocate(polygon=None,
                    bbox=None):
    """
    Restrict results to those from a specified area. Areas can be specified as 
    either polygons or bounding boxes, depending on type.
    
    Parameters
    ----------
        polygon : string, polygon object
            one polygon used to search (can be file name or polygon object).
        bbox : list, string
            list containing [xmin, ymin, xmax, ymax] or a polygon object.
        verbose : 

    Returns
    -------
        An object of class ``pandas.DataFrame``.

    Examples
    --------

    .. prompt:: python

        import galah
        galah.search_taxa(taxa="Vulpes vulpes")

    .. program-output:: python -c "import galah; print(galah.search_taxa(taxa=\\\"Vulpes vulpes\\\"))"
    """

    if polygon is not None:

        print(polygon)
        print(type(polygon))

        if type(polygon) is list:
            raise ValueError("Unsure how to deal with polygon lists")
        elif type(polygon) is str:
            if "POLYGON" not in polygon and "MULTIPOLYGON" not in polygon:
                if "shp" not in polygon:
                    raise ValueError("Only a shape file or wkt should be passed to polygon")
            geometry = shapely.wkt.loads(polygon)
            new_geom = str(geometry).replace("POLYGON ","MULTIPOLYGON (") + ")"
            return "wkt={}".format(urllib.parse.quote(str(new_geom))) # geometry
        elif type(polygon) is Polygon or MultiPolygon:
            return "wkt={}".format(urllib.parse.quote(str(polygon)))
        else:
            raise ValueError("The only types of variables geolocate takes are list, str and polygons")

    elif bbox is not None:

        print(bbox)
        print(type(bbox))

        if type(bbox) is list:
            new_bbox = Polygon.from_bounds(bbox[0],bbox[1],bbox[2],bbox[3])
            return "wkt={}".format(urllib.parse.quote(str(new_bbox)))
        elif type(bbox) is str:
            geometry = shapely.wkt.loads(bbox)
            new_geom = str(geometry).replace("POLYGON ","MULTIPOLYGON (") + ")"
            return "wkt={}".format(urllib.parse.quote(new_geom))
        elif type(bbox) is shapely.geometry.polygon.Polygon or shapely.geometry.polygon.MultiPolygon:
            bounds=list(bbox.bounds)
            new_bbox = box(bounds[0],bounds[1],bounds[2],bounds[3])
            return "wkt={}".format(urllib.parse.quote(str(new_bbox)))
        else:
            raise ValueError("The only types of variables geolocate takes are list, str and polygons")