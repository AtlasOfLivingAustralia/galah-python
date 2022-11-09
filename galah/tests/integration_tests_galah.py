'''
run pytest integration_tests_galah.py
'''
import pytest,os
import galah

#'''
# test atlas_counts() can call search_taxa() function with single taxa
def test_atlas_counts():
    taxa="Vulpes vulpes"
    assert galah.atlas_counts(taxa)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with single taxa
def test_atlas_counts_2():
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa,filters=filter1)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using two filter, filter results with single taxa
def test_atlas_counts_3():
    taxa = "Vulpes vulpes"
    filters=["year=2020","basisOfRecord=HUMAN_OBSERVATION"]
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert galah.atlas_counts(taxa,filters=filters)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() function with multiple taxa
def test_atlas_counts_4():
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    assert galah.atlas_counts(taxa_array)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_5():
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa_array,filters=filter1)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple taxa
def test_atlas_counts_6():
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    assert galah.atlas_counts(taxa_array,filters=filters)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using groups to group counts
def test_atlas_counts_7():
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    groups = ["year", "basisOfRecord"]
    assert galah.atlas_counts(taxa_array,group_by=groups).shape[0] > 0

# test altas_counts() can call search_taxa() and using groups to group counts
def test_atlas_counts_7():
    taxa_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    groups = ["year", "basisOfRecord"]
    assert galah.atlas_counts(taxa_array,group_by=groups,expand=False).shape[0] > 0

# test galah_group_by with one filter (galah_filter()) and one group
def test_galah_group_by_1():
    # third test to test single filter
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups1 = ["year"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL, group_by=groups1, filters=filters1,expand=False)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and one group
def test_galah_group_by_2():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups1 = ["year"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL, group_by=groups1, filters=filters2,expand=False)
    assert output.shape[1] > 1

# test galah_group_by with one filter (galah_filter()) and two groups
def test_galah_group_by_3():
    # third test to test single filter
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups2 = ["year","basisOfRecord"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL,group_by=groups2,filters=filters1,expand=False)
    assert output.shape[1] > 1

# test galah_group_by with one filter (galah_filter()) and two groups, with expand = True
def test_galah_group_by_4():
    # test to test single filter and expand
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups2 = ["year","basisOfRecord"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL, group_by=groups2, filters=filters1)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and two groups
def test_galah_group_by_5():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups2 = ["year","basisOfRecord"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL, group_by=groups2, filters=filters2,expand=False)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and two groups, with expand = True
def test_galah_group_by_6():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups2 = ["year","basisOfRecord"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL, group_by=groups2, filters=filters2)
    assert output.shape[1] > 1

# first test for atlas_occurrences() - check if search_taxa() is working
def test_atlas_occurrences_1():
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes")
    #rows
    assert occurrences.shape[0] > 1

# second test for atlas_occurrences() - check if galah_select() is working
def test_atlas_occurrences_2():
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",fields=['decimalLatitude', 'decimalLongitude'])
    # columns
    assert occurrences.shape[1] == 2

# third test for atlas_occurrences() - check if galah_filter() is working with this
def test_atlas_occurrences_3():
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]

# fourth test for atlas_occurrences() - check if galah_select() and galah_filter() are working concurrently
def test_atlas_occurrences_4():
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2020",fields=['decimalLatitude', 'decimalLongitude'])
    assert occurrences2.shape[0] < occurrences1.shape[0]

# search_all() - assertions using "AMBIGUOUS_COLLECTION"
def test_search_all_assertions():
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="AMBIGUOUS_COLLECTION")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - assertions using "collection" and column name "description"
def test_search_all_assertions_column_name():
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="collection",column_name="description")
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
    
# search_all() - apis using "collections" and column name "systems"
def test_search_all_apis_column_name():
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collections",column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - collections using "Agricultural"
def test_search_all_collections():
    total_show_all = galah.show_all(collections=True)
    total_search_all = galah.search_all(collections="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - collections using "Agricultural" and column name "uid"
def test_search_all_collections_column_name():
    total_show_all = galah.show_all(collections=True)
    total_search_all = galah.search_all(collections="85",column_name="uid")
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
    total_search_all = galah.search_all(fields="field",column_name="info")
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
#'''
def test_atlas_species():
    taxa = "Heleioporus"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0
