'''
run pytest integration_tests_galah.py
'''
import pytest,os
import galah

'''
# Austria 

>>> galah.galah_config(atlas="Austria")
>>> galah.atlas_media(taxa="Sehirus luctuosus")
galah.atlas_counts(taxa="Sehirus luctuosus",filters="year=2020")
galah.atlas_counts(taxa="Sehirus luctuosus",filters="year>2010)
galah.atlas_counts(taxa="Sehirus luctuosus",filters="year>2010",group_by="year",expand=False)
galah.atlas_species(taxa="Sehirus")

# Brazil
taxa = "Ramphastos toco"
taxa = "Hydrochoens hydrochaeris"
email = ala4r@ala.org.au

# Canada
taxa = "Alces alces"

# Estonia 
taxa = "Canis lupus"

# France
taxa = "Triturus marmoratus"

# Guatemala
taxa = "Herpailurus yagouaroundi"

# Portugal
taxa = "Gallus gallus"

# Spain
taxa = "Vipera latastei"

# Sweden
taxa = "Alces alces"

# UK
taxa - "Luscinia megarhynchos"
'''

# -------------------------------------------------------------------------------------------------
# Australia
# -------------------------------------------------------------------------------------------------
#'''
def test_show_all_assertions_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(assertions=True)
    print(output)
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

def test_show_all_reasons_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(reasons=True)
    assert output.shape[1] > 1

def test_show_all_ranks_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1

# integration test for search_taxa() - have to test get_api_url
def test_search_taxa_australia():
    galah.galah_config(atlas="Australia")
    output = galah.search_taxa("Vulpes vulpes")
    assert output['taxonConceptID'][0] != None

# test atlas_counts() can call search_taxa() function with single taxa
def test_atlas_counts_australia():
    galah.galah_config(atlas="Australia")
    taxa="Vulpes vulpes"
    assert galah.atlas_counts(taxa)['totalRecords'][0] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_australia():
    galah.galah_config(atlas="Australia")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts['totalRecords'][0] > filtered_counts['totalRecords'][0]

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_expand_australia():
    galah.galah_config(atlas="Australia")
    f = "year=2022"
    groups = ["month","basisOfRecord"]
    filtered_counts = galah.atlas_counts(filters=f,group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_australia():
    galah.galah_config(atlas="Australia")
    f = "year=2022"
    groups = ["month","basisOfRecord"]
    filtered_counts = galah.atlas_counts(filters="year=2022",group_by=groups,expand=False)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with single taxa
def test_atlas_counts_taxa_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas counts for a taxa and empty filter
def test_atlas_counts_taxa_filter_empty_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filter1 = "year="
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_astlas_counts_taxa_same_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa, filters=f)['totalRecords'][0] > 0

# COME BACK TO THIS ONE WHEN MORE BANDWIDTH
# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_atlas_counts_taxa_same_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022", "year!=2020"]
    assert galah.atlas_counts(taxa, filters=f)['totalRecords'][0] > 0

# test data quality filter
def test_atlas_counts_taxa_filter_data_quality_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    no_quality = galah.atlas_counts(taxa,filters=filter1)
    quality = galah.atlas_counts(taxa,filters=filter1,use_data_profile=True)
    assert no_quality['totalRecords'][0] >= quality['totalRecords'][0]

# test atlas counts with multiple taxa and filters, along with separate=True
def test_atlas_counts_multiple_taxa_filters_separate_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Notamacropus agilis"]
    f = ["dataResourceName = iNaturalist Australia","year=2022"]
    output = galah.atlas_counts(taxa=taxa_array,separate=True,filters=f)
    assert output.shape[0] > 0

# test if you can group counts by a single group_by
def test_atlas_counts_taxa_group_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    group_by = "year"
    output = galah.atlas_counts(taxa,group_by=group_by,expand=False)
    assert output.shape[0] > 0
    assert output.shape[1] == 2

# group counts by multiple groups (expand=False in this one)
def test_atlas_counts_taxa_groups_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    group_by = ["year","basisOfRecord"]
    output = galah.atlas_counts(taxa,group_by=group_by,expand=False)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# group counts by multiple groups
