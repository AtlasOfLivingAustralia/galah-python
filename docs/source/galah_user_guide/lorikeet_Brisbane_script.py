import geopandas as gpd
import pandas as pd
import galah
import shapely
from shapely.ops import unary_union
import matplotlib.pyplot as plt
import sys

when_to_stop = sys.argv[1]

# first, get all parts within the Brisbane postcode 4075
parks = gpd.read_file('galah_user_guide/Park___Locations.shp') 
parks = parks.to_crs(4326)
brisbane_parks = parks[parks["POST_CODE"] == '4075'].reset_index(drop=True)
if when_to_stop == "First":
    print(brisbane_parks.head(10))
    sys.exit()

# second, get a shape of all the Brisbane parks and draw a bounding box around it
brisbane_parks_all = gpd.GeoSeries(unary_union(brisbane_parks["geometry"]))
brisbane_parks_bbox = brisbane_parks_all.bounds

#-------------------------------------------------------------------------------------------------------
plot_brisbane_parks_bbox = shapely.box(xmin=brisbane_parks_bbox["minx"][0],
                                       xmax=brisbane_parks_bbox["maxx"][0],
                                       ymin=brisbane_parks_bbox["miny"][0],
                                       ymax=brisbane_parks_bbox["maxy"][0]
                                       )
brisbane_parks_all.plot(edgecolor = "#5A5A5A", linewidth = 1, facecolor = "white", figsize = (7,10))
plt.plot(*plot_brisbane_parks_bbox.exterior.xy,color="red")
plt.ylabel("Latitude",size=16,x=.45,y=0.5)
plt.xlabel("Longitude",size=16)
plt.savefig("galah_user_guide/brisbane_parks_and_bbox.png",dpi=300)
#-------------------------------------------------------------------------------------------------------

if when_to_stop == "Second":
    print(brisbane_parks_bbox)
    sys.exit()

# third, find all occurrences of Trichoglossus chlorolepidotus in the bounding box in 2022
import galah
galah.galah_config(email="amanda.buyan@csiro.au")
lorikeet_brisbane = galah.atlas_occurrences(
     taxa="Trichoglossus chlorolepidotus",
     filters="year>=2020",
     bbox=brisbane_parks_bbox,
)

# plots
brisbane_parks_all.plot(edgecolor = "#5A5A5A", linewidth = 1, facecolor = "white", figsize = (7,10))
plt.plot(*plot_brisbane_parks_bbox.exterior.xy,color="red")
plt.ylabel("Latitude",size=16,x=.45,y=0.5)
plt.xlabel("Longitude",size=16)
plt.scatter(lorikeet_brisbane["decimalLongitude"],lorikeet_brisbane["decimalLatitude"],alpha=0.5,color="orange",label="Lorikeet occurrences")
plt.legend(loc=(0.5,0.96))
plt.savefig("galah_user_guide/lorikeets_on_map_shapefile.png",dpi=300)

# stop at this point
if when_to_stop == "Third":
    print(lorikeet_brisbane)
    sys.exit()

# fourth, go through each park, add counts to the shapefile(?), then report the counts
brisbane_parks["count"] = pd.Series([0 for i in range(len(brisbane_parks))])
for i,park in brisbane_parks.iterrows():
    points = [(x,y) for x,y in zip(lorikeet_brisbane["decimalLongitude"], lorikeet_brisbane["decimalLatitude"]) if shapely.contains_xy(park["geometry"],x,y)]
    brisbane_parks.at[i,"count"] = len(points)

brisbane_parks_counts = brisbane_parks[["PARK_NAME","count"]].sort_values("count",ascending=False).reset_index(drop=True)
print(brisbane_parks_counts.head(10))