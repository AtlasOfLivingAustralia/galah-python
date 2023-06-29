'''
run pytest integration_tests_galah.py
'''
import pytest,os
import galah

'''
# Austria 

>>> galah.galah_config(atlas="Austria")
>>> galah.atlas_media(taxa="Sehirus luctuosus")
galah.atlas_counts(taxa="Sehirus luctuosus",filters="year=2020")
galah.atlas_counts(taxa="Sehirus luctuosus",filters="year>2010)
galah.atlas_counts(taxa="Sehirus luctuosus",filters="year>2010",group_by="year",expand=False)
galah.atlas_species(taxa="Sehirus")

# Brazil
taxa = "Ramphastos toco"
taxa = "Hydrochoens hydrochaeris"
email = ala4r@ala.org.au

# Canada
taxa = "Alces alces"

# Estonia 
taxa = "Canis lupus"

# France
taxa = "Triturus marmoratus"

# Guatemala
taxa = "Herpailurus yagouaroundi"

# Portugal
taxa = "Gallus gallus"

# Spain
taxa = "Vipera latastei"

# Sweden
taxa = "Alces alces"

# UK
taxa - "Luscinia megarhynchos"
'''