def test_atlas_counts_taxa_groups_expand_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    group_by = ["year","basisOfRecord"]
    output = galah.atlas_counts(taxa,group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa
def test_atlas_counts_taxa_filters_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filters=["year=2020","basisOfRecord=HUMAN_OBSERVATION"]
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert galah.atlas_counts(taxa,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa and group by one group
def test_atlas_counts_taxa_filters_group_by_no_expand_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filters=["year=2020","basisOfRecord=HUMAN_OBSERVATION"]
    group_by="basisOfRecord"
    output = galah.atlas_counts(taxa,filters=filters,group_by=group_by,expand=False)
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    assert galah.atlas_counts(taxa_array)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    group_by="year"
    output = galah.atlas_counts(taxa_array,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_group_by_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    group_by=["year",'basisOfRecord']
    output = galah.atlas_counts(taxa_array,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array,filters=filter1)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_group_by_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filter1 = "year=2020"
    group_by="basisOfRecord"
    output = galah.atlas_counts(taxa_array,filters=filter1,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    assert galah.atlas_counts(taxa_array,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filters = ["year>2010", "basisOfRecord=HUMAN_OBSERVATION"]
    group_by = ["county","year"]
    # county** , associatedOrganisms , day , decade
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa where one taxon is not present in ALA
def test_atlas_counts_invalid_multiple_taxa_separate_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Dasyurus hallucatus", "Ailuropoda melanoleuca", "Centrostephanus rodgersii"]
    output = galah.atlas_counts(taxa_array, separate=True)
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa
def test_atlas_counts_multiple_taxa_separate_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Dasyurus hallucatus", "Rhincodon typus", "Ceyx azureus", "Ornithorhynchus anatinus"]
    output = galah.atlas_counts(taxa_array, separate=True)
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal to zero

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_separate_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["state = Northern Territory", "month=11"]
    output = galah.atlas_counts(taxa_array, filters=f, separate=True)
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_separate():
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["dataResourceName = iNaturalist Australia", "year=2019"]
    group_by = ["month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, separate=True, expand=False)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate():
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["dataResourceName = iNaturalist Australia"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, separate=True, expand=False)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand():
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["dataResourceName = iNaturalist Australia", "year=2022"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, separate=True, expand=True)
    assert output.shape[1] == len(group_by) + 1
    assert output['count'][0] >= 0 # checks that all species counts are greater than or equal zero

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Australia_species():
    galah.galah_config(atlas="Australia")
    taxa = "Heleioporus"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Australia_family():
    galah.galah_config(atlas="Australia")
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# test galah_group_by with one filter (galah_filter()) and one group
def test_galah_group_by_filter():
    # third test to test single filter
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29%20AND%20"
    group_by1 = ["year"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL, group_by=group_by1, filters=filters1,expand=False)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and one group
def test_galah_group_by_filters():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29%20AND%20"
    group_by1 = ["year"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL, group_by=group_by1, filters=filters2,expand=False)
    assert output.shape[1] > 1

# test galah_group_by with one filter (galah_filter()) and two group_by
def test_galah_group_by_multiple_groups():
    # third test to test single filter
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29%20AND%20"
    group_by2 = ["year","basisOfRecord"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL,group_by=group_by2,filters=filters1,expand=False)
    assert output.shape[1] > 1

# test galah_group_by with one filter (galah_filter()) and two group_by, with expand = True
def test_galah_group_by_multiple_groups_multiple_filters():
    # test to test single filter and expand
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29%20AND%20"
    group_by2 = ["year","basisOfRecord"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL, group_by=group_by2, filters=filters1)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and two group_by
def test_galah_group_by_multiple_groups_multiple_filters_expand_false():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29%20AND%20"
    group_by2 = ["year","basisOfRecord"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL, group_by=group_by2, filters=filters2,expand=False)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and two group_by, with expand = True
def test_galah_group_by_multiple_groups_multiple_filters_expand_true():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29%20AND%20"
    group_by2 = ["year","basisOfRecord"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL, group_by=group_by2, filters=filters2)
    assert output.shape[1] > 1

# search_all() - assertions using "AMBIGUOUS_COLLECTION"
def test_search_all_assertions():
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="collection")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - assertions using "collection" and column name "description"
def test_search_all_assertions_column_name():
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="status",column_name="name")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Australia"
def test_search_all_atlases():
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Australia")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Australia" and column name "institution"
def test_search_all_atlases_column_name():
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Australia",column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - apis using "Australia"
def test_search_all_apis():
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Australia")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - apis using "collection" and column name "systems"
def test_search_all_apis_column_name():
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection",column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - collection using "Agricultural"
def test_search_all_collection():
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - collection using "Agricultural" and column name "uid"
def test_search_all_collection_column_name():
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - datasets using "Torres"
def test_search_all_datasets():
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Torres")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - datasets using "4047" and column_name "uid"
def test_search_all_datasets_column_name():
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - fields using "accepted"
def test_search_all_fields():
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - fields using "field" and column_nane "info"
def test_search_all_fields_column_name():
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="layer",column_name="type")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - licences using "accepted"
def test_search_all_licences():
    total_show_all = galah.show_all(licences=True)
    total_search_all = galah.search_all(licences="Creative")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - licences using "CC BY" and column_name "acronym"
def test_search_all_licences_column_name():
    total_show_all = galah.show_all(licences=True)
    total_search_all = galah.search_all(licences="CC BY",column_name="acronym")
    assert total_search_all.shape[0] < total_show_all.shape[0]
        
# search_all() - lists using "Quadrat"
def test_search_all_lists():
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="Quadrat")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - lists using "SPATIAL" and column_name "listType"
def test_search_all_lists_column_name():
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="SPATIAL",column_name="listType")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - profiles using "ALA"
def test_search_all_profiles():
    total_show_all = galah.show_all(profiles=True)
    total_search_all = galah.search_all(profiles="ALA")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - profiles using "ALA" and column_name "shortName"
def test_search_all_profiles_column_name():
    total_show_all = galah.show_all(profiles=True)
    total_search_all = galah.search_all(profiles="ALA",column_name="shortName")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - providers using "Ecological"
def test_search_all_providers():
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - providers using "1518" and column_name "uid"
def test_search_all_providers_column_name():
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "kingdom"
def test_search_all_ranks():
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "0" and column_name "id"
def test_search_all_ranks_column_name():
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0",column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - reasons using "conservation"
def test_search_all_reasons():
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="conservation")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - reasons using "0" and column_name "id"
def test_search_all_reasons_column_name():
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="0",column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]

