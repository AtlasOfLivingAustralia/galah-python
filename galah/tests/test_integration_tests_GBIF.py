import galah


def test_show_all_assertions_global():
    galah.galah_config(atlas="Global")
    output = galah.show_all(assertions=True)
    assert output.shape[1] > 1

def test_show_all_atlases_global():
    galah.galah_config(atlas="Global")
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1

def test_show_all_apis_global():
    galah.galah_config(atlas="Global")
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1

def test_show_all_datasets_global():
    galah.galah_config(atlas="Global")
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1

def test_show_all_fields_global():
    galah.galah_config(atlas="Global")
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1

def test_show_all_providers_global():
    galah.galah_config(atlas="Global")
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1

def test_show_all_ranks_global():
    galah.galah_config(atlas="Global")
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1

# integration test for search_taxa() - have to test get_api_url
def test_search_taxa_global():
    galah.galah_config(atlas="Global")
    output = galah.search_taxa("Vulpes vulpes")
    assert output['usageKey'][0] != None

# test atlas_counts() can call search_taxa() function with single taxa
def test_atlas_counts_global():
    galah.galah_config(atlas="Global")
    taxa="Vulpes vulpes"
    assert galah.atlas_counts(taxa)['totalRecords'][0] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_global():
    galah.galah_config(atlas="Global")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts['totalRecords'][0] > filtered_counts['totalRecords'][0]

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_expand_global():
    galah.galah_config(atlas="Global")
    f = "year=2022"
    groups = ["month","basisOfRecord"]
    filtered_counts = galah.atlas_counts(filters=f,group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_global():
    galah.galah_config(atlas="Global")
    f = "year=2022"
    groups = ["month","basisOfRecord"]
    filtered_counts = galah.atlas_counts(filters="year=2022",group_by=groups,expand=False)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with single taxa
def test_atlas_counts_taxa_filter_global():
    galah.galah_config(atlas="Global")
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas counts for a taxa and empty filter
def test_atlas_counts_taxa_filter_empty_global():
    galah.galah_config(atlas="Global")
    taxa = "Vulpes vulpes"
    filter1 = "year="
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

'''
# TODO: Figure these out
# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_atlas_counts_taxa_same_filter_global():
    galah.galah_config(atlas="Global")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa, filters=f)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_atlas_counts_taxa_same_filter_global2_global():
    galah.galah_config(atlas="Global")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022", "year!=2020"]
    assert galah.atlas_counts(taxa, filters=f)['totalRecords'][0] > 0
'''

# test altas_counts() with total_group_by
def test_atlas_counts_taxa_filters_global_total_group_by():
    galah.galah_config(atlas="Global")
    output = galah.atlas_counts(taxa="Triturus",filters="year=2020",group_by="scientificName",expand=False,total_group_by=True)
    assert output.shape[0] == 1
    assert output['count'][0] > 0

# test atlas counts with multiple taxa and filters, along with expand=True
def test_atlas_counts_multiple_taxa_filters_separate_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Notamacropus agilis"]
    f = ["dataResourceName = iNaturalist Global","year=2022"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f,group_by="scientificName",expand=False)
    assert output.shape[0] > 0

# test if you can group counts by a single group_by
def test_atlas_counts_taxa_group_global():
    galah.galah_config(atlas="Global")
    taxa = "Vulpes vulpes"
    group_by = "year"
    output = galah.atlas_counts(taxa,group_by=group_by,expand=False)
    assert output.shape[0] > 0
    assert output.shape[1] == 2

# group counts by multiple groups (expand=False in this one)
def test_atlas_counts_taxa_groups_global():
    galah.galah_config(atlas="Global")
    taxa = "Vulpes vulpes"
    group_by = ["year","basisOfRecord"]
    output = galah.atlas_counts(taxa,group_by=group_by,expand=False)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# group counts by multiple groups
def test_atlas_counts_taxa_groups_expand_global():
    galah.galah_config(atlas="Global")
    taxa = "Vulpes vulpes"
    group_by = ["year","basisOfRecord"]
    output = galah.atlas_counts(taxa,group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa
def test_atlas_counts_taxa_filters_global():
    galah.galah_config(atlas="Global")
    taxa = "Vulpes vulpes"
    filters=["year=2020","basisOfRecord=HUMAN_OBSERVATION"]
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert galah.atlas_counts(taxa,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa and group by one group
def test_atlas_counts_taxa_filters_group_by_no_expand_global():
    galah.galah_config(atlas="Global")
    taxa = "Vulpes vulpes"
    filters=["year=2020","basisOfRecord=HUMAN_OBSERVATION"]
    group_by="basisOfRecord"
    output = galah.atlas_counts(taxa,filters=filters,group_by=group_by,expand=False)
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    assert galah.atlas_counts(taxa_array)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    group_by="year"
    output = galah.atlas_counts(taxa_array,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_group_by_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    group_by=["year",'basisOfRecord']
    output = galah.atlas_counts(taxa_array,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array,filters=filter1)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_group_by_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filter1 = "year=2020"
    group_by="basisOfRecord"
    output = galah.atlas_counts(taxa_array,filters=filter1,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    assert galah.atlas_counts(taxa_array,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filters = ["year>2020", "basisOfRecord=HUMAN_OBSERVATION"]
    group_by = ["month","year"]
    # county** , associatedOrganisms , day , decade
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa
def test_atlas_counts_multiple_taxa_separate_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Dasyurus hallucatus", "Rhincodon typus", "Ceyx azureus", "Ornithorhynchus anatinus"]
    output = galah.atlas_counts(taxa_array, group_by="scientificName",expand=False)
    assert output.shape[0] >= len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal to zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_separate_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["basisOfRecord=HUMAN_OBSERVATION", "year>=2010"]
    group_by = ["month","scientificName"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, expand=True)
    assert output.shape[1] >= len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["dataResourceName = iNaturalist Global"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, expand=True)
    assert output.shape[1] >= len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_global():
    galah.galah_config(atlas="Global")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["dataResourceName = iNaturalist Global", "year=2022"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, expand=True)
    assert output.shape[1] == len(group_by) + 1
    assert output['count'][0] >= 0 # checks that all species counts are greater than or equal zero

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_species_global():
    galah.galah_config(atlas="Global",email="ala4r@ala.org.au",usernameGBIF="atlasoflivingaustralia",passwordGBIF="galah-gbif-test-login")
    taxa = "Heleioporus"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe
def test_atlas_species_family_global():
    galah.galah_config(atlas="Global",email="ala4r@ala.org.au",usernameGBIF="atlasoflivingaustralia",passwordGBIF="galah-gbif-test-login")
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

def test_atlas_species_global_filter_notaxa():
    galah.galah_config(atlas="Global",email="ala4r@ala.org.au",usernameGBIF="atlasoflivingaustralia",passwordGBIF="galah-gbif-test-login")
    filtered_species_table = galah.atlas_species(filters=["year=2022","basisOfRecord=HUMAN_OBSERVATION"])
    assert filtered_species_table.shape[0] > 0

# search_all() - assertions using "AMBIGUOUS_COLLECTION"
def test_search_all_assertions_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="collection")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - assertions using "collection" and column name "description"
def test_search_all_assertions_column_name_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="STATUS",column_name="ID")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Global"
def test_search_all_atlases_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Global")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Global" and column name "institution"
def test_search_all_atlases_column_name_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Global",column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - apis using "Global"
def test_search_all_apis_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Global")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - apis using "collection" and column name "systems"
def test_search_all_apis_column_name_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection",column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - datasets using "Torres"
def test_search_all_datasets_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Herbarium")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - datasets using "4047" and column_name "uid"
def test_search_all_datasets_column_name_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Marsup",column_name="title")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - fields using "accepted"
def test_search_all_fields_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - fields using "field" and column_nane "info"
def test_search_all_fields_column_name_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="layer",column_name="Parameter")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - providers using "Ecological"
def test_search_all_providers_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Univers")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - providers using "1518" and column_name "uid"
def test_search_all_providers_column_name_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Insititute",column_name="description")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "kingdom"
def test_search_all_ranks_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "0" and column_name "id"
def test_search_all_ranks_column_name_global():
    galah.galah_config(atlas="Global")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0",column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]

'''
def test_search_values_global():
    galah.galah_config(atlas="Global")
    first_output = galah.show_values(field="basisOfRecord")
    second_output = galah.search_values(field="basisOfRecord",value="OBS")
    assert first_output.shape[0] > second_output.shape[0]
#'''
# first test for atlas_occurrences() - check if search_taxa() is working
def test_atlas_occurrences_taxa_filters_global():
    galah.galah_config(atlas="Global",email="ala4r@ala.org.au",usernameGBIF="atlasoflivingaustralia",passwordGBIF="galah-gbif-test-login")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2022")
    assert occurrences.shape[0] > 1

# testing atlas occurrences with multiple filters
def test_atlas_occurrences_taxa_filters2_global():
    galah.galah_config(atlas="Global",email="ala4r@ala.org.au",usernameGBIF="atlasoflivingaustralia",passwordGBIF="galah-gbif-test-login")
    filters=["year=2022","basisOfRecord=HUMAN_OBSERVATION"]
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",filters=filters)
    assert occurrences.shape[0] > 0

# testing atlas occurrences with multiple filters
def test_atlas_occurrences_taxa_filters3_global():
    galah.galah_config(atlas="Global",email="ala4r@ala.org.au",usernameGBIF="atlasoflivingaustralia",passwordGBIF="galah-gbif-test-login")
    filters=["year>=2022","basisOfRecord=HUMAN_OBSERVATION"]
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",filters=filters)
    assert occurrences.shape[0] > 0

# testing atlas occurrences with multiple filters
def test_atlas_occurrences_taxa_filters4_global():
    galah.galah_config(atlas="Global",email="ala4r@ala.org.au",usernameGBIF="atlasoflivingaustralia",passwordGBIF="galah-gbif-test-login")
    filters=["year>2022","basisOfRecord=HUMAN_OBSERVATION"]
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",filters=filters)
    assert occurrences.shape[0] > 0

# testing atlas occurrences with multiple filters
def test_atlas_occurrences_taxa_filters5_global():
    galah.galah_config(atlas="Global",email="ala4r@ala.org.au",usernameGBIF="atlasoflivingaustralia",passwordGBIF="galah-gbif-test-login")
    filters=["year<2000","basisOfRecord=HUMAN_OBSERVATION"]
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",filters=filters)
    assert occurrences.shape[0] > 0
#'''