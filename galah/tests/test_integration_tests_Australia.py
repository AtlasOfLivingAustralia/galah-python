import galah
import os
import shapely
import geopandas

#'''
def test_show_all_assertions_australia():
    galah.galah_config(atlas="Australia")
    output = galah.show_all(assertions=True)
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

# integration test for search_taxa() - have to test get_api_url
def test_search_taxa_australia_identifiers():
    galah.galah_config(atlas="Australia")
    output = galah.search_taxa(identifiers="https://id.biodiversity.org.au/node/apni/2914510")
    assert output['taxonConceptID'][0] != None

# integration test for search_taxa() - have to test get_api_url
def test_search_taxa_australia_specific_epithet():
    galah.galah_config(atlas="Australia")
    output = galah.search_taxa(specific_epithet=["class=aves","family=pardalotidae",
                                                "genus=pardalotus","specificEpithet=punctatus"])
    assert output.shape[0] > 0

# integration test for search_taxa() - have to test get_api_url
def test_search_taxa_australia_scientific_name():
    galah.galah_config(atlas="Australia")
    output = galah.search_taxa(scientific_name={"family": ["pardalotidae","maluridae"],
                                                "scientificName": ["pardolatus striatus","malurus cyaneus"]})
    assert output.shape[0] > 0

# test atlas_counts() can call search_taxa() function with single taxa
def test_atlas_counts_australia():
    galah.galah_config(atlas="Australia")
    taxa="Vulpes vulpes"
    assert galah.atlas_counts(taxa=taxa)['totalRecords'][0] > 0

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
    filtered_counts = galah.atlas_counts(filters="year=2022",group_by=groups)
    assert filtered_counts.shape[0] > 0
    assert filtered_counts.shape[1] > 0

