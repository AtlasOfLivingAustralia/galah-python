import configparser
import os
import shutil

import galah
import pytest

configParser = configparser.ConfigParser()
configParser.read("logins.txt")
email_fl = configParser["Flanders"]["email"]

######################################
# exceptions and errors
######################################


#'''
######################################
# show_all
######################################
def test_show_all_assertions_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(assertions=True)
    assert output.shape[1] > 1


def test_show_all_atlases_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1


def test_show_all_apis_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1


def test_show_all_collection_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(collection=True)
    assert output.shape[1] > 1


def test_show_all_datasets_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1


def test_show_all_fields_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1


def test_show_all_lists_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(lists=True)
    assert output.shape[1] > 1


def test_show_all_licences_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(licences=True)
    assert output.shape[1] > 1


def test_show_all_providers_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1


def test_show_all_ranks_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1


def test_show_all_reasons_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_all(reasons=True)
    assert output.shape[1] > 1


######################################
# search_all
######################################
def test_search_all_assertions_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="ambiguousName")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_assertions_column_name_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="coll", column_name="name")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Flanders")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_column_name_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Flanders", column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Flanders")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_column_name_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection", column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_column_name_flanders():
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Nacional")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_column_name_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_column_name_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="basis", column_name="description")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_lists_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="Quadrat")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_lists_column_name_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="SPATIAL", column_name="listType")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_column_name_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_column_name_flanders():
    galah.galah_config(atlas="Flanders")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0", column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]


######################################
# show_values
######################################
def test_show_values_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.show_values(field="basis_of_record")
    assert output.shape[0] > 0


######################################
# search_values
######################################
def test_search_values_flanders():
    galah.galah_config(atlas="Flanders")
    first_output = galah.show_values(field="basis_of_record")
    second_output = galah.search_values(field="basis_of_record", value="obs")
    assert first_output.shape[0] > second_output.shape[0]


######################################
# search_taxa
######################################
def test_search_taxa_flanders():
    galah.galah_config(atlas="Flanders")
    output = galah.search_taxa("Columba palumbus")
    assert output["taxonConceptID"][0] != None


######################################
# atlas_counts
######################################
def test_atlas_counts_flanders():
    galah.galah_config(atlas="Flanders")
    taxa = "Columba palumbus"
    assert galah.atlas_counts(taxa)["totalRecords"][0] > 0


