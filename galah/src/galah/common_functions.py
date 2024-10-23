import requests
import urllib
import geopandas as gpd
import shapely
import shutil
from .galah_filter import galah_filter
from .get_api_url import get_api_url
from .search_taxa import search_taxa
from .galah_geolocate import galah_geolocate
from .common_dictionaries import atlases, ATLAS_KEYWORDS, MM_EXTENSIONS
from shapely import Polygon,MultiPolygon
from .version import __version__

def add_predicates(predicates=None,
                   filters=None):
    '''for adding filters specifically to atlas_occurrences'''

    if type(filters) == str:
        filters = [filters]

    if any("!=" in f for f in filters):
        raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")

    for f in filters:

        predicates.append(galah_filter(f,occurrencesGBIF=True))

    return predicates

def add_filters(URL=None,
                atlas=None,
                filters=None,
                ifGroupBy=False):
    '''Adding filters directly to the URL'''

    # change type of filters to list for easy looping
    if type(filters) == str:
        filters = [filters]

    # check if the atlas being used is GBIF
    if atlas in ["Global","GBIF"]:

        # check for filters that are not valid with GBIF
        if any("!=" in f for f in filters):
            raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")
        else:
            ### TODO: check that this is correct
            for f in filters:
                URL += "&{}".format(galah_filter(f,ifgroupBy=ifGroupBy))

    # filters for all other atlases
    else:

        # check to see if taxa are already in the URL - if not, add fq
        if "fq=" not in URL:
            URL += "fq=%28"
        else:
            URL += "%28"

        # loop over filters
        for f in filters:
            URL += galah_filter(f,ifgroupBy=ifGroupBy) + "%20AND%20"
        
        # remove last AND and add a closing parenthesis
        URL = URL[:-len("%20AND%20")] + "%29"
        
    return URL

def put_entries_in_grouped_dict(entry=None,
                                dict_values=None,
                                expand=None
                                ):
    '''Creating dictionaries for galah_group_by'''

    if expand:

        if len(entry['fq'].split(':')) > 2:
            name_and_values = entry['fq'].split(':')
            name = name_and_values[0]
            value = ":".join(name_and_values[1:])
        else:
            name,value=entry['fq'].split(':')

        value = value.replace('"', '')
        if value.isdigit():
            value = int(value)
        
        # check that this is correct
        if name in dict_values:
            dict_values[name].append(value)
            dict_values['count'].append(int(entry['count']))

        for key in dict_values:
            if (key != name) and (key != 'count'):
                while (len(dict_values[key]) < len(dict_values['count'])):
                    dict_values[key].append("-")

    else:
        if len(entry['fq'].split(':')) > 2:
            name_and_values = entry['fq'].split(':')
            name = name_and_values[0]
            value = ":".join(name_and_values[1:])
        else:
            name,value=entry['fq'].split(':')
        value=value.replace('"','')
        if value.isdigit():
            value = int(value)
        # check that this is correct
        if name in dict_values:
            dict_values[name].append(value)
            dict_values['count'].append(int(entry['count']))
        for entry in dict_values:
            if (entry != name) and (entry != 'count'):
                dict_values[entry].append("-")

    return dict_values    

def get_response_show_all(column1=None,
                      column1value=None,
                      column2=None,
                      column2value=None,
                      atlas=None,
                      headers={},
                      max_entries=-1,
                      offset=None,
                      verbose=False):
    
    '''Function for getting responses for all of the show_all functions'''
    # get headers
    headers = {"User-Agent": "galah-python {}".format(__version__)}

    # get data and check for 
    URL,method = get_api_url(column1=column1,column1value=column1value,column2=column2,column2value=column2value)
    if verbose:
        print("URL for querying:\n\n{}".format(URL))
        print("Method: {}".format(method))
        print()
    if max_entries is not None and offset is not None:
        URL += "?max={}&offset={}".format(max_entries,offset)
    response = requests.request(method,URL,headers=headers)
    if response.status_code == 403:
        raise ValueError("Provide a/an {} API key to get this information".format(atlas))
    if response.status_code == 429:
        raise ValueError("You have reached the maximum number of daily queries for the ALA.")

    # return response
    return response

def generate_list_taxonConceptIDs(taxa=None,
                                  scientific_name=None,
                                  atlas=None,
                                  verbose=None):
    '''Function for getting more than one taxonConceptIDs'''

    if taxa is None and scientific_name is None:
        raise ValueError("Please provide either a taxa or scientific_name for this information")
    
    if atlas is None:
        raise ValueError("Please provide an atlas to this function")

    # change taxa into list for easier looping and check if type of variable is correct
    if scientific_name is not None:

        # check for correct dictionary
        lens = [None for i in range(len(scientific_name))]
        for i,key in enumerate(scientific_name):
            lens[i] = len(scientific_name[key])
        if len(set(lens)) > 1:
            print(scientific_name)
            raise ValueError("Please provide a correctly formatted dictionary with scientific_name - you are missing one or more taxonomic keys.")
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
            raise TypeError("The taxa argument can only be a string or a list."
                        "\nExample: galah.atlas_counts(\"Vulpes vulpes\")"
                        "\n         galah.atlas_counts[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")

        # get the number of records associated with each taxa
        for name in taxa:

            # create temporary dataframe for taxon id
            tempdf = search_taxa(taxa=name,verbose=verbose)
            
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
    if atlas in ["Global","GBIF"]:

        # add using taxonKey
        return "".join(["taxonKey={}&".format(urllib.parse.quote(str(tid))) for tid in taxonConceptID])
    
    # for Australia
    elif atlas in ["Australia","ALA"]:

        return taxonConceptID
    
    else:

        return "fq=%28lsid%3A" + "%20OR%20lsid%3A".join(
                urllib.parse.quote(str(tid)) for tid in taxonConceptID) + "%29"