# test altas_counts() can call search_taxa() and using one filter, filter results with single taxa
def test_atlas_counts_taxa_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    assert galah.atlas_counts(taxa=taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas counts for a taxa and empty filter
def test_atlas_counts_taxa_filter_empty_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    filter1 = "year="
    assert galah.atlas_counts(taxa=taxa,filters=filter1)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_atlas_counts_taxa_same_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022"]
    assert galah.atlas_counts(taxa=taxa, filters=f)['totalRecords'][0] > 0

# test atlas_counts() can call search_taxa() and using two filters with the same field, return results for a single taxa
def test_atlas_counts_taxa_same_filter_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Anigozanthos manglesii"
    f = ["year >=2018", "year <= 2022", "year!=2020"]
    assert galah.atlas_counts(taxa=taxa, filters=f)['totalRecords'][0] > 0

# test data quality filter
def test_atlas_counts_taxa_filter_data_quality_australia():
    galah.galah_config(atlas="Australia",data_profile="ALA")
    taxa = "Vulpes vulpes"
    filter1 = "year=2020"
    no_quality = galah.atlas_counts(taxa,filters=filter1)
    quality = galah.atlas_counts(taxa,filters=filter1,use_data_profile=True)
    assert no_quality['totalRecords'][0] >= quality['totalRecords'][0]

# test atlas counts with multiple taxa and filters
def test_atlas_counts_multiple_taxa_filters_separate_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Notamacropus agilis"]
    f = ["dataResourceName = iNaturalist Australia","year=2022"]
    output = galah.atlas_counts(taxa=taxa_array, filters=f,group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal zero

# test if you can group counts by a single group_by
def test_atlas_counts_taxa_group_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    group_by = "year"
    output = galah.atlas_counts(taxa,group_by=group_by)
    assert output.shape[0] > 0
    assert output.shape[1] == 2

# group counts by multiple groups
def test_atlas_counts_taxa_groups_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes vulpes"
    group_by = ["year","basisOfRecord"]
    output = galah.atlas_counts(taxa,group_by=group_by)
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
    output = galah.atlas_counts(taxa,filters=filters,group_by=group_by)
    # test single taxa is working (search_taxa(), galah_filter() x 2)
    assert output['count'][0] > 0
    assert output.shape[1] == 2

# test altas_counts() with total_group_by
def test_atlas_counts_taxa_filters_australia_total_group_by():
    galah.galah_config(atlas="Australia")
    output = galah.atlas_counts(taxa="reptilia",filters="year=2020",group_by="species",total_group_by=True)
    assert output.shape[0] == 1
    assert output['count'][0] > 0

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
    output = galah.atlas_counts(taxa_array,group_by=group_by)
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
    output = galah.atlas_counts(taxa_array,filters=filter1,group_by=group_by)
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
    output = galah.atlas_counts(taxa_array,filters=filters,group_by=group_by)
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
    output = galah.atlas_counts(taxa_array,group_by="species")
    assert output.shape[0] == len(taxa_array) - 1
    assert output.shape[1] == 2

# test atlas_counts() can call search_taxa() and separate the counts for multiple taxa
def test_atlas_counts_multiple_taxa_separate_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Dasyurus hallucatus", "Rhincodon typus", "Ceyx azureus", "Ornithorhynchus anatinus"]
    output = galah.atlas_counts(taxa_array, group_by="species")
    assert output.shape[0] == len(taxa_array)
    assert output.shape[1] == 2
    assert (output['count'] >= 0).all() # checks that all species counts are greater than or equal to zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_separate_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["dataResourceName = iNaturalist Australia", "year=2019"]
    group_by = ["month","species"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filter_group_by_multiple_separate_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["dataResourceName = iNaturalist Australia"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert (output['count'] > 0).all() # checks that all species counts are greater than zero

# test altas_counts() can call search_taxa() and using one filter, filter and group results with multiple taxa separated
def test_atlas_counts_multiple_taxa_filters_group_by_multiple_separate_expand_australia():
    galah.galah_config(atlas="Australia")
    taxa_array = ["Swainsona formosa", "Crocodylus johnstoni", "Platalea (Platalea) regia", "Xeromys myoides"]
    f = ["dataResourceName = iNaturalist Australia", "year=2022"]
    group_by = ["year", "month"]
    output = galah.atlas_counts(taxa_array, filters=f, group_by=group_by)
    assert output.shape[1] == len(group_by) + 1
    assert output['count'][0] >= 0 # checks that all species counts are greater than or equal zero

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Australia_species_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Heleioporus"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# check if you can get subspecies
def test_atlas_species_Australia_species_rank_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Vulpes"
    species_table = galah.atlas_species(taxa=taxa,rank="subspecies")
    assert species_table.shape[0] > 0

# checking if atlas species can successfully call search_taxa() and get a non-empty dataframe\
def test_atlas_species_Australia_family_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa)
    assert species_table.shape[0] > 0

# check to see if you can get something when specifying the rank of genus
def test_atlas_species_Australia_family_rank_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa,rank="genus")
    assert species_table.shape[0] > 0

# check to see if you can get something when specifying the rank of genus
def test_atlas_species_Australia_family_australia():
    galah.galah_config(atlas="Australia")
    taxa = "Limnodynastidae"
    species_table = galah.atlas_species(taxa=taxa,rank="subspecies")
    assert species_table.shape[0] > 0

def test_atlas_species_Australia_filter():
    galah.galah_config(atlas="Australia")
    full_species_table = galah.atlas_species(taxa="Rodentia")
    filtered_species_table = galah.atlas_species(taxa="Rodentia",filters="stateProvince=Victoria")
    assert full_species_table.shape[0] > filtered_species_table.shape[0]

def test_atlas_species_Australia_filter_notaxa():
    galah.galah_config(atlas="Australia")
    filtered_species_table = galah.atlas_species(filters=["year=2022","stateProvince=Victoria"])
    assert filtered_species_table.shape[0] > 0

def test_atlas_species_Australia_polygon():
    galah.galah_config(atlas="Australia")
    full_species_table = galah.atlas_species(polygon=shapely.box(143,-29,148,-28))
    assert full_species_table.shape[0] > 0

def test_atlas_species_Australia_bbox():
    galah.galah_config(atlas="Australia")
    full_species_table = galah.atlas_species(bbox=shapely.box(143,-29,148,-28))
    assert full_species_table.shape[0] > 0

def test_atlas_species_Australia_filter_polygon():
    galah.galah_config(atlas="Australia")
    full_species_table = galah.atlas_species(polygon=shapely.box(143,-29,148,-28))
    filtered_species_table = galah.atlas_species(polygon=shapely.box(143,-29,148,-28),filters="stateProvince=Victoria")
    assert full_species_table.shape[0] > filtered_species_table.shape[0]

def test_atlas_species_Australia_filter_polygon():
    galah.galah_config(atlas="Australia")
    full_species_table = galah.atlas_species(bbox=shapely.box(143,-29,148,-28))
    filtered_species_table = galah.atlas_species(bbox=shapely.box(143,-29,148,-28),filters="stateProvince=Victoria")
    assert full_species_table.shape[0] > filtered_species_table.shape[0]

def test_atlas_species_Australia_filter_notaxa():
    galah.galah_config(atlas="Australia")
    filtered_species_table = galah.atlas_species(filters=["year=2022","stateProvince=Victoria"])
    assert filtered_species_table.shape[0] > 0

# test galah_group_by with one filter (galah_filter()) and one group
def test_galah_group_by_filter_australia():
    # third test to test single filter
    galah.galah_config(atlas="Australia")
    payload = {"fq": ["lsid:https://biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296"]}
    group_by1 = ["year"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL="https://biocache-ws.ala.org.au/ws/occurrences/search?disableAllQualityfilters=true&",method="GET",group_by=group_by1, filters=filters1,payload=payload)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and one group
def test_galah_group_by_filters_australia():
    galah.galah_config(atlas="Australia")
    payload = {"fq": ["lsid:https://biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296"]}
    group_by1 = ["year"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL="https://biocache-ws.ala.org.au/ws/occurrences/search?disableAllQualityfilters=true&",method="GET",group_by=group_by1, filters=filters2,payload=payload)
    assert output.shape[1] > 1

# test galah_group_by with one filter (galah_filter()) and two group_by
def test_galah_group_by_multiple_groups_australia():
    # third test to test single filter
    galah.galah_config(atlas="Australia")
    payload = {"fq": ["lsid:https://biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296"]}
    group_by2 = ["year","basisOfRecord"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL="https://biocache-ws.ala.org.au/ws/occurrences/search?disableAllQualityfilters=true&",method="GET",group_by=group_by2,filters=filters1,payload=payload)
    assert output.shape[1] > 1

# test galah_group_by with one filter (galah_filter()) and two group_by, with expand = True
def test_galah_group_by_multiple_groups_multiple_filters_australia():
    # test to test single filter and expand
    galah.galah_config(atlas="Australia")
    payload = {"fq": ["lsid:https://biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296"]}
    group_by2 = ["year","basisOfRecord"]
    filters1 = "year>2010"
    output = galah.galah_group_by(URL="https://biocache-ws.ala.org.au/ws/occurrences/search?disableAllQualityfilters=true&",method="GET",group_by=group_by2, filters=filters1,payload=payload)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and two group_by
def test_galah_group_by_multiple_groups_multiple_filters_expand_false_australia():
    galah.galah_config(atlas="Australia")
    payload = {"fq": ["lsid:https://biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296"]}
    group_by2 = ["year","basisOfRecord"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL="https://biocache-ws.ala.org.au/ws/occurrences/search?disableAllQualityfilters=true&",method="GET",group_by=group_by2, filters=filters2,payload=payload)
    assert output.shape[1] > 1

# test galah_group_by with two filters (galah_filter()) and two group_by, with expand = True
def test_galah_group_by_multiple_groups_multiple_filters_expand_true_australia():
    galah.galah_config(atlas="Australia")
    payload = {"fq": ["lsid:https://biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296"]}
    group_by2 = ["year","basisOfRecord"]
    filters2 = ["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    output = galah.galah_group_by(URL="https://biocache-ws.ala.org.au/ws/occurrences/search?disableAllQualityfilters=true&",method="GET",group_by=group_by2, filters=filters2,payload=payload)
    assert output.shape[1] > 1

# search_all() - assertions using "AMBIGUOUS_COLLECTION"
def test_search_all_assertions_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="collection")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - assertions using "collection" and column name "description"
def test_search_all_assertions_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(assertions=True)
    total_search_all = galah.search_all(assertions="status",column_name="name")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Australia"
def test_search_all_atlases_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Australia")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - atlases using "Australia" and column name "institution"
def test_search_all_atlases_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(atlases=True)
    total_search_all = galah.search_all(atlases="Australia",column_name="institution")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - apis using "Australia"
def test_search_all_apis_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="Australia")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - apis using "collection" and column name "systems"
def test_search_all_apis_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(apis=True)
    total_search_all = galah.search_all(apis="collection",column_name="system")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - collection using "Agricultural"
def test_search_all_collection_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="Agricultural")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - collection using "Agricultural" and column name "uid"
def test_search_all_collection_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(collection=True)
    total_search_all = galah.search_all(collection="85",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - datasets using "Torres"
def test_search_all_datasets_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="Torres")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - datasets using "4047" and column_name "uid"
def test_search_all_datasets_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(datasets=True)
    total_search_all = galah.search_all(datasets="4047",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - fields using "accepted"
def test_search_all_fields_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="accepted")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - fields using "field" and column_nane "info"
def test_search_all_fields_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(fields=True)
    total_search_all = galah.search_all(fields="layer",column_name="type")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - licences using "accepted"
