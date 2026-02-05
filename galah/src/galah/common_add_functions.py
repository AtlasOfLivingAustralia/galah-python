import urllib

from .galah_config import readConfig
from .galah_filter import (check_for_duplicate_filters, galah_filter,
                           process_or_filters)
from .galah_geolocate import galah_geolocate
from .search_taxa import generate_list_taxonConceptIDs


def add_extras_to_URL(add_email=True, use_data_profile=False, data_profile_list=None, atlas=None, config_file=None):

    # get your configs
    configs = readConfig(config_file=config_file)

    # initialise variable
    end_url = "&"

    # first, check for email_notify
    end_url += "emailNotify={}&".format(configs["galahSettings"]["email_notify"].lower())

    # next, check for email
    if add_email:
        if configs["galahSettings"]["email_notify"] not in ["None", ""]:
            end_url += "email={}&".format(urllib.parse.quote(configs["galahSettings"]["email"]))

    # then, check for data profile
    if use_data_profile:
        if not (configs["galahSettings"]["data_profile"] in ["None", ""]):
            if configs["galahSettings"]["data_profile"] in data_profile_list:
                end_url += "qualityProfile={}&".format(configs["galahSettings"]["data_profile"])
            else:
                raise ValueError(
                    "The data quality profile not recognised. To see valid data quality profiles, run \n\n"
                    "profiles = galah.show_all(profiles=True)\n\n"
                    "then type\n\n"
                    "profiles['shortName']\n\n"
                    "  To set a data profile, type\n"
                    "galah.galah_config(data_profile='NAME FROM SHORTNAME HERE')"
                    "If you don't want to use a data quality profile, set it to None by typing the following:\n\n"
                    "galah.galah_config(data_profile='None')"
                )
    else:
        if atlas in ["Australia", "ALA"]:
            end_url += "disableAllQualityFilters=true&"

    # finally, add reason
    end_url += "reasonTypeId={}".format(configs["galahSettings"]["reason"])
    end_url += "&pageSize=0"

    # return end_url
    return end_url


def add_filters(URL=None, atlas=None, filters=None, authenticate=False):
    """Adding filters directly to the URL"""
    # first, check if filters are None
    if filters is None:
        return URL

    # check if the atlas being used is GBIF
    if atlas in ["Global", "GBIF"]:

        # check for filters that are not valid with GBIF
        if any("!=" in f for f in filters):
            raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")

        # now, loop over filters
        fs = []
        for f in filters:
            fs.append(galah_filter(f=f, authenticate=authenticate))

        # add filters to URL
        URL += "&".join(fs)

        # return URL for GBIF
        return URL

    # check to see if taxa are already in the URL - if not, add fq
    if "fq=" not in URL:
        URL += "fq="  # was
    else:
        URL += "%20AND%20"  # add this; test this
    URL += "%28"

    # check for multiple filters with same name
    filters = check_for_duplicate_filters(filters=filters)

    # split filters into type: OR/AND
    or_filters, and_filters = [], []

    # Source - https://stackoverflow.com/questions/949098/how-can-i-partition-split-up-divide-a-list-based-on-a-condition
    # Posted by John La Rooy
    # Retrieved 05/11/2025, License - CC-BY-SA 4.0
    # split list based on the condition
    for f in filters:
        (and_filters, or_filters)[any(x in f for x in ["|", ","])].append(f)

    # try this
    if len(or_filters) > 0:
        for f in or_filters:
            if ", " in f:
                and_filters.append(f)
                or_filters.remove(f)

    # add and filters
    if len(and_filters) > 0:
        URL += "%20AND%20".join([galah_filter(x) for x in and_filters]) + "%20AND%20"

    # process or filters
    URL = process_or_filters(or_filters=or_filters, URL=URL)

    # return URL
    if URL[-9:] == "%20AND%20":
        URL = URL[:-9]
    URL += "%29"
    return URL


# adds predicates to GBIF
def add_predicates(predicates=None, filters=None, occurrencesGBIF=False):
    """for adding filters specifically to atlas_occurrences"""

    if filters is None:
        return predicates

    if isinstance(filters, str):
        filters = [filters]

    if any("!=" in f for f in filters):
        raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")

    for f in filters:

        predicates.append(galah_filter(f, occurrencesGBIF=occurrencesGBIF))

    return predicates


# galah_geolocate
def add_spatial_shapes(polygon=None, bbox=None, URL=None, simplify_polygon=False, tolerance=0.05):
    # testing for galah_geolocate - implemented in next version

    if all(x is None for x in [polygon, bbox]):
        return URL

    URL += "&wkt=" + urllib.parse.quote(
        str(galah_geolocate(polygon=polygon, bbox=bbox, simplify_polygon=simplify_polygon, tolerance=tolerance))
    )

    return URL


def add_taxa(taxa=None, atlas=None, URL=None, scientific_name=None):

    if all(x is None for x in [taxa, scientific_name]):
        if URL[-1] == "?":
            return URL
        return URL + "?"

    # if there is no taxa, assume you will get the total number of records in the ALA
    taxonConceptID = generate_list_taxonConceptIDs(taxa=taxa, atlas=atlas, scientific_name=scientific_name)

    # return None if there is no taxonConceptID; otherwise,
    if taxonConceptID is None:
        if URL[-1] == "?":
            URL += "?" # try this
        return URL
    if URL[-1] == "?":
        return URL + taxonConceptID

    URL += "?" + taxonConceptID

    return URL
