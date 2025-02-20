import galah
import os,configparser

# unit test for galah_group_by
def test_galah_group_by_1():
    URL = "https://biocache-ws.ala.org.au/ws/occurrence/search?fq=%28lsid%3Ahttps%3A//biodiversity.org.au/afd/taxa/2869ce8a-8212-46c2-8327-dfb7fabb8296%29"
    groups = ["year"]
    output = galah.galah_group_by(URL,method="GET",group_by=groups,expand=False)
    assert output.shape[0] > 1
    assert output.shape[1] > 1

# unit test for galah.atlas_counts()
def test_atlas_counts():
    # first test is to test if galah.atlas_counts() returns greater than 0
    galah.galah_config(atlas="Australia")
    output = galah.atlas_counts()
    assert output['totalRecords'][0] > 0

def test_galah_config():
    galah.galah_config(email="test@example.com")
    configFile = configparser.ConfigParser()
    inifile = os.path.join(galah.__path__[0], 'config.ini')
    configFile.read(inifile)
    assert configFile['galahSettings']['email'] == "test@example.com"

def test_galah_resetemail():
    galah.galah_config(email="amanda.buyan@csiro.au")
    configFile = configparser.ConfigParser()
    inifile = os.path.join(galah.__path__[0], 'config.ini')
    configFile.read(inifile)
    assert configFile['galahSettings']['email'] == "amanda.buyan@csiro.au"

def test_galah_changeatlas():
    galah.galah_config(atlas="Australia")
    configFile = configparser.ConfigParser()
    inifile = os.path.join(galah.__path__[0], 'config.ini')
    configFile.read(inifile)
    assert configFile['galahSettings']['atlas'] == "Australia"

def test_galah_config_custom_file():
    galah.galah_config(atlas="Australia",email="ala4r@ala.org.au",config_file='./temp_config.ini')
    temp_config = galah.galah_config()
    assert temp_config is not None