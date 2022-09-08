'''
run pytest integration_tests_galah.py
'''
import pytest
import galah

# test atlas_counts() can call search_taxa() function with single species
def test_atlas_counts():
    species="Vulpes vulpes"
    assert galah.atlas_counts(species)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with single species
def test_atlas_counts_2():
    species = "Vulpes vulpes"
    filter1 = "year=2020"
    assert galah.atlas_counts(species,filters=filter1)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using two filter, filter results with single species
def test_atlas_counts_3():
    species = "Vulpes vulpes"
    filters=["year=2020","basisOfRecord=HUMAN_OBSERVATION"]
    # test single species is working (search_taxa(), galah_filter() x 2)
    assert galah.atlas_counts(species,filters=filters)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() function with multiple species
def test_atlas_counts_4():
    species_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    assert galah.atlas_counts(species_array)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple species
def test_atlas_counts_5():
    species_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filter1 = "year=2020"
    assert galah.atlas_counts(species_array,filters=filter1)['totalRecords'][0] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with multiple species
def test_atlas_counts_6():
    species_array = ["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"]
    filters = ["year=2020", "basisOfRecord=HUMAN_OBSERVATION"]
    assert galah.atlas_counts(species_array,filters=filters)['totalRecords'][0] > 0

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