def test_search_all_licences_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(licences=True)
    total_search_all = galah.search_all(licences="Creative")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - licences using "CC BY" and column_name "acronym"
def test_search_all_licences_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(licences=True)
    total_search_all = galah.search_all(licences="CC BY",column_name="acronym")
    assert total_search_all.shape[0] < total_show_all.shape[0]
        
# search_all() - lists using "Quadrat"
def test_search_all_lists_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="Quadrat")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - lists using "SPATIAL" and column_name "listType"
def test_search_all_lists_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(lists=True)
    total_search_all = galah.search_all(lists="SPATIAL",column_name="listType")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - profiles using "ALA"
def test_search_all_profiles_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(profiles=True)
    total_search_all = galah.search_all(profiles="ALA")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - profiles using "ALA" and column_name "shortName"
def test_search_all_profiles_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(profiles=True)
    total_search_all = galah.search_all(profiles="ALA",column_name="shortName")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - providers using "Ecological"
def test_search_all_providers_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="Ecological")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - providers using "1518" and column_name "uid"
def test_search_all_providers_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(providers=True)
    total_search_all = galah.search_all(providers="1518",column_name="uid")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "kingdom"
def test_search_all_ranks_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="kingdom")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - ranks using "0" and column_name "id"
def test_search_all_ranks_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(ranks=True)
    total_search_all = galah.search_all(ranks="0",column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]