def test_atlas_counts_filters_flanders():
    galah.galah_config(atlas="Flanders")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_filters_groupby_expand_flanders():
    galah.galah_config(atlas="Flanders")
    f = "year=2022"
    groups = ["month", "basisOfRecord"]
    filtered_counts = galah.atlas_counts(filters=f, group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_filters_groupby_flanders():
    galah.galah_config(atlas="Flanders")
    f = "year=2022"
    groups = ["month", "basis_of_record"]
    filtered_counts = galah.atlas_counts(filters="year=2022", group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_taxa_filter_flanders():
    galah.galah_config(atlas="Flanders")
    taxa = "Columba palumbus"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filter_empty_flanders():
    galah.galah_config(atlas="Flanders")
    taxa = "Columba palumbus"
    filter1 = "year="
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_astlas_counts_taxa_same_filter_flanders():
    galah.galah_config(atlas="Flanders")
    taxa = "Columba palumbus"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filters_flanders_total_group_by():
    galah.galah_config(atlas="Flanders")
    output = galah.atlas_counts(taxa="Reptilia", filters="year=2020", group_by="species", total_group_by=True)
    assert output.shape[0] == 1
    assert output["count"][0] > 0


def test_atlas_counts_multiple_taxa_filters_separate_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    f = ["basis_of_record = HumanObservation", "year=2022"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f, group_by="species")
    assert output.shape[0] > 0


def test_atlas_counts_taxa_group_flanders():
    galah.galah_config(atlas="Flanders")
    taxa = "Columba palumbus"
    group_by = "year"
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_groups_expand_flanders():
    galah.galah_config(atlas="Flanders")
    taxa = "Columba palumbus"
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_filters_flanders():
    galah.galah_config(atlas="Flanders")
    taxa = "Columba palumbus"
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filters_group_by_no_expand_flanders():
    galah.galah_config(atlas="Flanders")
    taxa = "Columba palumbus"
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    assert galah.atlas_counts(taxa_array)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_group_by_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_multiple_taxa_filter_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filter_group_by_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    filter1 = "year=2020"
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa_array, filters=filter1, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa_array, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filters_group_by_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    filters = ["year>2010", "basis_of_record=HumanObservation"]
    group_by = ["species", "month"]
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


"""
## TODO: LATER
# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_flanders2_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus","Larus fuscus","Larus argentatus"]
    filters = ["year>2010", "basis_of_record=HumanObservation"]
    group_by = ["state","year"] # may have to change this
    # county** , associatedOrganisms , day , decade
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1
#"""


def test_atlas_counts_invalid_multiple_taxa_separate_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = [
        "Columba palumbus",
        "Larus fuscus",
        "Larus argentatus",
        "Vulpes vulpes",
    ]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_separate_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()


def test_atlas_counts_multiple_taxa_filters_separate_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    f = ["basis_of_record = HumanObservation", "year=2019"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_separate_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    f = ["basis_of_record = HumanObservation", "year=2019"]
    group_by = ["month", "species"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()


def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    f = ["basis_of_record = HumanObservation"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_flanders():
    galah.galah_config(atlas="Flanders")
    taxa_array = ["Columba palumbus", "Larus fuscus", "Larus argentatus"]
    f = ["basis_of_record = HumanObservation", "year=2022"]
    group_by = ["year", "species"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert output["count"][0] >= 0


######################################
# atlas_species
######################################
def test_atlas_species_Flanders_species_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    taxa = "Ramphastos"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_Flanders_species_rank_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    taxa = "Ramphastos"
    species_table = galah.atlas_species(taxa=taxa, rank="subspecies")
    assert species_table.shape[0] > 0


def test_atlas_species_Flanders_family_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    taxa = "Ramphastidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_Flanders_family_rank_genus_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    taxa = "Ramphastidae"
    species_table = galah.atlas_species(taxa=taxa, rank="genus")
    assert species_table.shape[0] > 0


def test_atlas_species_Flanders_family_rank_subspecies_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    taxa = "Ramphastidae"
    species_table = galah.atlas_species(taxa=taxa, rank="subspecies")
    assert species_table.shape[0] > 0


def test_atlas_species_flanders_filter_notaxa():
    galah.galah_config(atlas="Flanders", email=email_fl)
    filtered_species_table = galah.atlas_species(filters=["year=2022", "basis_of_record=HumanObservation"])
    assert filtered_species_table.shape[0] > 0


######################################
# atlas_occurrences
######################################
def test_atlas_occurrences_taxa_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    occurrences = galah.atlas_occurrences(taxa="Columba palumbus")
    assert occurrences.shape[0] > 1


def test_atlas_occurrences_taxa_fields_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    occurrences = galah.atlas_occurrences(taxa="Columba palumbus", fields=["latitude", "longitude"])
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    occurrences1 = galah.atlas_occurrences(taxa="Columba palumbus")
    occurrences2 = galah.atlas_occurrences(taxa="Columba palumbus", filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filter_fields_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    occurrences = galah.atlas_occurrences(
        taxa="Columba palumbus", filters="year=2020", fields=["latitude", "longitude"]
    )
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    filters = ["year>2018", "basis_of_record=HumanObservation"]
    occurrences1 = galah.atlas_occurrences(taxa="Columba palumbus")
    occurrences2 = galah.atlas_occurrences(taxa="Columba palumbus", filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filters_fields_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    occurrences = galah.atlas_occurrences(
        taxa="Columba palumbus",
        filters=["year>2018", "basis_of_record=HumanObservation"],
        fields=["latitude", "longitude"],
    )
    assert occurrences.shape[1] == 2


######################################
# atlas_media
######################################


# test if it can get a taxa and return output
def test_atlas_media_taxa_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    output = galah.atlas_media(taxa="Columba palumbus")
    assert output.shape[0] > 1


# test if the filters component of atlas_media is working
def test_atlas_media_filters_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    raw_output = galah.atlas_media(taxa="Columba palumbus")
    filtered_output = galah.atlas_media(taxa="Columba palumbus", filters="year>=2020")
    assert raw_output.shape[0] > filtered_output.shape[0]


def test_atlas_media_multimedia_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    multimedia_output = galah.atlas_media(taxa="Columba palumbus", multimedia="images")
    assert multimedia_output.shape[0] > 0


def test_atlas_media_filters_multimedia_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    raw_output = galah.atlas_media(taxa="Columba palumbus")
    multimedia_output = galah.atlas_media(taxa="Columba palumbus", filters="year>=2020", multimedia="images")
    assert raw_output.shape[0] > multimedia_output.shape[0]


def test_atlas_media_filters_multimedia_collect_path_flanders():
    galah.galah_config(atlas="Flanders", email=email_fl)
    path = "test"
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.mkdir("test")
    multimedia_output = galah.atlas_media(
        taxa="Columba palumbus",
        multimedia="images",
        filters="year>=2020",
        collect=True,
        path=path,
    )
    files = os.listdir(path)
    assert len(files) > 0


#'''
