'''
Function for configuring
'''

import configparser,os

# how I did this:
# https://www.codeproject.com/Articles/5319621/Configuration-Files-in-Python
# run this first at installation
def galah_config(email=None,atlas=None):

    # check to see if there are any arguments to update
    if email is None and atlas is None:
        raise ValueError("Please specify a value you would like to change, i.e. galah_config(email=\"youremail@example.come\")")

    # open the config parser
    configParser = configparser.ConfigParser()

    # read the config file
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configParser.read(inifile)

    # update the field to change
    if email is not None:
        configParser["galahSettings"]["email"] = email
    if atlas is not None:
        configParser["galahSettings"]["atlas"] = atlas
    # add things for data profiles here

    # write to file
    with open(inifile,"w") as fileObject:
        configParser.write(fileObject)
