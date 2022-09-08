'''
'''
import unittest2
import galah
import pandas as pd
#import nose2

class test_galah(unittest2.TestCase):

    # unit test for search_taxa()
    def test_search_taxa(self):
        output = galah.search_taxa("Vulpes vulpes")
        self.assertNotEqual(output['taxonConceptID'][0],None)

    # unit test for show_all_fields()
    def test_show_all_fields(self):
        output = galah.show_all_fields()
        self.assertTrue(type(output) is pd.core.frame.DataFrame)
        self.assertGreater(output.shape[0],1)

    # check that the number of rows and columns are
    def test_show_all_values(self):
        output = galah.show_all_values("basisOfRecord")
        self.assertGreater(output.shape[0], 1)
        self.assertGreater(output.shape[1], 1)

    # one unit test for galah_filter
    def test_galah_filter1(self):
        output = galah.galah_filter("year=2019")
        self.assertEqual(output,"&fq=year:(2019)")

    # second unit test for galah_filter
    def test_galah_filter2(self):
        output = galah.galah_filter(["year=2019","basisOfRecord=HUMAN_OBSERVATION"])
        self.assertEqual(output,"&fq=year:(2019)&fq=basisOfRecord:(HUMAN_OBSERVATION)")

    # unit test to make sure galah_select works as intended
    def test_galah_select(self):
        output = galah.galah_select(selectionList=['decimalLatitude','decimalLongitude'])
        self.assertEqual(output,"fields=decimalLatitude%2CdecimalLongitude%2C")

    # unit test for galah_group_by
    def test_galah_group_by_1(self):
        URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
        groups = ["year"]
        output = galah.galah_group_by(URL,groups=groups)
        self.assertGreater(output.shape[0], 1)
        self.assertGreater(output.shape[1], 1)

    # unit test for galah.atlas_counts()
    def test_atlas_counts(self):
        # first test is to test if galah.atlas_counts() returns greater than 0
        output = galah.atlas_counts()
        self.assertGreater(output['totalRecords'][0],0)

    # should include a unit test for this but I believe they are all integration tests
    def test_atlas_occurrences(self):
        #a=galah.atlas_occurrences("Vulpes vulpes")
        #print(a)
        pass

if __name__ == "__main__":
    unittest2.main()