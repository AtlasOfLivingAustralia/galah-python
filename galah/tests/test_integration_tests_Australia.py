import configparser
import os
import shutil

import galah
import geopandas as gpd
import pandas as pd
import pytest
import shapely

email_au = "ala4r@ala.org.au"

# """
######################################
# exceptions and errors
######################################
def test_no_dataframe():
    with pytest.raises(Exception) as e_info:
        galah.show_all(assertions="Yes")
    assert "True and False" in str(e_info.value)


def test_show_all_collection_non_atlas():
    galah.galah_config(atlas="A")
    with pytest.raises(Exception) as e_info:
        galah.show_all(collection=True)
    assert "account" in str(e_info.value)


def test_nonexistent_atlas_assertions():
    galah.galah_config(atlas="A")
    with pytest.raises(Exception) as e_info:
        galah.show_all(assertions=True)
    assert "taken into account" in str(e_info.value)


def test_show_values_australia_fields_none():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.show_values(field=None)
    assert "specify" in str(e_info.value)


def test_show_values_australia_fields_number():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.show_values(field=1)
    assert "string" in str(e_info.value)


def test_empty_galah_config():
    if os.path.isfile("test.ini"):
        os.remove("test.ini")
    os.system("touch test.ini")
    galah.galah_config(config_file="test.ini")
    assert os.path.isfile("test.ini")


def test_empty_galah_config_raise_error():
    if os.path.isfile("test.ini"):
        os.remove("test.ini")
    with pytest.raises(Exception) as e_info:
        galah.galah_config(config_file="test.ini")
    assert "config" in str(e_info.value)


def test_search_values_australia_field_none():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_values(field=None, value="temp")
    assert "field" in str(e_info.value)


def test_search_values_australia_value_none():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_values(field="basisOfRecord", value=None)
    assert "specify" in str(e_info.value)


def test_search_values_australia_value_number():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_values(field="basisOfRecord", value=1)
    assert "string" in str(e_info.value)


def test_search_values_australia_value_multiple():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_values(field="basisOfRecord", value=[1, 2])
    assert "string" in str(e_info.value)


def test_galah_geolocate_bad_string():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts(polygon="basisOfRecord")
    assert "shape" in str(e_info.value)


def test_galah_geolocate_polygon_non_string():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts(polygon=1)
    assert "str and polygons" in str(e_info.value)


def test_galah_geolocate_bbox_non_string():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts(bbox=1)
    assert "dicts and polygons" in str(e_info.value)


def test_search_all_assertions_non_string():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_all(assertions=True)
    assert "strings" in str(e_info.value)


def test_search_all_assertions_column_name_non_string():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_all(assertions="Non", column_name=1)
    assert "strings" in str(e_info.value)


def test_search_values_column_name_non_string():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_values(field="basisOfRecord", value="human", column_name=1)
    assert "strings" in str(e_info.value)


def test_search_values_value_non_string():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_values(field="basisOfRecord", value=1)
    assert "string" in str(e_info.value)


def test_galah_search_all_assertions_wrong_type():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_all(assertions=True)
    assert "string" in str(e_info.value)


def test_galah_show_all_invalid_atlas():
    galah.galah_config(atlas="A")
    with pytest.raises(Exception) as e_info:
        galah.show_all(datasets=True)
    assert "account" in str(e_info.value)


