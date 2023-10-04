import urllib
import shapely
import shapely.wkt
from shapely import Polygon,MultiPolygon
from .get_api_url import readConfig

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

    Returns
    -------
        An object of class ``pandas.DataFrame``.

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
                        n=1
                return shapely.wkt.loads(polygon)
            elif type(polygon) is Polygon or MultiPolygon:
                return str(polygon)
            else:
                print(polygon)
                print(type(polygon))
                raise ValueError("The only types of variables geolocate takes are str and polygons")

        elif bbox is not None:

            if type(bbox) is dict:
                #xmin, ymin, xmax, ymax
                print()
                return str(shapely.box(xmin=bbox["xmin"],xmax=bbox["xmax"],ymin=bbox["ymin"],ymax=bbox["ymax"]))
            elif type(bbox) is Polygon or type(bbox) is MultiPolygon:
                bounds=list(bbox.bounds)
                new_bbox = shapely.box(bounds[0],bounds[1],bounds[2],bounds[3])
                return str(new_bbox)
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
    
    # graveyard
    '''
            if type(polygon) is list:
                #print("here")
                polygon_wkts = "" #"(" #[]
                for i,p in enumerate(polygon):
                    if type(polygon) is str:
                        if "POLYGON" not in polygon and "MULTIPOLYGON" not in polygon:
                            raise ValueError("Only a wkt should be passed to polygon")
                        geometry = shapely.wkt.loads(p)
                        polygon[i] = str(geometry)
                        #polygon_wkts.append(str(geometry)) #"," + str(geometry) 
                    elif type(p) is Polygon or MultiPolygon:
                        polygon[i] = str(p)
                        #polygon_wkts.append(str(p)) #+= "," + str(p)
                    else:
                        raise ValueError("Only Polygon/MultiPolygon or str objects accepted for galah_geolocate")
                {{ fq=geo:"Intersects(-74.093 41.042 -69.347 44.558)"}}

                {{ fq=geo:"IsWithin(POLYGON((-10 30, -40 40, -10 -20, 40 20, 0 0, -10 30))) distErrPct=0"}}
                #print(polygon_wkts)
                #[" OR ".join("lsid:{}".format(id) for id in taxa_list)]
                polygon_wkts += str(" OR ".join(polygon)) #+ ")" #"wkt:{}".format()
                #return " OR ".join(polygon) 
                #return polygon
                return polygon_wkts #[1:]
                
    '''