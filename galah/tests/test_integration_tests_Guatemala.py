import galah
'''
def test_show_all_assertions_guatemala():
    galah.galah_config(atlas="Guatemala")
    output = galah.show_all(assertions=True)
    assert output.shape[1] > 1

def test_show_all_atlases_guatemala():
    galah.galah_config(atlas="Guatemala")
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1

def test_show_all_apis_guatemala():
    galah.galah_config(atlas="Guatemala")
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1

def test_show_all_collection_guatemala():
    galah.galah_config(atlas="Guatemala")
    output = galah.show_all(collection=True)
    assert output.shape[1] > 1

def test_show_all_datasets_guatemala():
    galah.galah_config(atlas="Guatemala")
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1

def test_show_all_fields_guatemala():
    galah.galah_config(atlas="Guatemala")
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1

def test_show_all_providers_guatemala():
    galah.galah_config(atlas="Guatemala")
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1

def test_show_all_ranks_guatemala():
    galah.galah_config(atlas="Guatemala")
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1

# integration test for search_taxa() - have to test get_api_url
def test_search_taxa_guatemala():
    galah.galah_config(atlas="Guatemala")
    output = galah.search_taxa("Coragyps atratus")
    assert output['guid'][0] != None

# test atlas_counts() can call search_taxa() function with single taxa
def test_atlas_counts_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa="Coragyps atratus"
    assert galah.atlas_counts(taxa)['totalRecords'][0] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_guatemala():
    galah.galah_config(atlas="Guatemala")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts['totalRecords'][0] > filtered_counts['totalRecords'][0]

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_expand_guatemala():
    galah.galah_config(atlas="Guatemala")
    f = "year=2022"
    groups = ["month","basis_of_record"]
    filtered_counts = galah.atlas_counts(filters=f,group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_guatemala():
    galah.galah_config(atlas="Guatemala")
    f = "year=2022"
    groups = ["month","basis_of_record"]
    filtered_counts = galah.atlas_counts(filters="year=2022",group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with single taxa
def test_atlas_counts_taxa_filter_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Coragyps atratus"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa=taxa,filters=filter1)['totalRecords'][0] > 0

### TODO: try to make this work
# test atlas counts for a taxa and empty filter
def test_atlas_counts_taxa_filter_empty_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Coragyps atratus"
    filter1 = "year="
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_astlas_counts_taxa_same_filter_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Coragyps atratus"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa, filters=f)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_atlas_counts_taxa_same_filter_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Coragyps atratus"
    f = ["year >=2018", "year <= 2022", "year!=2020"]
    assert galah.atlas_counts(taxa, filters=f)['totalRecords'][0] > 0

# test atlas counts with multiple taxa and filters, along with expand=True
def test_atlas_counts_multiple_taxa_filters_separate_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Coragyps atratus", "Pinus Caribaea","Juniperus Standleyi"]
    f = ["basis_of_record = HumanObservation","year>=2000"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f,group_by="species")
    assert output.shape[0] > 0

# test if you can group counts by a single group_by
def test_atlas_counts_taxa_group_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Coragyps atratus"
    group_by = "year"
    output = galah.atlas_counts(taxa,group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == 2

# group counts by multiple groups (expand=False in this one)
def test_atlas_counts_taxa_groups_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Coragyps atratus"
    group_by = ["year","basis_of_record"]
    output = galah.atlas_counts(taxa,group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# group counts by multiple groups
def test_atlas_counts_taxa_groups_expand_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Coragyps atratus"
    group_by = ["year","basis_of_record"]
    output = galah.atlas_counts(taxa,group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa
def test_atlas_counts_taxa_filters_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Coragyps atratus"
    filters=["year=2020","basis_of_record=HumanObservation"]
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert galah.atlas_counts(taxa,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa and group by one group
def test_atlas_counts_taxa_filters_group_by_no_expand_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Coragyps atratus"
    filters=["year=2020","basis_of_record=HumanObservation"]
    group_by="basis_of_record"
    output = galah.atlas_counts(taxa,filters=filters,group_by=group_by)
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    assert galah.atlas_counts(taxa_array)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    group_by="year"
    output = galah.atlas_counts(taxa_array,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_group_by_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    group_by=["year",'basis_of_record']
    output = galah.atlas_counts(taxa_array,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array,filters=filter1)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_group_by_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    filter1 = "year=2020"
    group_by="basis_of_record"
    output = galah.atlas_counts(taxa_array,filters=filter1,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa_array,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    filters = ["year>2010", "basis_of_record=HumanObservation"]
    group_by = ["country","year"]
    # county** , associatedOrganisms , day , decade
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa where one taxon is not present in Guatemala
def test_atlas_counts_invalid_multiple_taxa_separate_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Centrostephanus rodgersii"]
    output = galah.atlas_counts(taxa_array,group_by="species")
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa
def test_atlas_counts_multiple_taxa_separate_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal to zero

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_separate_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    f = ["year=2022", "month=11"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_separate_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    f = ["basis_of_record=HumanObservation", "year>=2019"]
    group_by = ["month","species"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    f = ["basis_of_record=HumanObservation"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa_array = ["Quiscalus mexicanus", "Coragyps atratus", "Turdus grayi", "Melanerpes aurifrons"]
    f = ["basis_of_record=HumanObservation", "year=2022"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert output['count'][0] >= 0 # checks that all species counts are greater than or equal zero

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Guatemala_species_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Quiscalus"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Guatemala_family_guatemala():
    galah.galah_config(atlas="Guatemala")
    taxa = "Icteridae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# search_all() - assertions using "AMBIGUOUS_COLLECTION"
def test_search_all_assertions_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="collection")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - assertions using "collection" and column name "description"
def test_search_all_assertions_column_name_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="status",column_name="name")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Guatemala"
def test_search_all_atlases_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Guatemala")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Guatemala" and column name "institution"
def test_search_all_atlases_column_name_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Guatemala",column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - apis using "Guatemala"
def test_search_all_apis_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Guatemala")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - apis using "collection" and column name "systems"
def test_search_all_apis_column_name_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection",column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - collection using "Agricultural"
def test_search_all_collection_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - collection using "Agricultural" and column name "uid"
def test_search_all_collection_column_name_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - datasets using "Torres"
def test_search_all_datasets_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Torres")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - datasets using "4047" and column_name "uid"
def test_search_all_datasets_column_name_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - fields using "accepted"
def test_search_all_fields_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - fields using "field" and column_nane "info"
def test_search_all_fields_column_name_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="layer",column_name="type")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
def test_search_all_providers_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - providers using "1518" and column_name "uid"
def test_search_all_providers_column_name_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "kingdom"
def test_search_all_ranks_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "0" and column_name "id"
def test_search_all_ranks_column_name_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0",column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - reasons using "conservation"
def test_search_all_reasons_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="conservation")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - reasons using "0" and column_name "id"
def test_search_all_reasons_column_name_guatemala():
    galah.galah_config(atlas="Guatemala")
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="0",column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]

def test_search_values_guatemala():
    galah.galah_config(atlas="Guatemala")
    first_output = galah.show_values(field="basis_of_record")
    second_output = galah.search_values(field="basis_of_record",value="OBS")
    assert first_output.shape[0] > second_output.shape[0]

# first test for atlas_occurrences_guatemala() - check if search_taxa() is working
def test_atlas_occurrences_taxa_guatemala():
    galah.galah_config(atlas="Guatemala",email="test@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Coragyps atratus")
    assert occurrences.shape[0] > 1

# second test for atlas_occurrences_guatemala() - check if galah_select() is working
def test_atlas_occurrences_taxa_fields_guatemala():
    galah.galah_config(atlas="Guatemala",email="test@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Coragyps atratus",fields=['decimalLatitude', 'decimalLongitude'])
    # columns
    assert occurrences.shape[1] == 2

# third test for atlas_occurrences() - check if galah_filter() is working with this
def test_atlas_occurrences_taxa_filters_guatemala():
    galah.galah_config(atlas="Guatemala",email="test@ala.org.au")
    occurrences1 = galah.atlas_occurrences(taxa="Coragyps atratus")
    occurrences2 = galah.atlas_occurrences(taxa="Coragyps atratus",filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]

# fourth test for atlas_occurrences() - check if galah_select() and galah_filter() are working concurrently
def test_atlas_occurrences_taxa_filter_fields_guatemala():
    galah.galah_config(atlas="Guatemala",email="test@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Coragyps atratus",filters="year=2020",fields=['decimalLatitude', 'decimalLongitude'])
    assert occurrences.shape[1] == 2

# testing atlas occurrences with multiple filters
def test_atlas_occurrences_taxa_filters_guatemala():
    galah.galah_config(atlas="Guatemala",email="test@ala.org.au")
    filters=["year>2018","basis_of_record=HumanObservation"]
    occurrences1 = galah.atlas_occurrences(taxa="Coragyps atratus")
    occurrences2 = galah.atlas_occurrences(taxa="Coragyps atratus",filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]

# testing atlas occurrences with multiple filters and fields
def test_atlas_occurrences_taxa_filters_fields_guatemala():
    galah.galah_config(atlas="Guatemala",email="test@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Coragyps atratus",filters=["year>2018","basis_of_record=HumanObservation"],
                                           fields=['decimalLatitude', 'decimalLongitude'])
    assert occurrences.shape[1] == 2
#'''