# search_all() - reasons using "conservation"
def test_search_all_reasons_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="conservation")
    assert total_search_all.shape[0] < total_show_all.shape[0]
    
# search_all() - reasons using "0" and column_name "id"
def test_search_all_reasons_column_name_australia():
    galah.galah_config(atlas="Australia")
    total_show_all = galah.show_all(reasons=True)
    total_search_all = galah.search_all(reasons="0",column_name="id")
    assert total_search_all.shape[0] < total_show_all.shape[0]

def test_show_values_australia():
    galah.galah_config(atlas="Australia")
    first_output = galah.show_values(field="basisOfRecord")
    assert first_output.shape[0] > 0

def test_search_values_australia():
    galah.galah_config(atlas="Australia")
    first_output = galah.show_values(field="basisOfRecord")
    second_output = galah.search_values(field="basisOfRecord",value="OBS")
    assert first_output.shape[0] > second_output.shape[0]

# first test for atlas_occurrences() - check if search_taxa() is working
def test_atlas_occurrences_taxa_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes")
    assert occurrences.shape[0] > 1

# second test for atlas_occurrences() - check if galah_select() is working
def test_atlas_occurrences_taxa_fields_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",fields=['decimalLatitude', 'decimalLongitude'])
    # columns
    assert occurrences.shape[1] == 2

