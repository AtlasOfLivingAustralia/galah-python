import configparser
import os
import shutil

import galah
import pytest

configParser = configparser.ConfigParser()
configParser.read("logins.txt")
email_uk = configParser["United Kingdom"]["email"]

galah.galah_config(authenticate=False)


######################################
# name change for UK atlas
######################################
def test_change_name_galah_config_UK():
    galah.galah_config(atlas="UK", authenticate=False)
    output = galah.galah_config()
    assert output[output["Configuration"] == "atlas"]["Value"][2] == "United Kingdom"


######################################
# show_all
######################################
def test_show_all_assertions_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.show_all(assertions=True)
    assert output.shape[1] > 1


def test_show_all_atlases_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1


def test_show_all_apis_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1


def test_show_all_collection_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    with pytest.raises(Exception) as e_info:
        galah.show_all(collection=True)
    assert "collections" in str(e_info.value)


def test_show_all_datasets_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1


def test_show_all_fields_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1


def test_show_all_lists_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.show_all(lists=True)
    assert output.shape[1] > 1


def test_show_all_providers_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1


def test_show_all_ranks_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1


######################################
# search_all
######################################
def test_search_all_assertions_uk():
    galah.galah_config(atlas="United Kingdom", reason=10)
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="ambiguousName")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_assertions_column_name_uk():
    galah.galah_config(atlas="United Kingdom", reason=10)
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="coll", column_name="description")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_uk():
    galah.galah_config(atlas="United Kingdom", reason=10)
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="United Kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_column_name_uk():
    galah.galah_config(atlas="United Kingdom", reason=10)
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="United Kingdom", column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_uk():
    galah.galah_config(atlas="United Kingdom", reason=10)
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="United Kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_column_name_uk():
    galah.galah_config(atlas="United Kingdom", reason=10)
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection", column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    with pytest.raises(Exception) as e_info:
        galah.search_all(collection="Agricultural")
    assert "collections" in str(e_info.value)


def test_search_all_collection_column_name_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    with pytest.raises(Exception) as e_info:
        galah.search_all(collection="Agricultural", column_name="id")
    assert "collections" in str(e_info.value)


def test_search_all_datasets_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Nacional")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_column_name_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_column_name_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="basis", column_name="description")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_lists_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="Quadrat")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_lists_column_name_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="SPATIAL", column_name="listType")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_column_name_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_column_name_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0", column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]


######################################
# show_values
######################################
def test_search_values_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.show_values(field="basis_of_record")
    assert output.shape[0] > 0


######################################
# search_values
######################################
def test_search_values_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    first_output = galah.show_values(field="basis_of_record")
    second_output = galah.search_values(field="basis_of_record", value="obs")
    assert first_output.shape[0] > second_output.shape[0]


######################################
# search_taxa
######################################
def test_search_taxa_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.search_taxa("Vulpes vulpes")
    assert output["guid"][0] != None


######################################
# atlas_counts
######################################
def test_atlas_counts_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa = "Vulpes vulpes"
    assert galah.atlas_counts(taxa=taxa)["totalRecords"][0] > 0


