# -------------------------------------------------------
# atlas titled functions
# -------------------------------------------------------
# from .atlas_citation import atlas_citation
from .atlas_counts import atlas_counts
from .atlas_media import atlas_media
from .atlas_occurrences import atlas_occurrences
from .atlas_species import atlas_species
# drop this from the release, as it might not be used all that often?? <== R version possibly broken
#from .atlas_taxonomy import atlas_taxonomy

#-------------------------------------------------------
# galah titled functions
#-------------------------------------------------------
from .galah_config import galah_config
from .galah_filter import galah_filter
# from .galah_geolocate import galah_geolocate
from .galah_group_by import galah_group_by
from .galah_select import galah_select

#-------------------------------------------------------
# search and show titled functions
#-------------------------------------------------------
from .search_all import search_all
# from .search_identifiers import search_identifiers
# from .search_media import search_media
from .search_taxa import search_taxa
from .show_all import show_all
from .search_all import search_all
from .show_values import show_values
from .search_values import search_values

#-------------------------------------------------------
# version
#-------------------------------------------------------
__version__ = "1.0.0"

# try this
#from galah import *

# test this
__all__=["atlas_counts","atlas_media","atlas_occurrences","atlas_species","galah_config","galah_filter",
         "galah_group_by","galah_select","search_all","search_taxa","show_all","search_all","show_values",
         "search_values"]