def test_galah_atlas_occurrences_invalid_email():
    galah.galah_config(email="", atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.atlas_occurrences(taxa="Vulpes vulpes")
    assert "email" in str(e_info.value)


def test_atlas_counts_invalid_filters():
    galah.galah_config(atlas="Australia", email=email_au)
    with pytest.raises(Exception) as e_info:
        galah.atlas_occurrences(filters=1998)
    assert "filters" in str(e_info.value)


def test_atlas_counts_invalid_filters_list():
    galah.galah_config(atlas="Australia", email=email_au)
    with pytest.raises(Exception) as e_info:
        galah.atlas_occurrences(filters=[1998])
    assert "filters" in str(e_info.value)


def test_search_taxa_check_taxa_type():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_taxa(taxa=1998)
    assert "taxa" in str(e_info.value)


def test_search_taxa_no_arguments():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_taxa()
    assert "specify" in str(e_info.value)


def test_search_taxa_specific_epithet_error():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_taxa(specific_epithet={"species": "Vulpes vulpes"})
    assert "specificEpithet" in str(e_info.value)


def test_search_taxa_scientific_name_no_scientificName():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_taxa(scientific_name={"species": "Vulpes vulpes"})
    assert "scientificName" in str(e_info.value)


def test_search_taxa_scientific_name_wrong_type():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_taxa(scientific_name=["scientificName", "Vulpes vulpes"])
    assert "scientific_name" in str(e_info.value)


def test_search_taxa_scientific_name_dict_length_not_equal():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.search_taxa(scientific_name={"scientificName": "Vulpes vulpes", "genus": ["Vulpes", "Vulpes"]})
    assert "dictionary" in str(e_info.value)


def test_search_taxa_homonyms():
    galah.galah_config(atlas="Australia")
    mg = galah.search_taxa(taxa="Morganella")
    assert mg.empty


def test_galah_group_by_more_than_2():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts(group_by=["year", "month", "species"])
    assert "groups" in str(e_info.value)


def test_verbose_atlas_counts(capfd):
    galah.galah_config(atlas="Australia", verbose=True)
    galah.atlas_counts()
    out, err = capfd.readouterr()
    assert "URL" in out


# def test_verbose_payload(capfd):
#     galah.galah_config(atlas="Australia")
#     galah.atlas_counts(verbose=True)  # Writes "Hello World!" to stdout
#     out, err = capfd.readouterr()
#     assert "URL" in out


def test_incorrect_character_in_filter():
    galah.galah_config(atlas="Australia")
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts(filters="year@")
    assert "filters" in str(e_info.value)


def test_show_all_ranks_invalid_value():
    galah.galah_config(atlas="Australia", ranks="Spain")
    with pytest.raises(Exception) as e_info:
        galah.show_all(ranks=True)
    assert "values" in str(e_info.value)


def test_check_atlas_not_working():
    galah.galah_config(atlas="France")
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts()
    assert "atlas" in str(e_info.value)


######################################
# show_all functions
######################################
def test_show_all_multiple_dataframes():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(assertions=True, apis=True)
    assert len(output) > 1


def test_show_all_assertions_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(assertions=True)
    assert output.shape[1] > 1


def test_show_all_atlases_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1


def test_show_all_apis_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1


def test_show_all_collection_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(collection=True)
    assert output.shape[1] > 1


def test_show_all_datasets_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1


def test_show_all_fields_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1


def test_show_all_licences_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(licences=True)
    assert output.shape[1] > 1


def test_show_all_lists_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(lists=True)
    assert output.shape[1] > 1


def test_show_all_profiles_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(profiles=True)
    assert output.shape[1] > 1


def test_show_all_providers_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1


def test_show_all_ranks_australia():
    galah.galah_config(atlas="Australia", ranks="all")
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1


def test_show_all_reasons_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(reasons=True)
    assert output.shape[1] > 1


######################################
# search_all functions
######################################
def test_search_all_assertions_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="collection")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_assertions_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="status", column_name="name")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Australia")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Australia", column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Australia")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection", column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Torres")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="layer", column_name="type")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_licences_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(licences=True)
    total_search_all = galah.search_all(licences="Creative")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_licences_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(licences=True)
    total_search_all = galah.search_all(licences="CC BY", column_name="acronym")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_lists_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="Quadrat")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_lists_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="SPATIAL", column_name="listType")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_profiles_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(profiles=True)
    total_search_all = galah.search_all(profiles="ALA")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_profiles_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(profiles=True)
    total_search_all = galah.search_all(profiles="ALA", column_name="shortName")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_australia():
    galah.galah_config(atlas="Australia", ranks="all")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_column_name_australia():
    galah.galah_config(atlas="Australia", ranks="all")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="2", column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_reasons_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="conservation")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_reasons_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="1", column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]


######################################
# show_values
######################################
def test_show_values_australia():
    galah.galah_config(atlas="Australia")
    first_output = galah.show_values(field="basisOfRecord")
    assert first_output.shape[0] > 0


def test_show_values_australia_lists():
    galah.galah_config(atlas="Australia")
    first_output = galah.show_values(field="dr656", lists=True)
    assert first_output.shape[0] > 0