def test_search_values():
    first_output = galah.show_values(field="basisOfRecord")
    second_output = galah.search_values(field="basisOfRecord",value="OBS")
    assert first_output.shape[0] > second_output.shape[0]

# first test for atlas_occurrences() - check if search_taxa() is working
def test_atlas_occurrences_taxa():
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes")
    assert occurrences.shape[0] > 1

# second test for atlas_occurrences() - check if galah_select() is working
def test_atlas_occurrences_taxa_fields():
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",fields=['decimalLatitude', 'decimalLongitude'])
    # columns
    assert occurrences.shape[1] == 2

# third test for atlas_occurrences() - check if galah_filter() is working with this
def test_atlas_occurrences_taxa_filters():
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]

# fourth test for atlas_occurrences() - check if galah_select() and galah_filter() are working concurrently
def test_atlas_occurrences_taxa_filter_fields():
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2020",fields=['decimalLatitude', 'decimalLongitude'])
    assert occurrences.shape[1] == 2

# testing atlas occurrences with multiple filters
def test_atlas_occurrences_taxa_filters():
    filters=["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes",filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]

# testing atlas occurrences with multiple filters and fields
def test_atlas_occurrences_taxa_filters_fields():
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",filters=["year>2018","basisOfRecord=HUMAN_OBSERVATION"],
                                           fields=['decimalLatitude', 'decimalLongitude'])
    assert occurrences.shape[1] == 2

# test data quality data profile is working
def test_atlas_occurrences_taxa_filters():
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes",use_data_profile=True)
    assert occurrences2.shape[0] < occurrences1.shape[0]
