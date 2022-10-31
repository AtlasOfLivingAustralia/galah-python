import requests,os,configparser
import pandas as pd
from .show_values import show_values

def search_values(field=None,value=None,column_name=None):

    if value is None:
        raise ValueError("Please specify the field you want to see query-able values for, i.e. field=\"basisOfRecord\"")
    elif type(value) is not str:
        raise TypeError("show_values() only takes a single string as the field argument, i.e. field=\"basisOfRecord\"")

    dataFrame = galah.show_values(field=field)
    print(dataFrame)