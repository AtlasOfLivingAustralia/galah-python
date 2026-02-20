import configparser
import os
import shutil

import galah

configParser = configparser.ConfigParser()
configParser.read("logins.txt")
email_se = configParser["Sweden"]["email"]

galah.galah_config(authenticate=False)


######################################
# show_all
######################################
def test_show_all_assertions_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.show_all(assertions=True)
    assert output.shape[1] > 1


def test_show_all_atlases_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1


def test_show_all_apis_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1


def test_show_all_collection_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.show_all(collection=True)
    assert output.shape[1] > 0


def test_show_all_datasets_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1


def test_show_all_fields_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1


def test_show_all_providers_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1


def test_show_all_ranks_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1


######################################
# search_all
######################################
def test_search_all_assertions_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="collection")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_assertions_column_name_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="status", column_name="name")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Sweden")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_column_name_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Sweden", column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Sweden")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_column_name_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection", column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_column_name_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Diversity")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_column_name_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_column_name_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="layer", column_name="type")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_column_name_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_column_name_sweden():
    galah.galah_config(atlas="Sweden")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0", column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]


######################################
# show_values
######################################
def test_show_values_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.show_values(field="basis_of_record")
    assert output.shape[0] > 0


######################################
# search_values
######################################
def test_search_values_sweden():
    galah.galah_config(atlas="Sweden")
    first_output = galah.show_values(field="basis_of_record")
    second_output = galah.search_values(field="basis_of_record", value="Obs")
    assert first_output.shape[0] > second_output.shape[0]


######################################
# search_taxa
######################################
def test_search_taxa_sweden():
    galah.galah_config(atlas="Sweden")
    output = galah.search_taxa("Alces alces")
    assert output["taxonConceptID"][0] != None


######################################
# atlas_counts
######################################
def test_atlas_counts_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    assert galah.atlas_counts(taxa)["totalRecords"][0] > 0


def test_atlas_counts_filters_sweden():
    galah.galah_config(atlas="Sweden")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_filters_groupby_expand_sweden():
    galah.galah_config(atlas="Sweden")
    f = "year=2022"
    groups = ["month", "basis_of_record"]
    filtered_counts = galah.atlas_counts(filters=f, group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_filters_groupby_sweden():
    galah.galah_config(atlas="Sweden")
    f = "year=2022"
    groups = ["month", "basis_of_record"]
    filtered_counts = galah.atlas_counts(filters="year=2022", group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_taxa_filter_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filter_empty_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    filter1 = "year="
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa=taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    f = ["year >=2018", "year <= 2022", "year!=2020"]
    assert galah.atlas_counts(taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filters_separate_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus"]
    f = ["basis_of_record = HumanObservation", "year>=2000"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f, group_by="species")
    assert output.shape[0] > 0


def test_atlas_counts_taxa_group_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    group_by = "year"
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_groups_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_groups_expand_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_filters_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filters_group_by_no_expand_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces alces"
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    assert galah.atlas_counts(taxa_array)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_group_by_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_multiple_taxa_filter_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filter_group_by_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    filter1 = "year=2020"
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa_array, filters=filter1, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa_array, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filters_group_by_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    filters = ["year>2010", "basis_of_record=HumanObservation"]
    group_by = ["month", "year"]
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_invalid_multiple_taxa_separate_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_separate_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()


def test_atlas_counts_multiple_taxa_filters_separate_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    f = ["basis_of_record=HumanObservation", "year>=2020"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_separate_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    f = ["basis_of_record=HumanObservation", "year>=2020"]
    group_by = ["month", "species"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()


def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    f = ["basis_of_record=HumanObservation"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_sweden():
    galah.galah_config(atlas="Sweden")
    taxa_array = ["Alces alces", "Carcinus maenas", "Sorex araneus", "Oniscus asellus"]
    f = ["basis_of_record=HumanObservation", "year=2022"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert output["count"][0] >= 0


######################################
# atlas_species
######################################
def test_atlas_species_Sweden_species_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Alces Alces"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_Sweden_family_sweden():
    galah.galah_config(atlas="Sweden")
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


######################################
# atlas_occurrences
######################################
def test_atlas_occurrences_taxa_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    occurrences = galah.atlas_occurrences(taxa="Alces alces")
    assert occurrences.shape[0] > 1


def test_atlas_occurrences_taxa_fields_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    occurrences = galah.atlas_occurrences(taxa="Alces alces", fields=["decimalLatitude", "decimalLongitude"])
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    occurrences1 = galah.atlas_occurrences(taxa="Alces alces")
    occurrences2 = galah.atlas_occurrences(taxa="Alces alces", filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filter_fields_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    occurrences = galah.atlas_occurrences(
        taxa="Alces alces",
        filters="year=2020",
        fields=["decimalLatitude", "decimalLongitude"],
    )
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    filters = ["year>2018", "basis_of_record=HumanObservation"]
    occurrences1 = galah.atlas_occurrences(taxa="Alces alces")
    occurrences2 = galah.atlas_occurrences(taxa="Alces alces", filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filters_fields_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    occurrences = galah.atlas_occurrences(
        taxa="Alces alces",
        filters=["year>2018", "basis_of_record=HumanObservation"],
        fields=["decimalLatitude", "decimalLongitude"],
    )
    assert occurrences.shape[1] == 2


######################################
# atlas_media
######################################


# test if it can get a taxa and return output
def test_atlas_media_taxa_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    output = galah.atlas_media(taxa="Alces alces")
    assert output.shape[0] > 1


# test if the filters component of atlas_media is working
def test_atlas_media_filters_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    raw_output = galah.atlas_media(taxa="Alces alces")
    filtered_output = galah.atlas_media(taxa="Alces alces", filters="decimalLatitude<-24.0")
    assert raw_output.shape[0] > filtered_output.shape[0]


def test_atlas_media_multimedia_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    multimedia_output = galah.atlas_media(taxa="Alces alces", multimedia="images")
    assert multimedia_output.shape[0] > 0


def test_atlas_media_filters_multimedia_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    raw_output = galah.atlas_media(taxa="Alces alces")
    multimedia_output = galah.atlas_media(taxa="Alces alces", filters="decimalLatitude<=-24.0", multimedia="images")
    assert raw_output.shape[0] > multimedia_output.shape[0]


def test_atlas_media_filters_multimedia_collect_path_sweden():
    galah.galah_config(atlas="Sweden", email=email_se)
    path = "test"
    if os.path.isdir("test"):
        shutil.rmtree("test")
    os.mkdir("test")
    multimedia_output = galah.atlas_media(
        taxa="Alces alces",
        multimedia="images",
        filters="decimalLatitude<=-24.0",
        collect=True,
        path=path,
    )
    files = os.listdir(path)
    assert len(files) > 0


# """
