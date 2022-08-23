'''
Function for configuring
'''

import configparser,glob

# how I did this:
# https://www.codeproject.com/Articles/5319621/Configuration-Files-in-Python
# run this first at installation
def config(fieldToChange=None):

    # check to
    if fieldToChange is None:
        raise ValueError("Please specify a value for the configuration file, i.e. config(['email','name@email.com'])")

    # open the config parser
    configParser = configparser.ConfigParser()

    # read the config file
    inifile=glob.glob('**/galah/config.ini',recursive=True)[0]
    configParser.read(inifile)

    # update the field to change
    configParser["galahSettings"][fieldToChange[0]]=fieldToChange[1]

    # write to file
    with open(inifile,"w") as fileObject:
        configParser.write(fileObject)