# third test for atlas_occurrences() - check if galah_filter() is working with this
def test_atlas_occurrences_taxa_filters_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2020")
    assert occurrences2.shape[0] < occurrences1.shape[0]

# fourth test for atlas_occurrences() - check if galah_select() and galah_filter() are working concurrently
def test_atlas_occurrences_taxa_filter_fields_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",filters="year=2020",fields=['decimalLatitude', 'decimalLongitude'])
    assert occurrences.shape[1] == 2

# testing atlas occurrences with multiple filters
def test_atlas_occurrences_taxa_filters2_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    filters=["year>2018","basisOfRecord=HUMAN_OBSERVATION"]
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes",filters=filters)
    assert occurrences2.shape[0] < occurrences1.shape[0]

# testing atlas occurrences with multiple filters and fields
def test_atlas_occurrences_taxa_filters_fields_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",filters=["year>2018","basisOfRecord=HUMAN_OBSERVATION"],
                                           fields=['decimalLatitude', 'decimalLongitude'])
    assert occurrences.shape[1] == 2

# test data quality data profile is working
def test_atlas_occurrences_taxa_filters_data_profile_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    occurrences1 = galah.atlas_occurrences(taxa="Vulpes vulpes")
    galah.galah_config(data_profile="ALA")
    occurrences2 = galah.atlas_occurrences(taxa="Vulpes vulpes",use_data_profile=True)
    galah.galah_config(data_profile=None)
    assert occurrences2.shape[0] < occurrences1.shape[0]

# galah_geolocate integration tests here
def test_atlas_counts_geolocate_polygon():
    test_shape = shapely.box(143,-29,148,-28)
    counts = galah.atlas_counts(polygon=test_shape)
    assert counts["totalRecords"][0] > 0

# galah_geolocate integration tests here
def test_atlas_counts_geolocate_bbox():
    test_shape = shapely.box(143,-29,148,-28)
    counts = galah.atlas_counts(bbox=test_shape)
    assert counts["totalRecords"][0] > 0

def test_atlas_counts_geolocate_bbox_dict():
    counts = galah.atlas_counts(bbox={"xmin": 143,"ymin": -29,"xmax": 148,"ymax": -28})
    assert counts["totalRecords"][0] > 0

def test_atlas_counts_geolocate_polygon_taxa():
    test_shape = shapely.box(143,-29,148,-28)
    counts = galah.atlas_counts(taxa="reptilia",polygon=test_shape)
    assert counts["totalRecords"][0] > 0

def test_atlas_counts_geolocate_bbox_taxa():
    test_shape = shapely.box(143,-29,148,-28)
    counts = galah.atlas_counts(taxa="reptilia",bbox=test_shape)
    assert counts["totalRecords"][0] > 0

# galah_geolocate integration tests here
def test_atlas_occurrences_geolocate_polygon():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    test_shape = shapely.box(143,-29,148,-28)
    occurrences = galah.atlas_occurrences(polygon=test_shape)
    assert occurrences.shape[0] > 0

# galah_geolocate integration tests here
def test_atlas_occurrences_geolocate_bbox():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    test_shape = shapely.box(143,-29,148,-28)
    occurrences = galah.atlas_occurrences(bbox=test_shape)
    assert occurrences.shape[0] > 0

def test_atlas_occurrences_geolocate_bbox_dict():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(bbox={"xmin": 143,"ymin": -29,"xmax": 148,"ymax": -28})
    assert occurrences.shape[0] > 0

def test_atlas_occurrences_geolocate_polygon_taxa():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    test_shape = shapely.box(143,-29,148,-28)
    occurrences = galah.atlas_occurrences(taxa="reptilia",polygon=test_shape)
    assert occurrences.shape[0] > 0

