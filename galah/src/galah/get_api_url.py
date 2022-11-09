import configparser,os
import pandas as pd

def readConfig():
    configFile=configparser.ConfigParser()
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configFile.read(inifile)
    return configFile

# get the URL for the API we want to ping for the
def get_api_url(column1=None,
                column1value=None,
                column2=None,
                column2value=None,
                ):

    # check that there is at least column 1 name and column 1 value
    if column1 is None and column1value is None:
        raise ValueError("You need to provide a column name for column1 and value for column1value")
    if column1 is None:
        raise ValueError("You need to provide a column name for column1")
    if column1value is None:
        raise ValueError("You need to provide a value for this function to search for in the column")

    # first, get specific atlas
    atlasfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_config.csv')
    atlaslist = pd.read_csv(atlasfile)
    configs = readConfig()
    specific_atlas = atlaslist[atlaslist['atlas'] == configs['galahSettings']['atlas']]

    # get rows with specific value
    rows = specific_atlas[specific_atlas[column1] == column1value]

    # check to see if there are two columns to filter by
    if column2 is None and column2value is None:
        index = rows[rows[column1] == column1value].index[0]
        return rows[rows[column1] == column1value]['api_url'][index]
    elif column2 is not None and column2value is not None:
        index = rows[rows[column2] == column2value].index[0]
        return rows[rows[column1] == column1value]['api_url'][index]
    else:
        raise ValueError("A value needs to be provided for both column2 and column2 value")
