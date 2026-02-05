import configparser

import galah

configParser = configparser.ConfigParser()
configParser.read("logins.txt")
email_at = configParser["Austria"]["email"]

galah.galah_config(authenticate=False,verbose=False)

######################################
# show_all
######################################
def test_show_all_assertions_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_all(assertions=True)
    assert output.shape[1] > 1


def test_show_all_atlases_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1


def test_show_all_apis_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1


def test_show_all_collection_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_all(collection=True)
    assert output.shape[1] > 1


def test_show_all_datasets_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1


def test_show_all_fields_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1


def test_show_all_lists_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_all(lists=True)
    assert output.shape[1] > 1


def test_show_all_providers_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1


def test_show_all_reasons_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_all(reasons=True)
    assert output.shape[1] > 1


######################################
# search_all
######################################
def test_search_all_assertions_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="collection")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_assertions_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="status", column_name="name")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Austria")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_atlases_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Austria", column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Austria")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_apis_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection", column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_collection_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Rote")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_datasets_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_fields_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="layer", column_name="type")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_lists_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="Quadrat")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_lists_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="SPATIAL", column_name="listType")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_providers_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518", column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_ranks_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0", column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_reasons_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="conservation")
    assert total_search_all.shape[0] < total_show_all.shape[0]


def test_search_all_reasons_column_name_austria():
    galah.galah_config(atlas="Austria")
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="0", column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]


######################################
# show_values
######################################
def test_show_values_austria():
    galah.galah_config(atlas="Austria")
    output = galah.show_values(field="basis_of_record")
    assert output.shape[0] > 0


######################################
# search_values
######################################
def test_search_values_austria():
    galah.galah_config(atlas="Austria")
    first_output = galah.show_values(field="basis_of_record")
    second_output = galah.search_values(field="basis_of_record", value="Obs")
    assert first_output.shape[0] > second_output.shape[0]


######################################
# search_taxa
######################################
def test_search_taxa_austria():
    galah.galah_config(atlas="Austria")
    output = galah.search_taxa("Sehirus luctuosus")
    assert output["guid"][0] != None


def test_atlas_counts_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Sehirus luctuosus"
    assert galah.atlas_counts(taxa)["totalRecords"][0] > 0


def test_atlas_counts_filters_austria():
    galah.galah_config(atlas="Austria")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts["totalRecords"][0] > filtered_counts["totalRecords"][0]


