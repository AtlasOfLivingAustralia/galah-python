import configparser
import os

import geopandas as gpd
import pandas as pd
import pytest
import shapely

import galah

configParser = configparser.ConfigParser()
configParser.read("logins.txt")
email_au = configParser["Australia"]["email"]


'''
######################################
# exceptions and errors
######################################


######################################
# search_taxa
######################################
def test_search_taxa_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    output = galah.search_taxa("Vulpes vulpes")
    assert output["taxonConceptID"][0] != None


def test_search_taxa_australia_two_taxa_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    output = galah.search_taxa(["Vulpes vulpes", "Osphranter rufus"])
    assert output["taxonConceptID"][0] != None


def test_search_taxa_australia_identifiers_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    output = galah.search_taxa(identifiers="https://id.biodiversity.org.au/node/apni/2914510")
    assert output["taxonConceptID"][0] != None


def test_search_taxa_australia_specific_epithet_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    output = galah.search_taxa(
        specific_epithet={
            "class": "aves",
            "family": "pardalotidae",
            "genus": "pardalotus",
            "specificEpithet": "punctatus",
        }
    )
    #     "class=aves",
    # "family=pardalotidae",
    # "genus=pardalotus",
    # "specificEpithet=punctatus",
    assert output.shape[0] > 0


def test_search_taxa_australia_scientific_name_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    output = galah.search_taxa(
        scientific_name={
            "family": ["pardalotidae", "maluridae"],
            "scientificName": ["pardolatus striatus", "malurus cyaneus"],
        }
    )
    assert output.shape[0] > 0


######################################
# atlas_counts
######################################
def test_atlas_counts_australia_scientific_name_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    output = galah.atlas_counts(
        scientific_name={
            "family": ["pardalotidae", "maluridae"],
            "scientificName": ["pardolatus striatus", "malurus cyaneus"],
        }
    )
    assert output.shape[0] > 0


def test_atlas_counts_australia_config_authenticate():
    if os.path.isfile("test.ini"):
        os.remove("test.ini")
    os.system("touch test.ini")
    galah.galah_config(config_file="test.ini", atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes vulpes"
    assert galah.atlas_counts(taxa=taxa)["totalRecords"][0] > 0


def test_atlas_counts_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes vulpes"
    assert galah.atlas_counts(taxa=taxa)["totalRecords"][0] > 0


def test_atlas_counts_filters_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_or_filters2_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters="year=[2021,2022]")
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_assertion_as_true_filter_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters="BASIS_OF_RECORD_INVALID=True")
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_assertion_as_false_filter_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters="BASIS_OF_RECORD_INVALID=False")
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_or_filters2_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=["year=2021", "year=2022"])
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_filters_groupby_expand_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    f = "year=2022"
    groups = ["month", "basisOfRecord"]
    filtered_counts = galah.atlas_counts(filters=f, group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_filters_groupby_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    f = "year=2022"
    groups = ["month", "basisOfRecord"]
    filtered_counts = galah.atlas_counts(filters="year=2022", group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_taxa_filter_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa=taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filter_empty_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes vulpes"
    filter1 = "year="
    assert galah.atlas_counts(taxa=taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa=taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022", "year!=2020"]
    assert galah.atlas_counts(taxa=taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filter_data_quality_australia_authenticate():
    galah.galah_config(atlas="Australia", data_profile="ALA")
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    no_quality = galah.atlas_counts(taxa, filters=filter1)
    quality = galah.atlas_counts(taxa, filters=filter1, use_data_profile=True)
    assert no_quality["totalRecords"][0] >= quality["totalRecords"][0]


def test_atlas_counts_multiple_taxa_filters_separate_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Swainsona formosa",
        "Crocodylus johnstoni",
        "Platalea (Platalea) regia",
        "Notamacropus agilis",
    ]
    f = ["dataResourceName = iNaturalist Australia", "year=2022"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()  # checks that all species counts are greater than or equal zero


def test_atlas_counts_taxa_group_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes vulpes"
    group_by = "year"
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_groups_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes vulpes"
    group_by = ["year", "basisOfRecord"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_groups_expand_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes vulpes"
    group_by = ["year", "basisOfRecord"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_filters_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes vulpes"
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    assert galah.atlas_counts(taxa, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filters_group_by_no_expand_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes vulpes"
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    group_by = "basisOfRecord"
    output = galah.atlas_counts(taxa, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_filters_australia_total_group_by_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    output = galah.atlas_counts(taxa="reptilia", filters="year=2020", group_by="species", total_group_by=True)
    assert output.shape[0] == 1
    assert output["count"][0] > 0


def test_atlas_counts_multiple_taxa_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    assert galah.atlas_counts(taxa_array)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_group_by_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    group_by = ["year", "basisOfRecord"]
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_multiple_taxa_filter_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filter_group_by_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    filter1 = "year=2020"
    group_by = "basisOfRecord"
    output = galah.atlas_counts(taxa_array, filters=filter1, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    assert galah.atlas_counts(taxa_array, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filters_group_by_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    filters = ["year>2010", "basisOfRecord=HUMAN_OBSERVATION"]
    group_by = ["county", "year"]
    # county** , associatedOrganisms , day , decade
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_invalid_multiple_taxa_separate_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Dasyurus hallucatus",
        "Ailuropoda melanoleuca",
        "Centrostephanus rodgersii",
    ]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_separate_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Dasyurus hallucatus",
        "Rhincodon typus",
        "Ceyx azureus",
        "Ornithorhynchus anatinus",
    ]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_separate_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Swainsona formosa",
        "Crocodylus johnstoni",
        "Platalea (Platalea) regia",
        "Xeromys myoides",
    ]
    f = ["dataResourceName = iNaturalist Australia", "year=2019"]
    group_by = ["month", "species"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()  # checks that all species counts are greater than zero


def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Swainsona formosa",
        "Crocodylus johnstoni",
        "Platalea (Platalea) regia",
        "Xeromys myoides",
    ]
    f = ["dataResourceName = iNaturalist Australia"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()  # checks that all species counts are greater than zero


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_australia_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    taxa_array = [
        "Swainsona formosa",
        "Crocodylus johnstoni",
        "Platalea (Platalea) regia",
        "Xeromys myoides",
    ]
    f = ["dataResourceName = iNaturalist Australia", "year=2022"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert output["count"][0] >= 0  # checks that all species counts are greater than or equal zero


def test_atlas_counts_geolocate_polygon_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    test_shape = shapely.box(143, -29, 148, -28)
    counts = galah.atlas_counts(polygon=test_shape)
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_bbox_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    test_shape = shapely.box(143, -29, 148, -28)
    counts = galah.atlas_counts(bbox=test_shape)
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_bbox_dict_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    counts = galah.atlas_counts(bbox={"xmin": 143, "ymin": -29, "xmax": 148, "ymax": -28})
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_polygon_taxa_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    test_shape = shapely.box(143, -29, 148, -28)
    counts = galah.atlas_counts(taxa="reptilia", polygon=test_shape)
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_bbox_taxa_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    test_shape = shapely.box(143, -29, 148, -28)
    counts = galah.atlas_counts(taxa="reptilia", bbox=test_shape)
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_pandas_polygon_taxa_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    test_shape = pd.DataFrame({"minx": 143, "miny": -29, "maxx": 148, "maxy": -28}, index=[0])
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts(taxa="reptilia", polygon=test_shape)
    assert "str" in str(e_info.value)


def test_atlas_counts_geolocate_pandas_bbox_taxa_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    test_shape = pd.DataFrame({"minx": 143, "miny": -29, "maxx": 148, "maxy": -28}, index=[0])
    counts = galah.atlas_counts(taxa="reptilia", bbox=test_shape)
    assert counts["totalRecords"][0] > 0


def tests_atlas_counts_geolocate_polygon_simplify_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    test_shape = gpd.read_file("nsw_state_polygon_shp/STE_2021_AUST_GDA94.shp")
    test_shape = test_shape.to_crs(4326)
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts(taxa="reptilia", polygon=test_shape)
    assert "variables" in str(e_info.value)


def tests_atlas_counts_geolocate_polygon_simplify_single_shape_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    test_shape = gpd.read_file("nsw_state_polygon_shp/STE_2021_AUST_GDA94.shp")
    test_shape = test_shape.to_crs(4326)
    nsw = str(test_shape[test_shape["STE_NAME21"] == "New South Wales"]["geometry"][0])
    counts = galah.atlas_counts(taxa="reptilia", polygon=nsw, simplify_polygon=True)
    assert counts["totalRecords"][0] > 0


######################################
# atlas_species
######################################
def test_atlas_species_Australia_species_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    taxa = "Heleioporus"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_species_rank_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    taxa = "Vulpes"
    species_table = galah.atlas_species(taxa=taxa, rank="subspecies")
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_family_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_family_rank_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa, rank="genus")
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_family_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa, rank="subspecies")
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_filter_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    full_species_table = galah.atlas_species(taxa="Rodentia")
    filtered_species_table = galah.atlas_species(taxa="Rodentia", filters="stateProvince=Victoria")
    assert full_species_table.shape[0] > filtered_species_table.shape[0]


def test_atlas_species_Australia_filter_notaxa_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    filtered_species_table = galah.atlas_species(filters=["year=2022", "stateProvince=Victoria"])
    assert filtered_species_table.shape[0] > 0


def test_atlas_species_Australia_polygon_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    full_species_table = galah.atlas_species(polygon=shapely.box(143, -29, 148, -28))
    assert full_species_table.shape[0] > 0


def test_atlas_species_Australia_bbox_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    full_species_table = galah.atlas_species(bbox=shapely.box(143, -29, 148, -28))
    assert full_species_table.shape[0] > 0


def test_atlas_species_Australia_filter_polygon_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    full_species_table = galah.atlas_species(polygon=shapely.box(143, -29, 148, -28))
    filtered_species_table = galah.atlas_species(
        polygon=shapely.box(143, -29, 148, -28), filters="stateProvince=Victoria"
    )
    assert full_species_table.shape[0] > filtered_species_table.shape[0]


def test_atlas_species_Australia_filter_polygon_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    full_species_table = galah.atlas_species(bbox=shapely.box(143, -29, 148, -28))
    filtered_species_table = galah.atlas_species(bbox=shapely.box(143, -29, 148, -28), filters="stateProvince=Victoria")
    assert full_species_table.shape[0] > filtered_species_table.shape[0]


def test_atlas_species_Australia_filter_notaxa_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    filtered_species_table = galah.atlas_species(filters=["year=2022", "stateProvince=Victoria"])
    assert filtered_species_table.shape[0] > 0


######################################
# atlas_occurrences
######################################
def test_atlas_occurrences_taxa_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes")
    assert occurrences.shape[0] > 1


def test_atlas_occurrences_taxa_fields_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes", fields=["decimalLatitude", "decimalLongitude"])
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes", filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filter_fields_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    occurrences = galah.atlas_occurrences(
        taxa="Vulpes vulpes",
        filters="year=2020",
        fields=["decimalLatitude", "decimalLongitude"],
    )
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters2_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    filters = ["year>2018", "basisOfRecord=HUMAN_OBSERVATION"]
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes", filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filters_fields_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    occurrences = galah.atlas_occurrences(
        taxa="Vulpes vulpes",
        filters=["year>2018", "basisOfRecord=HUMAN_OBSERVATION"],
        fields=["decimalLatitude", "decimalLongitude"],
    )
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_data_profile_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    galah.galah_config(data_profile="ALA")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes", use_data_profile=True)
    galah.galah_config(data_profile=None)
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_geolocate_polygon_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    test_shape = shapely.box(143, -29, 148, -28)
    occurrences = galah.atlas_occurrences(polygon=test_shape)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_geolocate_bbox_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    test_shape = shapely.box(143, -29, 148, -28)
    occurrences = galah.atlas_occurrences(bbox=test_shape)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_geolocate_bbox_dict_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    occurrences = galah.atlas_occurrences(bbox={"xmin": 143, "ymin": -29, "xmax": 148, "ymax": -28})
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_geolocate_polygon_taxa_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    test_shape = shapely.box(143, -29, 148, -28)
    occurrences = galah.atlas_occurrences(taxa="reptilia", polygon=test_shape)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_geolocate_bbox_taxa_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    test_shape = shapely.box(143, -29, 148, -28)
    occurrences = galah.atlas_occurrences(taxa="reptilia", bbox=test_shape)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_mint_doi_authenticate():
    galah.galah_config(
        atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json"
    )  # ala4r@ala.org.au
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes", mint_doi=True)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_doi_authenticate():
    galah.galah_config(
        atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json"
    )  # ala4r@ala.org.au
    occurrences = galah.atlas_occurrences(doi="https://doi.org/10.26197/ala.e413b946-8959-41f8-9ae9-897d86029844")
    assert occurrences.shape[0] > 0


######################################
# atlas_media
######################################


# test if it can get a taxa and return output
def test_atlas_media_taxa_australia_authenticate():
    galah.galah_config(
        atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json"
    )  # ala4r@ala.org.au
    output = galah.atlas_media(taxa="Liopholis margaretae")
    assert output.shape[0] > 1


# test if the filters component of atlas_media is working
def test_atlas_media_filters_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    raw_output = galah.atlas_media(taxa="Liopholis margaretae")
    filtered_output = galah.atlas_media(taxa="Liopholis margaretae", filters="decimalLatitude<-24.0")
    assert raw_output.shape[0] > filtered_output.shape[0]


def test_atlas_media_multimedia_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    multimedia_output = galah.atlas_media(taxa="Liopholis margaretae", multimedia="images")
    assert multimedia_output.shape[0] > 0


def test_atlas_media_filters_multimedia_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    raw_output = galah.atlas_media(taxa="Liopholis margaretae")
    multimedia_output = galah.atlas_media(
        taxa="Liopholis margaretae", filters="decimalLatitude<=-24.0", multimedia="images"
    )
    assert raw_output.shape[0] > multimedia_output.shape[0]


def test_atlas_media_filters_multimedia_collect_path_australia_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    path = "test"
    multimedia_output = galah.atlas_media(
        taxa="Liopholis margaretae",
        multimedia="images",
        filters="decimalLatitude<=-24.0",
        collect=True,
        path=path,
    )
    files = os.listdir(path)
    assert len(files) > 0


def test_atlas_counts_no_valid_taxa_authenticate():
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    counts = galah.atlas_counts(taxa="Macronycteris commersoni")
    assert counts == None


def test_atlas_counts_no_valid_taxa_output(capfd):
    galah.galah_config(atlas="Australia", authenticate=True, auth_filename="auth.json")
    counts = galah.atlas_counts(taxa="Macronycteris commersoni")
    out, err = capfd.readouterr()
    assert "We were not" in out


def test_atlas_occurrences_no_valid_taxa_authenticate():
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    occurrences = galah.atlas_occurrences(
        taxa="Macronycteris commersoni",
        filters=["cl22=Tasmania"],
        fields=["scientificName", "decimalLatitude", "decimalLongitude"],
    )
    assert occurrences == None


def test_atlas_occurrences_no_valid_taxa(capfd):
    galah.galah_config(atlas="Australia", email=email_au, authenticate=True, auth_filename="auth.json")
    occurrences = galah.atlas_occurrences(
        taxa="Macronycteris commersoni",
        filters=["cl22=Tasmania"],
        fields=["scientificName", "decimalLatitude", "decimalLongitude"],
    )
    out, err = capfd.readouterr()
    assert "We were not" in out


def test_atlas_counts_galah_config_custom_file_authenticate():
    galah.galah_config(
        atlas="Australia",
        email=email_au,
        config_file="./temp_config_atlas_counts.ini",
        authenticate=True,
        auth_filename="auth.json",
    )
    counts = galah.atlas_counts(config_file="./temp_config_atlas_counts.ini")
    assert counts["totalRecords"][0] > 0


def test_atlas_occurrences_galah_config_custom_file_authenticate():
    galah.galah_config(
        atlas="Australia",
        email=email_au,
        config_file="./temp_config_atlas_occurrences.ini",
        authenticate=True,
        auth_filename="auth.json",
    )
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes", config_file="./temp_config_atlas_occurrences.ini")
    assert occurrences.shape[0] > 0


def test_atlas_media_galah_config_custom_file_authenticate():
    galah.galah_config(
        atlas="Australia",
        email=email_au,
        config_file="./temp_config_atlas_media.ini",
        authenticate=True,
        auth_filename="auth.json",
    )
    filters = ["year=2020", "decimalLongitude>153.0"]
    output = galah.atlas_media(
        taxa="Ornithorhynchus anatinus",
        filters=filters,
        config_file="./temp_config_atlas_media.ini",
        authenticate=True,
        auth_filename="auth.json",
    )
    assert output.shape[0] > 0


def test_atlas_species_Australia_species_australia_galah_config_custom_file_authenticate():
    galah.galah_config(
        atlas="Australia",
        email=email_au,
        config_file="./temp_config_atlas_species.ini",
        authenticate=True,
        auth_filename="auth.json",
    )
    taxa = "Heleioporus"
    species_table = galah.atlas_species(taxa=taxa, config_file="./temp_config_atlas_species.ini")
    assert species_table.shape[0] > 0


#'''
