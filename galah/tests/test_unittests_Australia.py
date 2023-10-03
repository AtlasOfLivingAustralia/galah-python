import unittest2
import galah
import os,configparser

class test_galah_Australia(unittest2.TestCase):

    # unit test for galah_group_by
    def test_galah_group_by_1(self):
        URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
        groups = ["year"]
        output = galah.galah_group_by(URL,method="GET",group_by=groups,expand=False)
        self.assertGreater(output.shape[0], 1)
        self.assertGreater(output.shape[1], 1)
    
    # unit test for galah.atlas_counts()
    def test_atlas_counts(self):
        # first test is to test if galah.atlas_counts() returns greater than 0
        galah.galah_config(atlas="Australia")
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