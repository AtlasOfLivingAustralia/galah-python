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

    # one unit test for galah_filter
    def test_galah_filter1(self):
        output = galah.galah_filter("year=2019")
        self.assertEqual(output,"%28year%3A%222019%22%29")
    
    # second unit test for galah_filter
    def test_galah_filter2(self):
        output=""
        for f in ["year=2019","basisOfRecord=HUMAN_OBSERVATION"]:
            output += galah.galah_filter(f)
        self.assertEqual(output,"%28year%3A%222019%22%29%28basisOfRecord%3A%22HUMAN_OBSERVATION%22%29")
    
    # third unit test for galah_filter - ifgroupBy is true
    def test_galah_filter3(self):
        output = galah.galah_filter("year=2019",ifgroupBy=True)
        self.assertEqual(output,"%28year%3A%222019%22%29")

    # fourth unit test for galah_filter - filter parameter has spaces in it
    def test_galah_filter4(self):
        output = galah.galah_filter("state = New South Wales")
        self.assertEqual(output, "%28state%3A%22New%20South%20Wales%22%29")

    # fifth unit test for galah_filter - filter parameter has spaces and testing == operator
    def test_galah_filter5(self):
        output = galah.galah_filter("dataResourceName == iNaturalist Australia")
        self.assertEqual(output, "%28dataResourceName%3A%22iNaturalist%20Australia%22%29")
    
    # sixth unit test for galah_filter - testing > operator
    def test_galah_filter6(self):
        output = galah.galah_filter("decade>2000")
        self.assertEqual(output, "%28decade:%5B2000%20TO%20*%5d%20AND%20-%28decade%3A%222000%22%29%29")

    # seventh unit test for galah_filter - testing > operator
    def test_galah_filter7(self):
        output = galah.galah_filter("year<1900")
        self.assertEqual(output, '%28year%3A%5B*%20TO%201900%5d%20AND%20-%28year%3A"1900"%29%29')

    # eighth unit test for galah_filter - testing >= and => operator
    def test_galah_filter8(self):
        output1 = galah.galah_filter("month >= 8")
        self.assertEqual(output1, "%28month%3A%5B8%20TO%20%2A%5d%29")

    # ninth unit test for galah_filter - testing <= and =< operator
    def test_galah_filter9(self):
        output1 = galah.galah_filter("decade <= 1980")
        self.assertEqual(output1, "%28decade%3A%5B*%20TO%201980%5d%29")

    # tenth unit test for galah_filter - testing != and =! operator
    def test_galah_filter10(self):
        output1 = galah.galah_filter("habitat != Marine")
        self.assertEqual(output1, '-%28habitat%3A%22Marine%22%29')
    
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
    
    def test_galah_resetemail(self):
        galah.galah_config(email="amanda.buyan@csiro.au")
        configFile = configparser.ConfigParser()
        inifile = os.path.join(galah.__path__[0], 'config.ini')
        configFile.read(inifile)
        self.assertEqual(configFile['galahSettings']['email'],"amanda.buyan@csiro.au")
    
    def test_galah_changeatlas(self):
        galah.galah_config(atlas="Australia")
        configFile = configparser.ConfigParser()
        inifile = os.path.join(galah.__path__[0], 'config.ini')
        configFile.read(inifile)
        self.assertEqual(configFile['galahSettings']['atlas'],"Australia")
    
    #'''
    # Austria - comment out if we don't release the other APIs with it
    '''
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

    def test_show_all_collection_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(collection=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_austria(self):
        galah.galah_config(atlas="Austria")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

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

    # Brazil - comment out if we don't release the other APIs with it
    #'''
    def test_show_all_assertions_brazil(self):
        galah.galah_config(atlas="Brazil")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_brazil(self):
        galah.galah_config(atlas="Brazil")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_brazil(self):
        galah.galah_config(atlas="Brazil")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_collection_brazil(self):
        galah.galah_config(atlas="Brazil")
        output = galah.show_all(collection=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_brazil(self):
        galah.galah_config(atlas="Brazil")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_fields_brazil(self):
        galah.galah_config(atlas="Brazil")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_lists_brazil(self):
        galah.galah_config(atlas="Brazil")
        output = galah.show_all(lists=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_brazil(self):
        galah.galah_config(atlas="Brazil")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_ranks_brazil(self):
        galah.galah_config(atlas="Brazil")
        output = galah.show_all(ranks=True)
        self.assertGreater(output.shape[1],1)
    #'''

    # Canada - comment out if we don't release the other APIs with it
    '''
    def test_show_all_assertions_canada(self):
        galah.galah_config(atlas="Canada")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_canada(self):
        galah.galah_config(atlas="Canada")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_canada(self):
        galah.galah_config(atlas="Canada")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_canada(self):
        galah.galah_config(atlas="Canada")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_fields_canada(self):
        galah.galah_config(atlas="Canada")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_canada(self):
        galah.galah_config(atlas="Canada")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_reasons_canada(self):
        galah.galah_config(atlas="Canada")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)
    #'''

    # Estonia - comment out if we don't release the other APIs with it
    '''
    def test_show_all_assertions_estonia(self):
        galah.galah_config(atlas="Estonia")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_estonia(self):
        galah.galah_config(atlas="Estonia")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_estonia(self):
        galah.galah_config(atlas="Estonia")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_collection_estonia(self):
        galah.galah_config(atlas="Estonia")
        output = galah.show_all(collection=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_estonia(self):
        galah.galah_config(atlas="Estonia")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_fields_estonia(self):
        galah.galah_config(atlas="Estonia")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_estonia(self):
        galah.galah_config(atlas="Estonia")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)
    #'''

    # France - comment out if we don't release the other APIs with it
    '''
    def test_show_all_assertions_france(self):
        galah.galah_config(atlas="France")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_france(self):
        galah.galah_config(atlas="France")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_france(self):
        galah.galah_config(atlas="France")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_collection_france(self):
        galah.galah_config(atlas="France")
        output = galah.show_all(collection=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_france(self):
        galah.galah_config(atlas="France")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_fields_france(self):
        galah.galah_config(atlas="France")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_france(self):
        galah.galah_config(atlas="France")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)
    #'''

    # Guatemala - comment out if we don't release the other APIs with it
    '''
    def test_show_all_assertions_guatemala(self):
        galah.galah_config(atlas="Guatemala")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_guatemala(self):
        galah.galah_config(atlas="Guatemala")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_guatemala(self):
        galah.galah_config(atlas="Guatemala")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_collection_guatemala(self):
        galah.galah_config(atlas="Guatemala")
        output = galah.show_all(collection=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_guatemala(self):
        galah.galah_config(atlas="Guatemala")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_fields_guatemala(self):
        galah.galah_config(atlas="Guatemala")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_guatemala(self):
        galah.galah_config(atlas="Guatemala")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_reasons_guatemala(self):
        galah.galah_config(atlas="Guatemala")
        output = galah.show_all(reasons=True)
        self.assertGreater(output.shape[1], 1)
    #'''

    # Spain - comment out if we don't release the other APIs with it
    #'''
    def test_show_all_assertions_spain(self):
        galah.galah_config(atlas="Spain")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_spain(self):
        galah.galah_config(atlas="Spain")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_spain(self):
        galah.galah_config(atlas="Spain")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_spain(self):
        galah.galah_config(atlas="Spain")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_fields_spain(self):
        galah.galah_config(atlas="Spain")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_spain(self):
        galah.galah_config(atlas="Spain")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_reasons_spain(self):
        galah.galah_config(atlas="Spain")
        output = galah.show_all(reasons=True)
        self.assertGreater(output.shape[1], 1)
    #'''

    # Sweden - comment out if we don't release the other APIs with it
    '''
    def test_show_all_assertions_sweden(self):
        galah.galah_config(atlas="Sweden")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_sweden(self):
        galah.galah_config(atlas="Sweden")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_sweden(self):
        galah.galah_config(atlas="Sweden")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_sweden(self):
        galah.galah_config(atlas="Sweden")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_fields_sweden(self):
        galah.galah_config(atlas="Sweden")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_sweden(self):
        galah.galah_config(atlas="Sweden")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_reasons_sweden(self):
        galah.galah_config(atlas="Sweden")
        output = galah.show_all(reasons=True)
        self.assertGreater(output.shape[1], 1)
    #'''

    # UK - comment out if we don't release the other APIs with it
    '''
    def test_show_all_assertions_uk(self):
        galah.galah_config(atlas="United Kingdom")
        output = galah.show_all(assertions=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_atlases_uk(self):
        galah.galah_config(atlas="United Kingdom")
        output = galah.show_all(atlases=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_apis_uk(self):
        galah.galah_config(atlas="United Kingdom")
        output = galah.show_all(apis=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_datasets_uk(self):
        galah.galah_config(atlas="United Kingdom")
        output = galah.show_all(datasets=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_fields_uk(self):
        galah.galah_config(atlas="United Kingdom")
        output = galah.show_all(fields=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_providers_uk(self):
        galah.galah_config(atlas="United Kingdom")
        output = galah.show_all(providers=True)
        self.assertGreater(output.shape[1],1)

    def test_show_all_reasons_uk(self):
        galah.galah_config(atlas="United Kingdom")
        output = galah.show_all(reasons=True)
        self.assertGreater(output.shape[1], 1)
    #'''

    # should include a unit test for this but I believe they are all integration tests
    def test_atlas_occurrences_australia(self):
        galah.galah_config(atlas="Australia",email="amanda.buyan@csiro.au")
        a=galah.atlas_occurrences(test=True)
        self.assertIsNone(a)

    def test_show_values_australia(self):
        galah.galah_config(atlas="Australia")
        output = galah.show_values(field="basisOfRecord")
        self.assertGreater(output.shape[1], 1)

if __name__ == "__main__":
    unittest2.main()
