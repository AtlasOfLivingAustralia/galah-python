import configparser
import os
import shutil

import galah
import pytest

configParser = configparser.ConfigParser()
configParser.read("logins.txt")
email_kew = configParser["Kew"]["email"]

galah.galah_config(authenticate=False)

######################################
# exceptions and errors
######################################


#'''
######################################
# show_all
######################################
def test_show_all_assertions_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_all(assertions=True)
    assert output.shape[1] > 1


def test_show_all_atlases_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1


def test_show_all_apis_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1


def test_show_all_collection_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_all(collection=True)
    assert output.shape[1] > 1


def test_show_all_datasets_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1


def test_show_all_fields_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1


def test_show_all_providers_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1


def test_show_all_ranks_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1


def test_show_all_reasons_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_all(reasons=True)
    assert output.shape[1] > 1


######################################
# search_all
######################################
def test_search_all_assertions_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="ambiguousName")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_assertions_column_name_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="coll", column_name="description")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Kew")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_column_name_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Kew", column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Kew")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_column_name_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection", column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_column_name_kew():
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Aca")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_column_name_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="dr11", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_column_name_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="basis", column_name="description")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_column_name_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_column_name_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0", column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_reasons_kew():
    galah.galah_config(atlas="Kew")
    output = galah.search_all(reasons="con")
    assert output.shape[1] > 1


def test_search_all_reasons_column_name_kew():
    galah.galah_config(atlas="Kew")
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="0", column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]


######################################
# show_values
######################################
def test_show_values_kew():
    galah.galah_config(atlas="Kew")
    output = galah.show_values(field="basis_of_record")
    assert output.shape[0] > 0


######################################
# search_values
######################################
def test_search_values_kew():
    galah.galah_config(atlas="Kew")
    first_output = galah.show_values(field="basis_of_record")
    second_output = galah.search_values(field="basis_of_record", value="obs")
    assert first_output.shape[0] > second_output.shape[0]


######################################
# search_taxa
######################################
def test_search_taxa_kew():
    galah.galah_config(atlas="Kew")
    output = galah.search_taxa("Hypoestes forskaolii")
    assert output["guid"][0] != None


######################################
# atlas_counts
######################################
def test_atlas_counts_kew():
    galah.galah_config(atlas="Kew")
    taxa = "Hypoestes forskaolii"
    assert galah.atlas_counts(taxa=taxa)["totalRecords"][0] > 0


