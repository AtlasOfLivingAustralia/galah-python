import configparser,os,urllib
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
                add_email=False,
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
    rows = specific_atlas[specific_atlas[column1].astype(str).str.contains(column1value, case=True, na=False)]

    # check to see if there are two columns to filter by
    if column2 is None and column2value is None:
        if len(rows.loc[rows[column1].astype(str).str.contains(column1value, case=True, na=False)].index) > 1:
            raise ValueError("There are more than one possible APIs - need to specify column2 and column2value")
        else:
            # dataFrame.loc[dataFrame[column_name].astype(str).str.contains(assertions, case=True, na=False)].sort_values('name', key=lambda x: x.str.len()))
            index = rows[rows[column1] == column1value].index[0]
            baseURL = rows[rows[column1] == column1value]['api_url'][index]
    # add a test here
    elif column2 is not None and column2value is not None:
        if len(rows[rows[column2].astype(str).str.contains(column2value,case=True,na=False)].index) > 1:
            raise ValueError("There are more than one possible APIs with column2 and column2value - choose this API another way")
        else:
            index = rows[rows[column2].astype(str).str.contains(column2value,case=True,na=False)].index[0]
            #baseURL = rows[rows[column1] == column1value]['api_url'][index]
            baseURL = rows.loc[rows[column1].astype(str).str.contains(column1value, case=True, na=False)]['api_url'][index]
    else:
        raise ValueError("A value needs to be provided for both column2 and column2 value")

    if add_email:

        # email for querying
        if configs['galahSettings']['email'] is None:
            raise ValueError("You need to provide a valid email address for this function to be able to download data")
        else:
            if "download" in baseURL:
                baseURL += "?email={}&dwcHeaders=True".format(urllib.parse.quote(configs['galahSettings']['email']))
                baseURL += "&reasonTypeId={}".format(configs['galahSettings']['reason'])
            else:
                baseURL += "&email={}&dwcHeaders=True".format(urllib.parse.quote(configs['galahSettings']['email']))
                baseURL += "&reasonTypeId={}".format(urllib.parse.quote(configs['galahSettings']['email']))
            if configs['galahSettings']['email_notify'].lower() == "false":
                baseURL += "&emailNotify=false&"
            elif configs['galahSettings']['email_notify'].lower() == "true":
                baseURL += "&emailNotify=true&" # check if this is correct
            else:
                raise ValueError("email_notify option should be set to either True or False - please set that with "
                                 "galah_config(email_notify=\"False\") or galah_config(email_notify=\"True\")")

    return baseURL
