import requests
import urllib
from .galah_filter import galah_filter
from .get_api_url import get_api_url
from .search_taxa import search_taxa
from .galah_geolocate import galah_geolocate
from .common_dictionaries import atlases, ATLAS_KEYWORDS

# for adding filters specifically to atlas_occurrences
def add_predicates(predicates=None,
                   filters=None):

    if type(filters) == str:
        filters = [filters]

    if any("!=" in f for f in filters):
        raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")

    for f in filters:

        predicates.append(galah_filter(f,occurrencesGBIF=True))

    return predicates

# for adding filters to the URL
def add_filters(URL=None,
                atlas=None,
                filters=None,
                ifGroupBy=False):

    # change type of filters to list for easy looping
    if type(filters) == str:
        filters = [filters]

    # check if the atlas being used is GBIF
    if atlas in ["Global","GBIF"]:

        # check for filters that are not valid with GBIF
        if any("!=" in f for f in filters):
            raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")
        else:
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
            URL += galah_filter(f,ifgroupBy=ifGroupBy) + "AND" 
                    
        # remove last AND and add a closing parenthesis
        URL = URL[:-len("AND")] + "%29"
        
    return URL

def put_entries_in_grouped_dict(entry=None,
                                dict_values=None,
                                name=None,
                                value=None,
                                expand=None
                                ):
    '''X'''
    if expand:
        name2,value2 = entry['fq'].split(":")
        value2 = value2.replace('"', '')
        if value2.isdigit():
            value2 = int(value2)
        dict_values[name2].append(value2)
        dict_values['count'].append(int(entry['count']))
        dict_values[name].append(value)
        for key in dict_values:
            if (key != name2) and (key != name) and (key != 'count'):
                dict_values[key].append("-")

    else:
        name,value=entry['fq'].split(':')
        value=value.replace('"','')
        if value.isdigit():
            value = int(value)
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
                      offset=None):
    '''Function for X'''

    # get data and check for 
    URL,method = get_api_url(column1=column1,column1value=column1value,column2=column2,column2value=column2value)
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
                                  atlas=None):

    if taxa is None:
        raise ValueError("Please provide a taxa for this information")
    
    if atlas is None:
        raise ValueError("Please provide an atlas to this function")

    # change taxa into list for easier looping and check if type of variable is correct
    if type(taxa) is str:
        taxa = [taxa]
    elif type(taxa) is list:
        pass
    else:
        raise TypeError("The taxa argument can only be a string or a list."
                    "\nExample: atlas.counts(\"Vulpes vulpes\")"
                    "\n         atlas.counts[\"Osphranter rufus\",\"Vulpes vulpes\",\"Macropus giganteus\",\"Phascolarctos cinereus\"])")

    # get the number of records associated with each taxa
    for name in taxa:

        # create temporary dataframe for taxon id
        tempdf = search_taxa(name)
        
        # check if dataframe is empty - if so, return None; else, continue
        if tempdf.empty:
            print("No taxon matches were found for {} in the selected atlas ({})".format(name, atlas))
            if len(taxa) == 1:
                return None
            continue

    # get the taxonConceptID for taxa while checking for extant atlas
    if atlas in atlases:
        taxonConceptID = list(search_taxa(taxa)[ATLAS_KEYWORDS[atlas]])
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
                       filters=None,
                       polygon=None,
                       bbox=None
                       ):

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

    if filters is not None:
        if type(filters) is str:
            if "fq" not in payload:
                payload["fq"] = [galah_filter(filters)]
            else:
                payload["fq"].append(galah_filter(filters))
        else:
            for f in filters:
                if "fq" not in payload:
                    payload["fq"] = [galah_filter(f)]
                else:
                    payload["fq"].append(galah_filter(f))

    if polygon is not None or bbox is not None:
        wkts = galah_geolocate(polygon=polygon,bbox=bbox)
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