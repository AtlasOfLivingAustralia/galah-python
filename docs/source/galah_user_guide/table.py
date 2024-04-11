import galah
import pandas as pd

# "France",
atlases = ["Australia","Brazil","GBIF","Guatemala","Spain","Sweden"]
counts_dict = {"Atlas": [], "Total Records": []}
for atlas in atlases:
    galah.galah_config(atlas=atlas)
    counts_dict["Atlas"].append(atlas)
    counts_dict["Total Records"].append(galah.atlas_counts()["totalRecords"][0])
print(pd.DataFrame(counts_dict))