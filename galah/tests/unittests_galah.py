'''
'''
import unittest2
import galah
import pandas as pd
import os,configparser
#import nose2

class test_galah(unittest2.TestCase):

    # unit test for search_taxa()
    def test_search_taxa(self):
        output = galah.search_taxa("Vulpes vulpes")
        self.assertNotEqual(output['taxonConceptID'][0],None)

    # one unit test for galah_filter
    def test_galah_filter1(self):
        output = galah.galah_filter("year=2019")
        self.assertEqual(output,"&fq=year:(2019)")

    # second unit test for galah_filter
    def test_galah_filter2(self):
        output = galah.galah_filter(["year=2019","basisOfRecord=HUMAN_OBSERVATION"])
        self.assertEqual(output,"&fq=year:(2019)&fq=basisOfRecord:(HUMAN_OBSERVATION)")

    # third unit test for galah_filter - ifgroupBy is true
    def test_galah_filter3(self):
        output = galah.galah_filter("year=2019",ifgroupBy=True)
        self.assertEqual(output,"&fq=year:[2019]")

    # unit test to make sure galah_select works as intended
    def test_galah_select(self):
        output = galah.galah_select(selectionList=['decimalLatitude','decimalLongitude'])
        self.assertEqual(output,"fields=decimalLatitude%2CdecimalLongitude%2C")

    # unit test for galah_group_by
    def test_galah_group_by_1(self):
        URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
        groups = ["year"]
        output = galah.galah_group_by(URL,group_by=groups,expand=False)
        self.assertGreater(output.shape[0], 1)
        self.assertGreater(output.shape[1], 1)

    # unit test for galah.atlas_counts()
    def test_atlas_counts(self):
        # first test is to test if galah.atlas_counts() returns greater than 0
        output = galah.atlas_counts()
        self.assertGreater(output['totalRecords'][0],0)

    def test_galah_config(self):
        galah.galah_config(email="test@example.com")
        configFile = configparser.ConfigParser()
        inifile = os.path.join(galah.__path__[0], 'config.ini')
        configFile.read(inifile)
        self.assertEqual(configFile['galahSettings']['email'],"test@example.com")

    def test_show_all_assertions(self):
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases(self):
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis(self):
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_collections(self):
        output = galah.show_all(collections=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets(self):
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    # check if this gives errors
    def test_show_all_fields(self):
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_licences(self):
        output = galah.show_all(licences=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_lists(self):
        output = galah.show_all(lists=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_profiles(self):
        output = galah.show_all(profiles=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers(self):
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_reasons(self):
        output = galah.show_all(reasons=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_ranks(self):
        output = galah.show_all(ranks=True)
        self.assertGreater(output.shape[1],1)

    # should include a unit test for this but I believe they are all integration tests
    def test_atlas_occurrences(self):
        galah.galah_config(email="amanda.buyan@csiro.au")
        a=galah.atlas_occurrences(test=True)
        self.assertIsNone(a)

    def test_show_values(self):
        output = galah.show_values(field="basisOfRecord")
        self.assertGreater(output.shape[1], 1)

if __name__ == "__main__":
    unittest2.main()