def test_atlas_counts_filters_groupby_expand_austria():
    galah.galah_config(atlas="Austria")
    f = "year=2022"
    groups = ["month", "basis_of_record"]
    filtered_counts = galah.atlas_counts(filters=f, group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_filters_groupby_austria():
    galah.galah_config(atlas="Austria")
    f = "year=2022"
    groups = ["month", "basis_of_record"]
    filtered_counts = galah.atlas_counts(filters="year=2022", group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0


def test_atlas_counts_taxa_filter_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Sehirus luctuosus"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filter_empty_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Sehirus luctuosus"
    filter1 = "year="
    assert galah.atlas_counts(taxa, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Sehirus luctuosus"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_taxa_same_filter_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Sehirus luctuosus"
    f = ["year >=2018", "year <= 2022", "year!=2020"]
    assert galah.atlas_counts(taxa, filters=f)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filters_separate_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Anser anser"]
    f = ["basis_of_record=HumanObservation", "year=2022"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f, group_by="species")
    assert output.shape[0] > 0


def test_atlas_counts_taxa_group_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Sehirus luctuosus"
    group_by = "year"
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_groups_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Sehirus luctuosus"
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_groups_expand_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Anser anser"
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa, group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_taxa_filters_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Sehirus luctuosus"
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_taxa_filters_group_by_no_expand_austria():
    galah.galah_config(atlas="Austria")
    taxa = "Anser anser"
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa, filters=filters, group_by=group_by)
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Anser anser"]
    assert galah.atlas_counts(taxa_array)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Anser anser"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_group_by_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Anser anser"]
    group_by = ["year", "basis_of_record"]
    output = galah.atlas_counts(taxa_array, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_multiple_taxa_filter_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Anser anser"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array, filters=filter1)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filter_group_by_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Anser anser"]
    filter1 = "year=2020"
    group_by = "basis_of_record"
    output = galah.atlas_counts(taxa_array, filters=filter1, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_taxa_filters_austria_total_group_by():
    galah.galah_config(atlas="Austria")
    output = galah.atlas_counts(filters="year>=2020", group_by="species", total_group_by=True)
    assert output.shape[0] == 1
    assert output["count"][0] > 0


def test_atlas_counts_multiple_taxa_filters_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Anser anser"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa_array, filters=filters)["totalRecords"][0] > 0


def test_atlas_counts_multiple_taxa_filters_group_by_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Anser anser"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Anser anser"]
    filters = ["year>2010", "basis_of_record=HumanObservation"]
    group_by = ["country", "year"]
    output = galah.atlas_counts(taxa_array, filters=filters, group_by=group_by)
    assert output["count"][0] > 0
    assert output.shape[1] == len(group_by) + 1


def test_atlas_counts_invalid_multiple_taxa_separate_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Dasyurus hallucatus", "Sehirus luctuosus", "Sehirus morio"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2


def test_atlas_counts_multiple_taxa_separate_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Sehirus morio"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output["count"] >= 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_separate_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Sehirus morio"]
    f = ["basis_of_record=HumanObservation", "year>2000"]
    group_by = ["month", "species"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()


def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Sehirus morio"]
    f = ["basis_of_record=HumanObservation"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output["count"] > 0).all()


def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_austria():
    galah.galah_config(atlas="Austria")
    taxa_array = ["Sehirus luctuosus", "Marmota marmota", "Sehirus morio"]
    f = ["country = Austria", "year=2022"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert output["count"][0] >= 0  # checks that all species counts are greater than or equal zero


######################################
# atlas_species
######################################
def test_atlas_species_Austria_species_austria():
    galah.galah_config(atlas="Austria",email=email_at)
    taxa = "Sehirus"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_Austria_family_austria():
    galah.galah_config(atlas="Austria",email=email_at)
    taxa = "Cydnidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0


def test_atlas_species_Austria_filter_notaxa():
    galah.galah_config(atlas="Austria",email=email_at)
    filtered_species_table = galah.atlas_species(filters=["year=2022", "basis_of_record=HumanObservation"])
    assert filtered_species_table.shape[0] > 0


######################################
# atlas_occurrences
######################################
def test_atlas_occurrences_taxa_austria():
    galah.galah_config(atlas="Austria", email=email_at, reason=10)
    occurrences = galah.atlas_occurrences(taxa="Sehirus luctuosus")
    assert occurrences.shape[0] > 1


def test_atlas_occurrences_taxa_fields_austria():
    galah.galah_config(atlas="Austria", email=email_at, reason=10)
    occurrences = galah.atlas_occurrences(taxa="Sehirus luctuosus", fields=["latitude", "longitude"])
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_austria():
    galah.galah_config(atlas="Austria", email=email_at, reason=10)
    occurrences1 = galah.atlas_occurrences(taxa="Sehirus luctuosus")
    occurrences2 = galah.atlas_occurrences(taxa="Sehirus luctuosus", filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filter_fields_austria():
    galah.galah_config(atlas="Austria", email=email_at, reason=10)
    occurrences = galah.atlas_occurrences(
        taxa="Sehirus luctuosus", filters="year=2020", fields=["latitude", "longitude"]
    )
    assert occurrences.shape[1] == 2


def test_atlas_occurrences_taxa_filters_austria():
    galah.galah_config(atlas="Austria", email=email_at, reason=10)
    filters = ["year>2018", "basis_of_record=HumanObservation"]
    occurrences1 = galah.atlas_occurrences(taxa="Sehirus luctuosus")
    occurrences2 = galah.atlas_occurrences(taxa="Sehirus luctuosus", filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]


def test_atlas_occurrences_taxa_filters_fields_austria():
    galah.galah_config(atlas="Austria", email=email_at, reason=10)
    occurrences = galah.atlas_occurrences(
        taxa="Sehirus luctuosus",
        filters=["year>2018", "basis_of_record=HumanObservation"],
        fields=["latitude", "longitude"],
    )
    assert occurrences.shape[1] == 2


# """