def test_show_values_australia_lists_kvp():
    galah.galah_config(atlas="Australia")
    first_output = galah.show_values(field="dr656", lists=True)
    second_output = galah.show_values(field="dr656", lists=True, all_fields=True)
    assert first_output.shape[1] < second_output.shape[1]  # change to 0 if this isn't working


######################################
# search_values
######################################
def test_search_values_australia():
    galah.galah_config(atlas="Australia")
    first_output = galah.show_values(field="basisOfRecord")
    second_output = galah.search_values(field="basisOfRecord", value="OBS")
    assert first_output.shape[0] > second_output.shape[0]


######################################
# search_taxa
######################################
def test_search_taxa_australia():
    galah.galah_config(atlas="Australia")
    output = galah.search_taxa("Vulpes vulpes")
    assert output["taxonConceptID"][0] != None


def test_search_taxa_australia_two_taxa():
    galah.galah_config(atlas="Australia")
    output = galah.search_taxa(["Vulpes vulpes", "Osphranter rufus"])
    assert output["taxonConceptID"][0] != None


def test_search_taxa_australia_identifiers():
    galah.galah_config(atlas="Australia")
    output = galah.search_taxa(identifiers="https://id.biodiversity.org.au/node/apni/2914510")
    assert output["taxonConceptID"][0] != None


def test_search_taxa_australia_specific_epithet():
    galah.galah_config(atlas="Australia")
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


def test_search_taxa_australia_scientific_name():
    galah.galah_config(atlas="Australia")
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
def test_atlas_counts_australia_scientific_name():
    galah.galah_config(atlas="Australia")
    output = galah.atlas_counts(
        scientific_name={
            "family": ["pardalotidae", "maluridae"],
            "scientificName": ["pardolatus striatus", "malurus cyaneus"],
        }
    )
    assert output.shape[0] > 0


def test_atlas_counts_australia_config():
    if os.path.isfile("test.ini"):
        os.remove("test.ini")
    os.system("touch test.ini")
    galah.galah_config(config_file="test.ini", atlas="Australia")
    taxa = "Vulpes vulpes"
    assert galah.atlas_counts(taxa=taxa)["totalRecords"][0] > 0


def test_atlas_counts_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    assert galah.atlas_counts(taxa=taxa)["totalRecords"][0] > 0