#'''
# add multimedia tests, but not too many...
'''
#test if it can get a taxa and return output
def test_atlas_media_taxa():
    output = galah.atlas_media(taxa="Ornithorhynchus anatinus")
    assert output.shape[0] > 1

# test if the filters component of atlas_media is working
def test_atlas_media_filters():
    raw_output = galah.atlas_media(taxa="Ornithorhynchus anatinus")
    filters = ["year=2020","decimalLongitude>153.0"]
    filtered_output = galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=filters)
    assert raw_output.shape[0] > filtered_output.shape[0]

def test_atlas_media_multimedia():
    multimedia="images"
    raw_output = galah.atlas_media(taxa="Ornithorhynchus anatinus")
    multimedia_output = galah.atlas_media(taxa="Ornithorhynchus anatinus",multimedia=multimedia)
    assert raw_output.shape[0] > multimedia_output.shape[0]
    #filters=["year=2020","decimalLongitude>153.0"],collect=True,path="test"

def test_atlas_media_filters_multimedia():
    multimedia="images"
    raw_output = galah.atlas_media(taxa="Ornithorhynchus anatinus")
    filters = ["year=2020", "decimalLongitude>153.0"]
    multimedia_output = galah.atlas_media(taxa="Ornithorhynchus anatinus",multimedia=multimedia,filters=filters)
    assert raw_output.shape[0] > multimedia_output.shape[0]
    #filters=["year=2020","decimalLongitude>153.0"],collect=True,path="test"

def test_atlas_media_filters_multimedia_collect_path():
    multimedia="images"
    filters = ["year=2020", "decimalLongitude>153.0"]
    path="test"
    multimedia_output = galah.atlas_media(taxa="Ornithorhynchus anatinus",multimedia=multimedia,filters=filters,collect=True,path=path)
    files = os.listdir(path)
    assert len(files) > 0
'''

# -------------------------------------------------------------------------------------------------
# Brazil
# -------------------------------------------------------------------------------------------------
#'''
def test_show_all_assertions_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.show_all(assertions=True)
    print(output)
    assert output.shape[1] > 1

def test_show_all_atlases_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1

def test_show_all_apis_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1

def test_show_all_collection_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.show_all(collection=True)
    assert output.shape[1] > 1

def test_show_all_datasets_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1

def test_show_all_fields_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1

def test_show_all_lists_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.show_all(lists=True)
    assert output.shape[1] > 1

def test_show_all_providers_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1

def test_show_all_ranks_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1

# integration test for search_taxa() - have to test get_api_url
def test_search_taxa_brazil():
    galah.galah_config(atlas="Brazil")
    output = galah.search_taxa("Ramphastos toco")
    assert output['guid'][0] != None