def test_atlas_occurrences_geolocate_bbox_taxa():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    test_shape = shapely.box(143,-29,148,-28)
    occurrences = galah.atlas_occurrences(taxa="reptilia",bbox=test_shape)
    assert occurrences.shape[0] > 0

def test_atlas_occurrences_mint_doi():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",mint_doi=True)
    assert occurrences.shape[0] > 0

def test_atlas_occurrences_doi():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    occurrences = galah.atlas_occurrences(doi="https://doi.org/10.26197/ala.e413b946-8959-41f8-9ae9-897d86029844")
    assert occurrences.shape[0] > 0

#test if it can get a taxa and return output
def test_atlas_media_taxa_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    output = galah.atlas_media(taxa="Ornithorhynchus anatinus")
    assert output.shape[0] > 1

# test if the filters component of atlas_media is working
def test_atlas_media_filters_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    raw_output = galah.atlas_media(taxa="Ornithorhynchus anatinus")
    filters = ["year=2020","decimalLongitude>153.0"]
    filtered_output = galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=filters)
    assert raw_output.shape[0] > filtered_output.shape[0]

def test_atlas_media_multimedia_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    multimedia="images"
    raw_output = galah.atlas_media(taxa="Ornithorhynchus anatinus")
    multimedia_output = galah.atlas_media(taxa="Ornithorhynchus anatinus",multimedia=multimedia)
    assert multimedia_output.shape[0] > 0

def test_atlas_media_filters_multimedia_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    multimedia="images"
    raw_output = galah.atlas_media(taxa="Ornithorhynchus anatinus")
    filters = ["year=2020", "decimalLongitude>153.0"]
    multimedia_output = galah.atlas_media(taxa="Ornithorhynchus anatinus",multimedia=multimedia,filters=filters)
    assert raw_output.shape[0] > multimedia_output.shape[0]
    #filters=["year=2020","decimalLongitude>153.0"],collect=True,path="test"

def test_atlas_media_filters_multimedia_collect_path_australia():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    multimedia="images"
    filters = ["year=2020", "decimalLongitude>153.0"]
    path="test"
    multimedia_output = galah.atlas_media(taxa="Ornithorhynchus anatinus",multimedia=multimedia,filters=filters,collect=True,path=path)
    files = os.listdir(path)
    assert len(files) > 0

def test_atlas_counts_no_valid_taxa():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    species = 'Macronycteris commersoni'
    counts = galah.atlas_counts(taxa=species,filters=["cl22=Tasmania"]) 
    assert counts == None

def test_atlas_occurrences_no_valid_taxa():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au")
    species = 'Macronycteris commersoni'
    occurrences = galah.atlas_occurrences(taxa=species,filters=["cl22=Tasmania"],fields=["scientificName","decimalLatitude","decimalLongitude"])
    assert occurrences == None

def test_atlas_counts_galah_config_custom_file():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au",config_file='./temp_config_atlas_counts.ini')
    counts = galah.atlas_counts(config_file='./temp_config_atlas_counts.ini')
    assert counts['totalRecords'][0] > 0

def test_atlas_occurrences_galah_config_custom_file():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au",config_file='./temp_config_atlas_occurrences.ini')
    occurrences = galah.atlas_occurrences(taxa="Vulpes vulpes",config_file='./temp_config_atlas_occurrences.ini')
    assert occurrences.shape[0] > 0

def test_atlas_media_galah_config_custom_file():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au",config_file='./temp_config_atlas_media.ini')
    filters = ["year=2020","decimalLongitude>153.0"]
    output = galah.atlas_media(taxa="Ornithorhynchus anatinus",filters=filters,config_file='./temp_config_atlas_media.ini')
    assert output.shape[0] > 0

def test_atlas_species_Australia_species_australia_galah_config_custom_file():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au",config_file='./temp_config_atlas_species.ini')
    galah.galah_config(atlas="Australia")
    taxa = "Heleioporus"
    species_table = galah.atlas_species(taxa=taxa,config_file='./temp_config_atlas_species.ini')
    assert species_table.shape[0] > 0
#'''