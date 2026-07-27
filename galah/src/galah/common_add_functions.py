import urllib

from .common_dictionaries import (ATLAS_GEO_NAMES, QGIS_SOURCE_TYPE_ID,
                                  SOURCE_TYPE_ID)
from .galah_filter import (check_for_duplicate_filters, galah_filter,
                           process_or_filters)
from .galah_geolocate import galah_geolocate
from .search_taxa import generate_list_taxonConceptIDs, search_taxa


def add_extras_to_URL(
    atlas=None,
    qgis=None,
    email_notify=None,
    email=None,
    add_email=True,
    use_data_profile=False,
    data_profile_list=None,
    data_profile=None,
    reason=None,
):

    # get qgis argument
    if qgis:
        sourceTypeId = QGIS_SOURCE_TYPE_ID
    else:
        sourceTypeId = SOURCE_TYPE_ID

    # initialise variable
    end_url = "&"

    # next, check for email
    if add_email:
        end_url += "email={}&".format(urllib.parse.quote(email))
        end_url += "emailNotify={}&".format(str(email_notify).lower())

    # then, check for data profile
    if use_data_profile:
        if not (data_profile in ["None", ""]):
            if data_profile in data_profile_list:
                end_url += "qualityProfile={}&".format(data_profile)
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
        # if atlas in ["Australia", "ALA"]:
        end_url += "disableAllQualityFilters=true&"

    # finally, add reason
    end_url += f"reasonTypeId={reason}"
    if atlas in ["ALA", "Australia"]:
        end_url += f"&sourceTypeId={sourceTypeId}&pageSize=0"

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
        check_missing_filters_GBIF(filters=filters)

        # now, loop over filters
        fs = []
        for f in filters:
            fs.append(galah_filter(f=f, atlas=atlas, authenticate=authenticate))

        # add filters to URL
        URL += "&".join(fs)

        # return URL for GBIF
        return URL

    # check to see if taxa are already in the URL - if not, add q or fq
    URL = check_for_added_taxa(URL=URL)

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
        URL += (
            "%20AND%20".join([galah_filter(x, atlas=atlas, authenticate=authenticate) for x in and_filters])
            + "%20AND%20"
        )

    # process or filters
    URL = process_or_filters(or_filters=or_filters, URL=URL)

    # return URL
    if URL[-9:] == "%20AND%20":
        URL = URL[:-9]
    URL += "%29"
    return URL


def check_missing_filters_GBIF(filters=None):

    # check for filters that are not valid with GBIF
    if any("!=" in f for f in filters):
        raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")


def check_for_added_taxa(URL=None):

    # check for q and fq in url; return URL
    if "q=" not in URL:
        URL += "q="
    elif "fq=" not in URL:
        URL += "&fq="  # was
    else:
        URL += "%20AND%20"  # add this; test this
    URL += "%28"
    return URL


# adds predicates to GBIF
def add_predicates(predicates=None, filters=None, occurrencesGBIF=True, taxa=None, atlas="Global"):
    """for adding filters specifically to atlas_occurrences"""

    if all(x is None for x in [filters, taxa]):
        return predicates

    if isinstance(filters, str):
        filters = [filters]

    if isinstance(taxa, str):
        taxa = [taxa]

    if filters is not None:
        if any("!=" in f for f in filters):
            raise ValueError("!= cannot be used with GBIF atlas.  Run separate queries.")

        for f in filters:

            predicates.append(galah_filter(f, occurrencesGBIF=occurrencesGBIF, atlas=atlas))

    if taxa is not None:

        for t in taxa:

            # get the taxon key
            t2 = search_taxa(taxa=t)["usageKey"][0]

            # have to see if taxonKey is the right one
            predicates.append(galah_filter("taxonKey={}".format(t2), atlas="GBIF", occurrencesGBIF=occurrencesGBIF))

    return predicates


def add_spatial_shapes(atlas=None, polygon=None, bbox=None, URL=None, crs=None):

    # return URL if there are no shapes
    if all(x is None for x in [polygon, bbox]):
        return URL

    # add text to URL
    URL += f"&{ATLAS_GEO_NAMES[atlas]}=" + urllib.parse.quote(
        str(
            galah_geolocate(
                atlas=atlas,
                polygon=polygon,
                bbox=bbox,
                # simplify_polygon=simplify_polygon,
                # tolerance=tolerance,
            )
        )
    )

    return URL


def add_taxa(
    taxa=None,
    atlas=None,
    URL=None,
    scientific_name=None,
    predicates=None,
    specific_epithet=None,
    identifiers=None,
):

    if all(x is None for x in [taxa, scientific_name, specific_epithet, identifiers]):
        if URL[-1] == "?":
            return URL
        return URL + "?"

    # if there is no taxa, assume you will get the total number of records in the ALA
    taxonConceptID = generate_list_taxonConceptIDs(
        taxa=taxa,
        atlas=atlas,
        scientific_name=scientific_name,
        specific_epithet=specific_epithet,
        identifiers=identifiers,
    )

    # return None if there is no taxonConceptID; otherwise,
    if taxonConceptID is None:
        if URL[-1] == "?":
            URL += "?"  # try this
        return URL
    if URL[-1] == "?":
        return URL + taxonConceptID

    URL += "?" + taxonConceptID

    return URL
