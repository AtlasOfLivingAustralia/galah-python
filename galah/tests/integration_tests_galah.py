'''
run pytest integration_tests_galah.py
'''
import pytest
import galah

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

# test galah_group_by with one filter (galah_filter()) and one group
def test_galah_group_by_1():
    # third test to test single filter
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups1 = ["year"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL, groups=groups1, filters=filters1)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and one group
def test_galah_group_by_2():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups1 = ["year"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL, groups=groups1, filters=filters2)
    assert output.shape[1] > 1

# test galah_group_by with one filter (galah_filter()) and two groups
def test_galah_group_by_3():
    # third test to test single filter
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups2 = ["year","basisOfRecord"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL,groups=groups2,filters=filters1)
    assert output.shape[1] > 1

# test galah_group_by with one filter (galah_filter()) and two groups, with expand = True
def test_galah_group_by_4():
    # test to test single filter and expand
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups2 = ["year","basisOfRecord"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL, groups=groups2, filters=filters1,expand=True)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and two groups
def test_galah_group_by_5():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups2 = ["year","basisOfRecord"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL, groups=groups2, filters=filters2)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and two groups, with expand = True
def test_galah_group_by_6():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups2 = ["year","basisOfRecord"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL, groups=groups2, filters=filters2,expand=True)
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