def add_to_payload_ALA(payload=None,
                       atlas=None,
                       taxa=None,
                       scientific_name=None,
                       filters=None,
                       polygon=None,
                       bbox=None,
                       simplify_polygon=False
                       ):
    '''Function for adding variables to the payload when we cache (post) data to the ALA'''

    if payload is None:
        raise ValueError("You need to provide the payload for this function")
    
    if atlas is None:
        raise ValueError("You need to provide the atlas for this function")

    if taxa is not None:
        taxa_list = generate_list_taxonConceptIDs(taxa=taxa,atlas=atlas)
        if "fq" not in payload:
            payload["fq"] = [" OR ".join("lsid:{}".format(id) for id in taxa_list)]
        else:
            payload["fq"].append(" OR ".join("lsid:{}".format(id) for id in taxa_list))

    if scientific_name is not None:
        taxa_list = generate_list_taxonConceptIDs(scientific_name=scientific_name,atlas=atlas)
        if "fq" not in payload:
            payload["fq"] = [" OR ".join("lsid:{}".format(id) for id in taxa_list)]
        else:
            payload["fq"].append(" OR ".join("lsid:{}".format(id) for id in taxa_list))

    if filters is not None:
        if type(filters) is str:
            filters_check = galah_filter(filters)
            if " AND " in filters_check:
                filters_check = filters_check.split(" AND ")
            payload = add_filter_to_payload(filters_check,payload=payload)
        else:
            for f in filters:
                filters_check = galah_filter(f)
                if " AND " in filters_check:
                    filters_check = filters_check.split(" AND ")
                payload = add_filter_to_payload(filters_check,payload=payload)

    if polygon is not None or bbox is not None:
        wkts = galah_geolocate(polygon=polygon,bbox=bbox,simplify_polygon=simplify_polygon)
        if "wkt" not in payload:
            if type(wkts) is str:
                payload["wkt"] = [wkts]
            else:
                payload["wkt"] = wkts
        else:
            if type(wkts) is str:
                payload["wkt"].append(wkts)
            else:
                payload["wkt"] += wkts

    return payload

def add_filter_to_payload(f,payload):
    '''Checks for less than or greater than syntax and returns two strings'''
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


def add_buffer(polygon=None,
               bbox=None,
               buffer=None,
               crs_deg=4326,
               crs_meters=3577):
    '''DEPRECATED? function to add buffer to shapefile'''
    
    if buffer is None:
        raise ValueError("You need to include a buffer with this function")
    
    # make sure buffer is in meters
    if buffer>1000:
        raise ValueError("Currently `galah-python` doesn't support buffers greater than 1000km.  Enter a number between 0 and 1000.")
    buffer = buffer*1000

    if polygon is not None:

        # make sure polygon is the correct type
        if type(polygon) is str or type(polygon) is Polygon or type(polygon) is MultiPolygon:
            polygon_df = gpd.GeoDataFrame({"name": "user_defined_polygon","geometry": polygon},index=[0],crs="EPSG:{}".format(crs_deg))
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
            bbox_df = gpd.GeoDataFrame({"name": "user_defined_bbox","geometry": bbox},index=[0],crs="EPSG:{}".format(crs_deg))
        else:
            raise ValueError("The polygon must be either of type string or type Polygon/MultiPolygon")
        
        # change Coordinate Reference System, add buffer, and change it back to 
        bbox_meters = bbox_df.to_crs(crs_meters)
        bbox_meters_buffer = bbox_meters.buffer(buffer)
        bbox_buffer = bbox_meters_buffer.to_crs(crs_deg)
        
        # return the polygon
        return bbox_buffer[0]
    
def write_image_to_file(image=None,
                        headers=None,
                        path=None,
                        thumbnail=False):

    # set extension variable
    ext = ""

    # replace extensions in mimetype with actual filenames
    if image["mimetype"] in MM_EXTENSIONS:
        ext = MM_EXTENSIONS[image["mimetype"]]
    else:
        raise ValueError("Extension {} is not in our list of extensions.".format(image["mimetype"]))

    # check if they want the thumbnail vs. original 
    if thumbnail:
        data = requests.get(image["imageUrl"].replace('original','thumbnail'),headers=headers,stream=True)
    else:
        data = requests.get(image["imageUrl"],headers=headers,stream=True)

    # write image to file
    with open("{}/{}.{}".format(path,image["images"],ext),'wb') as f:
        data.raw.decode_content = True
        shutil.copyfileobj(data.raw,f)