def test_atlas_counts_filters_australia():
    galah.galah_config(atlas="Australia")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_or_filters2_australia():
    galah.galah_config(atlas="Australia")
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters="year=[2021,2022]")
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_assertion_as_true_filter_australia():
    galah.galah_config(atlas="Australia")
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters="BASIS_OF_RECORD_INVALID=True")
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_assertion_as_false_filter_australia():
    galah.galah_config(atlas="Australia")
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters="BASIS_OF_RECORD_INVALID=False")
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_or_filters2_australia():
    galah.galah_config(atlas="Australia")
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=["year=2021", "year=2022"])
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_filters_groupby_expand_australia():
    galah.galah_config(atlas="Australia")
    f = "year=2022"
    groups = ["month", "basisOfRecord"]
    filtered_counts = galah.atlas_counts(filters=f, group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_filters_groupby_australia():
    galah.galah_config(atlas="Australia")
    f = "year=2022"
    groups = ["month", "basisOfRecord"]
    filtered_counts = galah.atlas_counts(filters="year=2022", group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_taxa_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa=taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filter_empty_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filter1 = "year="
    assert galah.atlas_counts(taxa=taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa=taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022", "year!=2020"]
    assert galah.atlas_counts(taxa=taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filter_data_quality_australia():
    galah.galah_config(atlas="Australia", data_profile="ALA")
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    no_quality = galah.atlas_counts(taxa, filters=filter1)
    quality = galah.atlas_counts(taxa, filters=filter1, use_data_profile=True)
    assert no_quality["totalRecords"][0] >= quality["totalRecords"][0]


def test_atlas_counts_multiple_taxa_filters_separate_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_taxa_group_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    group_by = "year"
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_groups_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    group_by = ["year", "basisOfRecord"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_groups_expand_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    group_by = ["year", "basisOfRecord"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_filters_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    assert galah.atlas_counts(taxa, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filters_group_by_no_expand_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    group_by = "basisOfRecord"
    output = galah.atlas_counts(taxa, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_filters_australia_total_group_by():
    galah.galah_config(atlas="Australia")
    output = galah.atlas_counts(taxa="reptilia", filters="year=2020", group_by="species", total_group_by=True)
    assert output.shape[0] == 1
    assert output["count"][0] > 0


def test_atlas_counts_multiple_taxa_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    assert galah.atlas_counts(taxa_array)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_multiple_taxa_group_by_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_multiple_taxa_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filter_group_by_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_multiple_taxa_filters_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = [
        "Osphranter rufus",
        "Vulpes vulpes",
        "Macropus giganteus",
        "Phascolarctos cinereus",
    ]
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    assert galah.atlas_counts(taxa_array, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filters_group_by_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_invalid_multiple_taxa_separate_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = [
        "Dasyurus hallucatus",
        "Ailuropoda melanoleuca",
        "Centrostephanus rodgersii",
    ]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_separate_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_multiple_taxa_filters_group_by_separate_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_australia():
    galah.galah_config(atlas="Australia")
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


def test_atlas_counts_geolocate_polygon():
    test_shape = shapely.box(143, -29, 148, -28)
    counts = galah.atlas_counts(polygon=test_shape)
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_bbox():
    test_shape = shapely.box(143, -29, 148, -28)
    counts = galah.atlas_counts(bbox=test_shape)
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_bbox_dict():
    counts = galah.atlas_counts(bbox={"xmin": 143, "ymin": -29, "xmax": 148, "ymax": -28})
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_polygon_taxa():
    test_shape = shapely.box(143, -29, 148, -28)
    counts = galah.atlas_counts(taxa="reptilia", polygon=test_shape)
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_bbox_taxa():
    test_shape = shapely.box(143, -29, 148, -28)
    counts = galah.atlas_counts(taxa="reptilia", bbox=test_shape)
    assert counts["totalRecords"][0] > 0


def test_atlas_counts_geolocate_pandas_polygon_taxa():
    test_shape = pd.DataFrame({"minx": 143, "miny": -29, "maxx": 148, "maxy": -28}, index=[0])
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts(taxa="reptilia", polygon=test_shape)
    assert "str" in str(e_info.value)


def test_atlas_counts_geolocate_pandas_bbox_taxa():
    test_shape = pd.DataFrame({"minx": 143, "miny": -29, "maxx": 148, "maxy": -28}, index=[0])
    counts = galah.atlas_counts(taxa="reptilia", bbox=test_shape)
    assert counts["totalRecords"][0] > 0


def tests_atlas_counts_geolocate_polygon_simplify():
    galah.galah_config(atlas="Australia")
    test_shape = gpd.read_file("nsw_state_polygon_shp/STE_2021_AUST_GDA94.shp")
    test_shape = test_shape.to_crs(4326)
    with pytest.raises(Exception) as e_info:
        galah.atlas_counts(taxa="reptilia", polygon=test_shape)
    assert "variables" in str(e_info.value)


def tests_atlas_counts_geolocate_polygon_simplify_single_shape():
    galah.galah_config(atlas="Australia")
    test_shape = gpd.read_file("nsw_state_polygon_shp/STE_2021_AUST_GDA94.shp")
    test_shape = test_shape.to_crs(4326)
    nsw = str(test_shape[test_shape["STE_NAME21"] == "New South Wales"]["geometry"][0])
    counts = galah.atlas_counts(taxa="reptilia", polygon=nsw, simplify_polygon=True)
    assert counts["totalRecords"][0] > 0


######################################
# atlas_species
######################################
def test_atlas_species_Australia_species_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    taxa = "Heleioporus"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_species_rank_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    taxa = "Vulpes"
    species_table = galah.atlas_species(taxa=taxa, rank="subspecies")
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_family_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_family_rank_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa, rank="genus")
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_family_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa, rank="subspecies")
    assert species_table.shape[0] > 0


def test_atlas_species_Australia_filter():
    galah.galah_config(atlas="Australia", email=email_au)
    full_species_table = galah.atlas_species(taxa="Rodentia")
    filtered_species_table = galah.atlas_species(taxa="Rodentia", filters="stateProvince=Victoria")
    assert full_species_table.shape[0] > filtered_species_table.shape[0]


def test_atlas_species_Australia_filter_notaxa():
    galah.galah_config(atlas="Australia", email=email_au)
    filtered_species_table = galah.atlas_species(filters=["year=2022", "stateProvince=Victoria"])
    assert filtered_species_table.shape[0] > 0


def test_atlas_species_Australia_polygon():
    galah.galah_config(atlas="Australia", email=email_au)
    full_species_table = galah.atlas_species(polygon=shapely.box(143, -29, 148, -28))
    assert full_species_table.shape[0] > 0


def test_atlas_species_Australia_bbox():
    galah.galah_config(atlas="Australia", email=email_au)
    full_species_table = galah.atlas_species(bbox=shapely.box(143, -29, 148, -28))
    assert full_species_table.shape[0] > 0


def test_atlas_species_Australia_filter_polygon():
    galah.galah_config(atlas="Australia", email=email_au)
    full_species_table = galah.atlas_species(polygon=shapely.box(143, -29, 148, -28))
    filtered_species_table = galah.atlas_species(
        polygon=shapely.box(143, -29, 148, -28), filters="stateProvince=Victoria"
    )
    assert full_species_table.shape[0] > filtered_species_table.shape[0]


def test_atlas_species_Australia_filter_polygon():
    galah.galah_config(atlas="Australia", email=email_au)
    full_species_table = galah.atlas_species(bbox=shapely.box(143, -29, 148, -28))
    filtered_species_table = galah.atlas_species(bbox=shapely.box(143, -29, 148, -28), filters="stateProvince=Victoria")
    assert full_species_table.shape[0] > filtered_species_table.shape[0]


def test_atlas_species_Australia_filter_notaxa():
    galah.galah_config(atlas="Australia", email=email_au)
    filtered_species_table = galah.atlas_species(filters=["year=2022", "stateProvince=Victoria"])
    assert filtered_species_table.shape[0] > 0


######################################
# atlas_occurrences
######################################
def test_atlas_occurrences_taxa_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes")
    assert occurrences.shape[0] > 1


def test_atlas_occurrences_taxa_fields_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes", fields=["decimalLatitude", "decimalLongitude"])
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes", filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filter_fields_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    occurrences = galah.atlas_occurrences(
        taxa="Vulpes vulpes",
        filters="year=2020",
        fields=["decimalLatitude", "decimalLongitude"],
    )
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters2_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    filters = ["year>2018", "basisOfRecord=HUMAN_OBSERVATION"]
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes", filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filters_fields_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    occurrences = galah.atlas_occurrences(
        taxa="Vulpes vulpes",
        filters=["year>2018", "basisOfRecord=HUMAN_OBSERVATION"],
        fields=["decimalLatitude", "decimalLongitude"],
    )
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_data_profile_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    galah.galah_config(data_profile="ALA")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes", use_data_profile=True)
    galah.galah_config(data_profile=None)
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_geolocate_polygon():
    galah.galah_config(atlas="Australia", email=email_au)
    test_shape = shapely.box(143, -29, 148, -28)
    occurrences = galah.atlas_occurrences(polygon=test_shape)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_geolocate_bbox():
    galah.galah_config(atlas="Australia", email=email_au)
    test_shape = shapely.box(143, -29, 148, -28)
    occurrences = galah.atlas_occurrences(bbox=test_shape)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_geolocate_bbox_dict():
    galah.galah_config(atlas="Australia", email=email_au)
    occurrences = galah.atlas_occurrences(bbox={"xmin": 143, "ymin": -29, "xmax": 148, "ymax": -28})
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_geolocate_polygon_taxa():
    galah.galah_config(atlas="Australia", email=email_au)
    test_shape = shapely.box(143, -29, 148, -28)
    occurrences = galah.atlas_occurrences(taxa="reptilia", polygon=test_shape)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_geolocate_bbox_taxa():
    galah.galah_config(atlas="Australia", email=email_au)
    test_shape = shapely.box(143, -29, 148, -28)
    occurrences = galah.atlas_occurrences(taxa="reptilia", bbox=test_shape)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_mint_doi():
    galah.galah_config(atlas="Australia", email=email_au)  # ala4r@ala.org.au
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes", mint_doi=True)
    assert occurrences.shape[0] > 0


def test_atlas_occurrences_doi():
    galah.galah_config(atlas="Australia", email=email_au)  # ala4r@ala.org.au
    occurrences = galah.atlas_occurrences(doi="https://doi.org/10.26197/ala.e413b946-8959-41f8-9ae9-897d86029844")
    assert occurrences.shape[0] > 0


######################################
# atlas_media
######################################


# test if it can get a taxa and return output
def test_atlas_media_taxa_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    output = galah.atlas_media(taxa="Liopholis margaretae")
    assert output.shape[0] > 1


# test if the filters component of atlas_media is working
def test_atlas_media_filters_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    raw_output = galah.atlas_media(taxa="Liopholis margaretae")
    filtered_output = galah.atlas_media(taxa="Liopholis margaretae", filters="decimalLatitude<-24.0")
    assert raw_output.shape[0] > filtered_output.shape[0]


def test_atlas_media_multimedia_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    multimedia_output = galah.atlas_media(taxa="Liopholis margaretae", multimedia="images")
    assert multimedia_output.shape[0] > 0


def test_atlas_media_filters_multimedia_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    raw_output = galah.atlas_media(taxa="Liopholis margaretae")
    multimedia_output = galah.atlas_media(
        taxa="Liopholis margaretae", filters="decimalLatitude<=-24.0", multimedia="images"
    )
    assert raw_output.shape[0] > multimedia_output.shape[0]


def test_atlas_media_filters_multimedia_collect_path_australia():
    galah.galah_config(atlas="Australia", email=email_au)
    path = "test"
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.mkdir("test")
    multimedia_output = galah.atlas_media(
        taxa="Liopholis margaretae",
        multimedia="images",
        filters="decimalLatitude<=-24.0",
        collect=True,
        path=path,
    )
    files = os.listdir(path)
    assert len(files) > 0


def test_atlas_counts_no_valid_taxa():
    galah.galah_config(atlas="Australia")
    counts = galah.atlas_counts(taxa="Macronycteris commersoni")
    assert counts == None


def test_atlas_counts_no_valid_taxa_output(capfd):
    galah.galah_config(atlas="Australia")
    counts = galah.atlas_counts(taxa="Macronycteris commersoni")
    out, err = capfd.readouterr()
    assert "We were not" in out


def test_atlas_occurrences_no_valid_taxa():
    galah.galah_config(atlas="Australia", email=email_au)
    occurrences = galah.atlas_occurrences(
        taxa="Macronycteris commersoni",
        filters=["cl22=Tasmania"],
        fields=["scientificName", "decimalLatitude", "decimalLongitude"],
    )
    assert occurrences == None


def test_atlas_occurrences_no_valid_taxa_output(capfd):
    galah.galah_config(atlas="Australia", email=email_au)
    occurrences = galah.atlas_occurrences(
        taxa="Macronycteris commersoni",
        filters=["cl22=Tasmania"],
        fields=["scientificName", "decimalLatitude", "decimalLongitude"],
    )
    out, err = capfd.readouterr()
    assert "We were not" in out


def test_atlas_counts_galah_config_custom_file():
    galah.galah_config(
        atlas="Australia", email=email_au, config_file="./temp_config.ini", authenticate=False
    )
    counts = galah.atlas_counts(config_file="./temp_config.ini")
    assert counts["totalRecords"][0] > 0


def test_atlas_occurrences_galah_config_custom_file():
    galah.galah_config(
        atlas="Australia", email=email_au, config_file="./temp_config.ini", authenticate=False
    )
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes", config_file="./temp_config.ini")
    assert occurrences.shape[0] > 0


def test_atlas_media_galah_config_custom_file():
    galah.galah_config(
        atlas="Australia", email=email_au, config_file="./temp_config.ini", authenticate=False
    )
    filters = ["year=2020", "decimalLongitude>153.0"]
    output = galah.atlas_media(
        taxa="Ornithorhynchus anatinus",
        filters=filters,
        config_file="./temp_config.ini",
    )
    assert output.shape[0] > 0


def test_atlas_species_Australia_species_australia_galah_config_custom_file():
    galah.galah_config(
        atlas="Australia", email=email_au, config_file="./temp_config.ini", authenticate=False
    )
    taxa = "Heleioporus"
    species_table = galah.atlas_species(taxa=taxa, config_file="./temp_config.ini")
    assert species_table.shape[0] > 0


# """
