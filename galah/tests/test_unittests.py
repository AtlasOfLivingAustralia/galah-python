'''
'''
import unittest2
import galah
import pandas as pd
import os,configparser

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
