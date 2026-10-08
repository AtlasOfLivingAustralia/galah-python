import configparser
import os

import galah


# unit test for galah.atlas_counts()
def test_atlas_counts():
    # first test is to test if galah.atlas_counts() returns greater than 0
    galah.galah_config(atlas="Australia")
    output = galah.atlas_counts()
    assert output["totalRecords"][0] > 0


def test_galah_config():
    galah.galah_config(email="test@example.com")
    configFile = configparser.ConfigParser()
    inifile = os.path.join(galah.__path__[0], "config.ini")
    configFile.read(inifile)
    assert configFile["galahSettings"]["email"] == "test@example.com"


def test_galah_resetemail():
    galah.galah_config(email="amanda.buyan@csiro.au")
    configFile = configparser.ConfigParser()
    inifile = os.path.join(galah.__path__[0], "config.ini")
    configFile.read(inifile)
    assert configFile["galahSettings"]["email"] == "amanda.buyan@csiro.au"


def test_galah_changeatlas():
    galah.galah_config(atlas="Australia")
    configFile = configparser.ConfigParser()
    inifile = os.path.join(galah.__path__[0], "config.ini")
    configFile.read(inifile)
    assert configFile["galahSettings"]["atlas"] == "Australia"


def test_galah_config_custom_file():
    galah.galah_config(atlas="Australia", email="ala4r@ala.org.au", config_file="./temp_config.ini")
    temp_config = galah.galah_config()
    assert temp_config is not None
