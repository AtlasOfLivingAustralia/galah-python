'''
Function for configuring
'''

import configparser,glob,os,sys

# how I did this:
# https://www.codeproject.com/Articles/5319621/Configuration-Files-in-Python
# run this first at installation
def galah_config(fieldToChange=None):

    # check to
    if fieldToChange is None:
        raise ValueError("Please specify a value for the configuration file, i.e. config(['email','name@email.com'])")

    # open the config parser
    configParser = configparser.ConfigParser()

    # read the config file
    inifile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    configParser.read(inifile)

    # update the field to change
    configParser["galahSettings"][fieldToChange[0]]=fieldToChange[1]

    # write to file
    with open(inifile,"w") as fileObject:
        configParser.write(fileObject)
