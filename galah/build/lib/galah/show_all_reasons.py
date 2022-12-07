'''
This is a collection of the search functions from the R galah package

Each function has a description of what it does and what its arguments are
'''

import requests
import pandas as pd

APIs = {
    'Australia': 'https://namematching-ws.ala.org.au/'
}

def show_all_reasons():
    # pseudocode here
    n=1
