'''
'''
import unittest2
import galah
import pandas as pd
import os,configparser
#import nose2

'''
# Austria 

taxa="Sehirus luctuosus"

# Brazil
taxa = "Ramphastos toco"
taxa = "Hydrochoens hydrochaeris"

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

class test_galah(unittest2.TestCase):

    # integration test for search_taxa() - have to test get_api_url
    def test_search_taxa_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.search_taxa("Vulpes vulpes")
        self.assertNotEqual(output['taxonConceptID'][0], None)

    # integration test for search_taxa() - have to test get_api_url
    def test_search_taxa_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.search_taxa(taxa="Sehirus luctuosus")
        self.assertNotEqual(output['guid'][0], None)

    # one unit test for galah_filter
    def test_galah_filter1(self):
        output = galah.galah_filter("year=2019")
        self.assertEqual(output,"&fq=year:(2019)")

    # second unit test for galah_filter
    def test_galah_filter2(self):
        output=""
        for f in ["year=2019","basisOfRecord=HUMAN_OBSERVATION"]:
            output += galah.galah_filter(f)
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

    def test_show_all_assertions_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_collections_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(collections=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    # check if this gives errors
    def test_show_all_fields_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_licences_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(licences=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_lists_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(lists=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_profiles_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(profiles=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_reasons_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(reasons=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_ranks_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_all(ranks=True)
        self.assertGreater(output.shape[1],1)

    # Austria - comment out if we don't release the other APIs with it
    #'''
    def test_show_all_assertions_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_collections_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(collections=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    # check if this gives errors
    def test_show_all_fields_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_lists_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(lists=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_reasons_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(reasons=True)
        self.assertGreater(output.shape[1],1)
    #'''

    # should include a unit test for this but I believe they are all integration tests
    def test_atlas_occurrences_australia(self):
        galah.galah_config(atlas="Australia")
        galah.galah_config(email="amanda.buyan@csiro.au")
        a=galah.atlas_occurrences(test=True)
        self.assertIsNone(a)

    def test_show_values_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_values(field="basisOfRecord")
        self.assertGreater(output.shape[1], 1)

if __name__ == "__main__":
    unittest2.main()