# test atlas_counts() can call search_taxa() function with single taxa
def test_atlas_counts_brazil():
    galah.galah_config(atlas="Brazil")
    taxa="Ramphastos toco"
    assert galah.atlas_counts(taxa)['totalRecords'][0] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_brazil():
    galah.galah_config(atlas="Brazil")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts['totalRecords'][0] > filtered_counts['totalRecords'][0]

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_expand_brazil():
    galah.galah_config(atlas="Brazil")
    f = "year=2022"
    groups = ["month","basis_of_record"]
    filtered_counts = galah.atlas_counts(filters=f,group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_brazil():
    galah.galah_config(atlas="Brazil")
    f = "year=2022"
    groups = ["month","basis_of_record"]
    filtered_counts = galah.atlas_counts(filters="year=2022",group_by=groups,expand=False)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with single taxa
def test_atlas_counts_taxa_filter_brazil():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastos toco"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas counts for a taxa and empty filter
def test_atlas_counts_taxa_filter_empty_brazil():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastos toco"
    filter1 = "year="
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_astlas_counts_taxa_same_filter_brazil():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastos toco"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa, filters=f)['totalRecords'][0] > 0

# test atlas counts with multiple taxa and filters, along with separate=True
def test_atlas_counts_multiple_taxa_filters_separate_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    f = ["basis_of_record = HumanObservation","year=2022"]
    output = galah.atlas_counts(taxa=taxa_array,separate=True,filters=f)
    assert output.shape[0] > 0

# test if you can group counts by a single group_by
def test_atlas_counts_taxa_group_brazil():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastos toco"
    group_by = "year"
    output = galah.atlas_counts(taxa,group_by=group_by,expand=False)
    assert output.shape[0] > 0
    assert output.shape[1] == 2

# group counts by multiple groups (expand=False in this one)
def test_atlas_counts_taxa_groups_brazil():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastos toco"
    group_by = ["year","basis_of_record"]
    output = galah.atlas_counts(taxa,group_by=group_by,expand=False)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# group counts by multiple groups
def test_atlas_counts_taxa_groups_expand_brazil():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastos toco"
    group_by = ["year","basis_of_record"]
    output = galah.atlas_counts(taxa,group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa
def test_atlas_counts_taxa_filters_brazil():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastos toco"
    filters=["year=2020","basis_of_record=HumanObservation"]
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert galah.atlas_counts(taxa,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa and group by one group
def test_atlas_counts_taxa_filters_group_by_no_expand_brazil():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastos toco"
    filters=["year=2020","basis_of_record=HumanObservation"]
    group_by="basis_of_record"
    output = galah.atlas_counts(taxa,filters=filters,group_by=group_by,expand=False)
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    assert galah.atlas_counts(taxa_array)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    group_by="year"
    output = galah.atlas_counts(taxa_array,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_group_by_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    group_by=["year",'basis_of_record']
    output = galah.atlas_counts(taxa_array,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array,filters=filter1)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_group_by_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    filter1 = "year=2020"
    group_by="basis_of_record"
    output = galah.atlas_counts(taxa_array,filters=filter1,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa_array,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    filters = ["year>2010", "basis_of_record=HumanObservation"]
    group_by = ["state","year"] # may have to change this
    # county** , associatedOrganisms , day , decade
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa where one taxon is not present in ALA
def test_atlas_counts_invalid_multiple_taxa_separate_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris","Vulpes vulpes"]
    output = galah.atlas_counts(taxa_array, separate=True)
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa
def test_atlas_counts_multiple_taxa_separate_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    output = galah.atlas_counts(taxa_array, separate=True)
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal to zero

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_separate_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    f = ["basis_of_record = HumanObservation", "year=2019"] # change
    output = galah.atlas_counts(taxa_array, filters=f, separate=True)
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_separate_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    f = ["basis_of_record = HumanObservation", "year=2019"]
    group_by = ["month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, separate=True, expand=False)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    f = ["basis_of_record = HumanObservation"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, separate=True, expand=False)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_brazil():
    galah.galah_config(atlas="Brazil")
    taxa_array = ["Ramphastos toco","Turdus rufiventris","Tapirus terrestris"]
    f = ["basis_of_record = HumanObservation", "year=2022"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, separate=True, expand=True)
    assert output.shape[1] == len(group_by) + 1
    assert output['count'][0] >= 0 # checks that all species counts are greater than or equal zero

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Brazil_species():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastos"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Brazil_family():
    galah.galah_config(atlas="Brazil")
    taxa = "Ramphastidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# search_all() - assertions using "AMBIGUOUS_COLLECTION"
def test_search_all_assertions_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="ambiguousName")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - assertions using "collection" and column name "description"
def test_search_all_assertions_column_name_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="coll",column_name="description")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Brazil"
def test_search_all_atlases_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Brazil")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Australia" and column name "institution"
def test_search_all_atlases_column_name_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Brazil",column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - apis using "Australia"
def test_search_all_apis_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Brazil")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - apis using "collection" and column name "systems"
def test_search_all_apis_column_name_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection",column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - collection using "Agricultural"
def test_search_all_collection_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - collection using "Agricultural" and column name "uid"
def test_search_all_collection_column_name():
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - datasets using "Torres"
def test_search_all_datasets_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Torres")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - datasets using "4047" and column_name "uid"
def test_search_all_datasets_column_name_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - fields using "accepted"
def test_search_all_fields_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - fields using "field" and column_nane "info"
def test_search_all_fields_column_name_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="basis",column_name="description")
    assert total_search_all.shape[0] < total_show_all.shape[0]
        
# search_all() - lists using "Quadrat"
def test_search_all_lists_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="Quadrat")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - lists using "SPATIAL" and column_name "listType"
def test_search_all_lists_column_name_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="SPATIAL",column_name="listType")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - providers using "Ecological"
def test_search_all_providers_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - providers using "1518" and column_name "uid"
def test_search_all_providers_column_name_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "kingdom"
def test_search_all_ranks_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "0" and column_name "id"
def test_search_all_ranks_column_name_brazil():
    galah.galah_config(atlas="Brazil")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0",column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]

def test_search_values_brazil():
    galah.galah_config(atlas="Brazil")
    first_output = galah.show_values(field="basis_of_record")
    second_output = galah.search_values(field="basis_of_record",value="obs")
    assert first_output.shape[0] > second_output.shape[0]

# first test for atlas_occurrences() - check if search_taxa() is working
def test_atlas_occurrences_taxa_brazil():
    galah.galah_config(atlas="Brazil",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Ramphastos Toco")
    assert occurrences.shape[0] > 1

# second test for atlas_occurrences() - check if galah_select() is working
def test_atlas_occurrences_taxa_fields_brazil():
    galah.galah_config(atlas="Brazil",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Ramphastos Toco",fields=['latitude', 'longitude'])
    # columns
    assert occurrences.shape[1] == 2

# third test for atlas_occurrences() - check if galah_filter() is working with this
def test_atlas_occurrences_taxa_filters_brazil():
    galah.galah_config(atlas="Brazil",email="ala4r@ala.org.au")
    occurrences1 = galah.atlas_occurrences(taxa="Ramphastos Toco")
    occurrences2 = galah.atlas_occurrences(taxa="Ramphastos Toco",filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]

# fourth test for atlas_occurrences() - check if galah_select() and galah_filter() are working concurrently
def test_atlas_occurrences_taxa_filter_fields_brazil():
    galah.galah_config(atlas="Brazil",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Ramphastos Toco",filters="year=2020",fields=['latitude', 'longitude'])
    assert occurrences.shape[1] == 2

# testing atlas occurrences with multiple filters
def test_atlas_occurrences_taxa_filters_brazil():
    galah.galah_config(atlas="Brazil",email="ala4r@ala.org.au")
    filters=["year>2018","basis_of_record=HumanObservation"]
    occurrences1 = galah.atlas_occurrences(taxa="Ramphastos Toco")
    occurrences2 = galah.atlas_occurrences(taxa="Ramphastos Toco",filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]

# testing atlas occurrences with multiple filters and fields
def test_atlas_occurrences_taxa_filters_fields_brazil():
    galah.galah_config(atlas="Brazil",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Ramphastos Toco",filters=["year>2018","basis_of_record=HumanObservation"],
                                           fields=['latitude', 'longitude'])
    assert occurrences.shape[1] == 2
#'''
# -------------------------------------------------------------------------------------------------
# Spain
# -------------------------------------------------------------------------------------------------
#'''
def test_show_all_assertions_spain():
    galah.galah_config(atlas="Spain")
    output = galah.show_all(assertions=True)
    print(output)
    assert output.shape[1] > 1

def test_show_all_atlases_spain():
    galah.galah_config(atlas="Spain")
    output = galah.show_all(atlases=True)
    assert output.shape[1] > 1

def test_show_all_apis_spain():
    galah.galah_config(atlas="Spain")
    output = galah.show_all(apis=True)
    assert output.shape[1] > 1

def test_show_all_collection_spain():
    galah.galah_config(atlas="Spain")
    output = galah.show_all(collection=True)
    assert output.shape[1] > 1

def test_show_all_datasets_spain():
    galah.galah_config(atlas="Spain")
    output = galah.show_all(datasets=True)
    assert output.shape[1] > 1

def test_show_all_fields_spain():
    galah.galah_config(atlas="Spain")
    output = galah.show_all(fields=True)
    assert output.shape[1] > 1

def test_show_all_lists_spain():
    galah.galah_config(atlas="Spain")
    output = galah.show_all(lists=True)
    assert output.shape[1] > 1

def test_show_all_providers_spain():
    galah.galah_config(atlas="Spain")
    output = galah.show_all(providers=True)
    assert output.shape[1] > 1

def test_show_all_ranks_spain():
    galah.galah_config(atlas="Spain")
    output = galah.show_all(ranks=True)
    assert output.shape[1] > 1

# integration test for search_taxa() - have to test get_api_url
def test_search_taxa_spain():
    galah.galah_config(atlas="Spain")
    output = galah.search_taxa(taxa = "Abies alba")
    assert output['taxonConceptID'][0] != None

# test atlas_counts() can call search_taxa() function with single taxa
def test_atlas_counts_spain():
    galah.galah_config(atlas="Spain")
    taxa="Abies alba"
    assert galah.atlas_counts(taxa)['totalRecords'][0] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_spain():
    galah.galah_config(atlas="Spain")
    f = "year=2022"
    all_counts = galah.atlas_counts()
    filtered_counts = galah.atlas_counts(filters=f)
    assert all_counts['totalRecords'][0] > filtered_counts['totalRecords'][0]

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_expand_spain():
    galah.galah_config(atlas="Spain")
    f = "year=2022"
    groups = ["month","basis_of_record"]
    filtered_counts = galah.atlas_counts(filters=f,group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# testing filtering works when no taxa are entered
def test_atlas_counts_filters_groupby_spain():
    galah.galah_config(atlas="Spain")
    f = "year=2022"
    groups = ["month","basis_of_record"]
    filtered_counts = galah.atlas_counts(filters="year=2022",group_by=groups,expand=False)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with single taxa
def test_atlas_counts_taxa_filter_spain():
    galah.galah_config(atlas="Spain")
    taxa = "Vipera latastei"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas counts for a taxa and empty filter
def test_atlas_counts_taxa_filter_empty_spain():
    galah.galah_config(atlas="Spain")
    taxa = "Vipera latastei"
    filter1 = "year="
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_astlas_counts_taxa_same_filter_spain():
    galah.galah_config(atlas="Spain")
    taxa = "Vipera latastei"
    f = ["year >=2018", "year <= 2022"]

# test if you can group counts by a single group_by
def test_atlas_counts_taxa_group_spain():
    galah.galah_config(atlas="Spain")
    taxa = "Vipera latastei"
    group_by = "year"
    output = galah.atlas_counts(taxa,group_by=group_by,expand=False)
    assert output.shape[0] > 0
    assert output.shape[1] == 2

# group counts by multiple groups (expand=False in this one)
def test_atlas_counts_taxa_groups_spain():
    galah.galah_config(atlas="Spain")
    taxa = "Vipera latastei"
    group_by = ["year","basis_of_record"]
    output = galah.atlas_counts(taxa,group_by=group_by,expand=False)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# group counts by multiple groups
def test_atlas_counts_taxa_groups_expand_spain():
    galah.galah_config(atlas="Spain")
    taxa = "Vipera latastei"
    group_by = ["year","basis_of_record"]
    output = galah.atlas_counts(taxa,group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa
def test_atlas_counts_taxa_filters_spain():
    galah.galah_config(atlas="Spain")
    taxa = "Vipera latastei"
    filters=["year=2020","basis_of_record=HumanObservation"]
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert galah.atlas_counts(taxa,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa and group by one group
def test_atlas_counts_taxa_filters_group_by_no_expand_spain():
    galah.galah_config(atlas="Spain")
    taxa = "Vipera latastei"
    filters=["year=2020","basis_of_record=HumanObservation"]
    group_by="basis_of_record"
    output = galah.atlas_counts(taxa,filters=filters,group_by=group_by,expand=False)
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    assert galah.atlas_counts(taxa_array)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    group_by="year"
    output = galah.atlas_counts(taxa_array,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_multiple_taxa_group_by_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    group_by=["year",'basis_of_record']
    output = galah.atlas_counts(taxa_array,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array,filters=filter1)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filter_group_by_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    filter1 = "year=2020"
    group_by="basis_of_record"
    output = galah.atlas_counts(taxa_array,filters=filter1,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    assert galah.atlas_counts(taxa_array,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    filters = ["year=2020", "basis_of_record=HumanObservation"]
    group_by = "year"
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by,expand=False)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    filters = ["year>2010", "basis_of_record=HumanObservation"]
    group_by = ["state","year"] # may have to change this
    # county** , associatedOrganisms , day , decade
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by)
    assert output['count'][0] > 0
    assert output.shape[1] == len(group_by) + 1

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa where one taxon is not present in ALA
def test_atlas_counts_invalid_multiple_taxa_separate_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Macropus","Ursus arctos"]
    output = galah.atlas_counts(taxa_array, separate=True)
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa
def test_atlas_counts_multiple_taxa_separate_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    output = galah.atlas_counts(taxa_array, separate=True)
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal to zero

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_separate_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Aquila adalberti"]
    f = ["basis_of_record = HumanObservation", "year=2019"] # change
    output = galah.atlas_counts(taxa_array, filters=f, separate=True)
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_separate_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    f = ["basis_of_record = HumanObservation", "year=2019"]
    group_by = ["month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, separate=True, expand=False)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    f = ["basis_of_record = HumanObservation"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, separate=True, expand=False)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_spain():
    galah.galah_config(atlas="Spain")
    taxa_array = ["Vipera latastei","Gypaetus barbatus","Ursus arctos"]
    f = ["basis_of_record = HumanObservation", "year=2022"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by, separate=True, expand=True)
    assert output.shape[1] == len(group_by) + 1
    assert output['count'][0] >= 0 # checks that all species counts are greater than or equal zero

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Spain_species():
    galah.galah_config(atlas="Spain")
    taxa = "Vipera latastei"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Spain_family():
    galah.galah_config(atlas="Spain")
    taxa = "Viperidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# search_all() - assertions using "AMBIGUOUS_COLLECTION"
def test_search_all_assertions_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="ambiguousName")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - assertions using "collection" and column name "description"
def test_search_all_assertions_column_name_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="coll",column_name="description")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Spain"
def test_search_all_atlases_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Spain")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Australia" and column name "institution"
def test_search_all_atlases_column_name_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Spain",column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - apis using "Australia"
def test_search_all_apis_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Spain")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - apis using "collection" and column name "systems"
def test_search_all_apis_column_name_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection",column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - collection using "Agricultural"
def test_search_all_collection_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - collection using "Agricultural" and column name "uid"
def test_search_all_collection_column_name_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - datasets using "Torres"
def test_search_all_datasets_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Torres")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - datasets using "4047" and column_name "uid"
def test_search_all_datasets_column_name_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - fields using "accepted"
def test_search_all_fields_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - fields using "field" and column_nane "info"
def test_search_all_fields_column_name_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="field",column_name="type")
    assert total_search_all.shape[0] < total_show_all.shape[0]
        
# search_all() - lists using "Quadrat"
def test_search_all_lists_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="Quadrat")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - lists using "SPATIAL" and column_name "listType"
def test_search_all_lists_column_name_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="SPATIAL",column_name="listType")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - providers using "Ecological"
def test_search_all_providers_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - providers using "1518" and column_name "uid"
def test_search_all_providers_column_name_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "kingdom"
def test_search_all_ranks_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "0" and column_name "id"
def test_search_all_ranks_column_name_spain():
    galah.galah_config(atlas="Spain")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0",column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]

def test_search_values_spain():
    galah.galah_config(atlas="Spain")
    first_output = galah.show_values(field="basis_of_record")
    second_output = galah.search_values(field="basis_of_record",value="obs")
    assert first_output.shape[0] > second_output.shape[0]

# first test for atlas_occurrences() - check if search_taxa() is working
def test_atlas_occurrences_taxa_spain():
    galah.galah_config(atlas="Spain",email="amanda.buyan@csiro.au")
    occurrences = galah.atlas_occurrences(taxa="Vipera latastei")
    assert occurrences.shape[0] > 1

# second test for atlas_occurrences() - check if galah_select() is working
def test_atlas_occurrences_taxa_fields_spain():
    galah.galah_config(atlas="Spain",email="amanda.buyan@csiro.au")
    occurrences = galah.atlas_occurrences(taxa="Vipera latastei",fields=['latitude', 'longitude'])
    # columns
    assert occurrences.shape[1] == 2

# third test for atlas_occurrences() - check if galah_filter() is working with this
def test_atlas_occurrences_taxa_filters_spain():
    galah.galah_config(atlas="Spain",email="amanda.buyan@csiro.au")
    occurrences1 = galah.atlas_occurrences(taxa="Vipera latastei")
    occurrences2 = galah.atlas_occurrences(taxa="Vipera latastei",filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]

# fourth test for atlas_occurrences() - check if galah_select() and galah_filter() are working concurrently
def test_atlas_occurrences_taxa_filter_fields_spain():
    galah.galah_config(atlas="Spain",email="amanda.buyan@csiro.au")
    occurrences = galah.atlas_occurrences(taxa="Vipera latastei",filters="year=2020",fields=['latitude', 'longitude'])
    assert occurrences.shape[1] == 2

# testing atlas occurrences with multiple filters
def test_atlas_occurrences_taxa_filters_spain():
    galah.galah_config(atlas="Spain",email="amanda.buyan@csiro.au")
    filters=["year>2018","basis_of_record=HumanObservation"]
    occurrences1 = galah.atlas_occurrences(taxa="Vipera latastei")
    occurrences2 = galah.atlas_occurrences(taxa="Vipera latastei",filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]

# testing atlas occurrences with multiple filters and fields
def test_atlas_occurrences_taxa_filters_fields_spain():
    galah.galah_config(atlas="Spain",email="amanda.buyan@csiro.au")
    occurrences = galah.atlas_occurrences(taxa="Vipera latastei",filters=["year>2018","basis_of_record=HumanObservation"],
                                           fields=['latitude', 'longitude'])
    assert occurrences.shape[1] == 2
#'''