def test_atlas_counts_filters_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_filters_groupby_expand_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    f = "year=2022"
    groups = ["month", "basis_of_record"]
    filtered_counts = galah.atlas_counts(filters=f, group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_filters_groupby_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    f = "year=2022"
    groups = ["month", "basis_of_record"]
    filtered_counts = galah.atlas_counts(filters="year=2022", group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_taxa_filter_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filter_empty_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa = "Vulpes vulpes"
    filter1 = "year="
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa = "Vulpes vulpes"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filters_uk_total_group_by():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    output = galah.atlas_counts(taxa="reptilia", filters="year=2020", group_by="species", total_group_by=True)
    assert output.shape[0] == 1
    assert output["count"][0] > 0


def test_atlas_counts_multiple_taxa_filters_separate_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles"]
    f = ["basis_of_record = HumanObservation", "year=2022"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f, group_by="species")
    assert output.shape[0] > 0


def test_atlas_counts_taxa_group_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa = "Vulpes vulpes"
    group_by = "year"
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_groups_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa = "Vulpes vulpes"
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_groups_expand_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa = "Vulpes vulpes"
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_filters_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa = "Vulpes vulpes"
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filters_group_by_no_expand_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa = "Vulpes vulpes"
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    assert galah.atlas_counts(taxa_array)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_group_by_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_multiple_taxa_filter_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filter_group_by_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    filter1 = "year=2020"
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa_array, filters=filter1, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa_array, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filters_group_by_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    filters = ["year>2010", "basis_of_record=HumanObservation"]
    group_by = ["species", "month"]
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_uk2_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    filters = ["year>2010", "basis_of_record=HumanObservation"]
    group_by = ["state", "year"]
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_invalid_multiple_taxa_separate_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri", "Vulpes vulpes"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_separate_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()


def test_atlas_counts_multiple_taxa_filters_separate_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles"]
    f = ["basis_of_record = HumanObservation", "year=2019"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_separate_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    f = ["basis_of_record = HumanObservation", "year=2019"]
    group_by = ["month", "species"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()


def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    f = ["basis_of_record = HumanObservation"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_uk():
    galah.galah_config(atlas="United Kingdom", authenticate=False)
    taxa_array = ["Vulpes vulpes", "Meles meles", "Physoderma potteri"]
    f = ["basis_of_record = HumanObservation", "year=2022"]
    group_by = ["year", "species"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert output["count"][0] >= 0


######################################
# atlas_species
######################################
def test_atlas_species_United_Kingdom_species_uk():
    galah.galah_config(atlas="United Kingdom", reason=10)
    taxa = "Vulpes"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_United_Kingdom_family_uk():
    galah.galah_config(atlas="United Kingdom", reason=10)
    taxa = "Vulpes"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_United_Kingdom_family_rank_genus_uk():
    galah.galah_config(atlas="United Kingdom", reason=10)
    taxa = "Vulpes"
    species_table = galah.atlas_species(taxa=taxa, rank="genus")
    assert species_table.shape[0] > 0


def test_atlas_species_uk_filter_notaxa():
    galah.galah_config(atlas="United Kingdom", reason=10)
    filtered_species_table = galah.atlas_species(filters=["year=2022", "basis_of_record=HumanObservation"])
    assert filtered_species_table.shape[0] > 0


######################################
# atlas_occurrences
######################################
def test_atlas_occurrences_taxa_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk, reason="10")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes")
    assert occurrences.shape[0] > 1


def test_atlas_occurrences_taxa_fields_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk, reason="10")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes", fields=["decimalLatitude", "decimalLongitude"])
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk, reason="10")
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes", filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filter_fields_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk, reason="10")
    occurrences = galah.atlas_occurrences(
        taxa="Vulpes vulpes", filters="year=2020", fields=["decimalLatitude", "decimalLongitude"]
    )
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters2_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk, reason="10")
    filters = ["year>2018", "basisOfRecord=HUMAN_OBSERVATION"]
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes", filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filters_fields_uk2():
    galah.galah_config(atlas="United Kingdom", email=email_uk, reason="10")
    occurrences = galah.atlas_occurrences(
        taxa="Vulpes vulpes",
        filters=["year>2018", "basis_of_record=HumanObservation"],
        fields=["decimalLatitude", "decimalLongitude"],
    )
    assert occurrences.shape[1] == 2


######################################
# atlas_media
######################################


# test if it can get a taxa and return output
def test_atlas_media_taxa_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk)
    output = galah.atlas_media(taxa="Vulpes vulpes")
    assert output.shape[0] > 1


# test if the filters component of atlas_media is working
def test_atlas_media_filters_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk)
    raw_output = galah.atlas_media(taxa="Vulpes vulpes")
    filtered_output = galah.atlas_media(taxa="Vulpes vulpes", filters="year>=2024")
    assert raw_output.shape[0] > filtered_output.shape[0]


def test_atlas_media_multimedia_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk)
    multimedia_output = galah.atlas_media(taxa="Vulpes vulpes", multimedia="images")
    assert multimedia_output.shape[0] > 0


def test_atlas_media_filters_multimedia_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk)
    raw_output = galah.atlas_media(taxa="Vulpes vulpes")
    multimedia_output = galah.atlas_media(taxa="Vulpes vulpes", filters="year>=2024", multimedia="images")
    assert raw_output.shape[0] > multimedia_output.shape[0]


def test_atlas_media_filters_multimedia_collect_path_uk():
    galah.galah_config(atlas="United Kingdom", email=email_uk)
    path = "test"
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.mkdir("test")
    multimedia_output = galah.atlas_media(
        taxa="Vulpes vulpes",
        multimedia="images",
        filters="year>=2024",
        collect=True,
        path=path,
    )
    files = os.listdir(path)
    assert len(files) > 0


# """