def test_atlas_counts_filters_kew():
    galah.galah_config(atlas="Kew")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_filters_groupby_expand_kew():
    galah.galah_config(atlas="Kew")
    f = "year=2022"
    groups = ["month", "basis_of_record"]
    filtered_counts = galah.atlas_counts(filters=f, group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_filters_groupby_kew():
    galah.galah_config(atlas="Kew")
    groups = ["month", "basis_of_record"]
    filtered_counts = galah.atlas_counts(filters="year=2022", group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_taxa_filter_kew():
    galah.galah_config(atlas="Kew")
    taxa = "Hypoestes forskaolii"
    filter1 = "year=2021"
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filter_empty_kew():
    galah.galah_config(atlas="Kew")
    taxa = "Hypoestes forskaolii"
    filter1 = "year="
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_kew():
    galah.galah_config(atlas="Kew")
    taxa = "Hypoestes forskaolii"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filters_kew_total_group_by():
    galah.galah_config(atlas="Kew")
    output = galah.atlas_counts(taxa="Acanthaceae", filters="year>=2020", group_by="species", total_group_by=True)
    assert output.shape[0] == 1
    assert output["count"][0] > 0


def test_atlas_counts_multiple_taxa_filters_separate_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis"]
    f = ["basisOfRecord = PRESERVED_SPECIMEN", "year>=2020"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f, group_by="species")
    assert output.shape[0] > 0


def test_atlas_counts_taxa_group_kew():
    galah.galah_config(atlas="Kew")
    taxa = "Hypoestes forskaolii"
    group_by = "year"
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_groups_kew():
    galah.galah_config(atlas="Kew")
    taxa = "Hypoestes forskaolii"
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_groups_expand_kew():
    galah.galah_config(atlas="Kew")
    taxa = "Hypoestes forskaolii"
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_filters_group_by_kew():
    galah.galah_config(atlas="Kew")
    taxa = "Hypoestes forskaolii"
    filters = ["year>=2020", "basisOfRecord=PRESERVED_SPECIMEN"]
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    assert galah.atlas_counts(taxa_array)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_group_by_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_multiple_taxa_filter_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    filter1 = "year>=2020"
    assert galah.atlas_counts(taxa_array, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filter_group_by_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    filter1 = "year>=2020"
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa_array, filters=filter1, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    filters = ["year>=2020", "basisOfRecord=PRESERVED_SPECIMEN"]
    assert galah.atlas_counts(taxa_array, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filters_group_by_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    filters = ["year>=2020", "basisOfRecord=PRESERVED_SPECIMEN"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    filters = ["year>2010", "basisOfRecord=PRESERVED_SPECIMEN"]
    group_by = ["species", "month"]
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_kew2_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    filters = ["year>2010", "basisOfRecord=PRESERVED_SPECIMEN"]
    group_by = ["month", "year"]
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_invalid_multiple_taxa_separate_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa", "Hypoestes forskaolii"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_separate_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_separate_kew():
    galah.galah_config(atlas="Kew")
    taxa_array = ["Hypoestes forskaolii", "Galanthus nivalis", "Curcuma longa"]
    f = ["year>=2019"]
    group_by = ["month", "species"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()


######################################
# atlas_species
######################################
def test_atlas_species_species_kew():
    galah.galah_config(atlas="Kew", email=email_kew, reason=10)
    taxa = "Hypoestes"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_family_kew():
    galah.galah_config(atlas="Kew", email=email_kew, reason=10)
    taxa = "Acanthaceae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_family_rank_genus_kew():
    galah.galah_config(atlas="Kew", email=email_kew, reason=10)
    taxa = "Acanthaceae"
    species_table = galah.atlas_species(taxa=taxa, rank="genus")
    assert species_table.shape[0] > 0


def test_atlas_species_kew_filter_notaxa():
    galah.galah_config(atlas="Kew", email=email_kew, reason=10)
    filtered_species_table = galah.atlas_species(filters=["year=2022", "basisOfRecord=PRESERVED_SPECIMEN"])
    assert filtered_species_table.shape[0] > 0


######################################
# atlas_occurrences
######################################
def test_atlas_occurrences_taxa_kew():
    galah.galah_config(atlas="Kew", email=email_kew, reason="10")
    occurrences = galah.atlas_occurrences(taxa="Hypoestes forskaolii")
    assert occurrences.shape[0] > 1


def test_atlas_occurrences_taxa_fields_kew():
    galah.galah_config(atlas="Kew", email=email_kew, reason="10")
    occurrences = galah.atlas_occurrences(taxa="Hypoestes forskaolii", fields=["decimalLatitude", "decimalLongitude"])
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_kew():
    galah.galah_config(atlas="Kew", email=email_kew, reason="10")
    occurrences1 = galah.atlas_occurrences(taxa="Hypoestes forskaolii")
    occurrences2 = galah.atlas_occurrences(taxa="Hypoestes forskaolii", filters="year>=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filter_fields_kew():
    galah.galah_config(atlas="Kew", email=email_kew, reason="10")
    occurrences = galah.atlas_occurrences(
        taxa="Hypoestes forskaolii", filters="year>=2020", fields=["decimalLatitude", "decimalLongitude"]
    )
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters2_kew():
    galah.galah_config(atlas="Kew", email=email_kew, reason="10")
    filters = ["year>2018", "basisOfRecord=HUMAN_OBSERVATION"]
    occurrences1 = galah.atlas_occurrences(taxa="Hypoestes forskaolii")
    occurrences2 = galah.atlas_occurrences(taxa="Hypoestes forskaolii", filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filters_fields_kew2():
    galah.galah_config(atlas="Kew", email=email_kew, reason="10")
    occurrences = galah.atlas_occurrences(
        taxa="Hypoestes forskaolii",
        filters=["year>2018", "basisOfRecord=PRESERVED_SPECIMEN"],
        fields=["decimalLatitude", "decimalLongitude"],
    )
    assert occurrences.shape[1] == 2


######################################
# atlas_media
######################################
def test_atlas_media_taxa_kew():
    galah.galah_config(atlas="Kew", email=email_kew)  # verbose=True,
    media = galah.atlas_media(taxa="Hypoestes forskaolii", filters="year>2010")
    assert media.shape[0] > 0


# test if the filters component of atlas_media is working
def test_atlas_media_filters_kew():
    galah.galah_config(atlas="Kew", email=email_kew)
    raw_output = galah.atlas_media(taxa="Hypoestes forskaolii")
    filtered_output = galah.atlas_media(taxa="Hypoestes forskaolii", filters="year>=2020")
    assert raw_output.shape[0] > filtered_output.shape[0]


def test_atlas_media_multimedia_kew():
    galah.galah_config(atlas="Kew", email=email_kew)
    multimedia_output = galah.atlas_media(taxa="Hypoestes forskaolii", multimedia="images")
    assert multimedia_output.shape[0] > 0


def test_atlas_media_filters_multimedia_kew():
    galah.galah_config(atlas="Kew", email=email_kew)
    raw_output = galah.atlas_media(taxa="Hypoestes forskaolii")
    multimedia_output = galah.atlas_media(taxa="Hypoestes forskaolii", filters="year>=2020", multimedia="images")
    assert raw_output.shape[0] > multimedia_output.shape[0]


def test_atlas_media_filters_multimedia_collect_path_kew():
    galah.galah_config(atlas="Kew", email=email_kew)
    path = "test"
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.mkdir("test")
    multimedia_output = galah.atlas_media(
        taxa="Hypoestes forskaolii",
        multimedia="images",
        filters="year>=2020",
        collect=True,
        path=path,
    )
    files = os.listdir(path)
    assert len(files) > 0


#'''
