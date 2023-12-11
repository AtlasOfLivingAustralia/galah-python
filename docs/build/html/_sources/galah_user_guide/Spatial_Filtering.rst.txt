.. _Spatial Filtering:

Spatial filtering
=================

Adapted from `the Temporal Filtering galah-R article <galah.ala.org.au/R/articles/spatial_filtering.html>`_.

*Callum Waite, Shandiya Balasubramaniam, Amanda Buyan*

Biodiversity queries to the ALA usually require some spatial filtering. Let’s see how spatial data 
are stored in the ALA and a few different methods to spatially filter data with ``{galah}``, ``{shapely}``
and ``{geopandas}``.

Most records in the ALA contain location data in the form of two key fields: ``decimalLatitude`` and 
``decimalLongitude``. As expected, these fields are the decimal coordinates of each occurrence, with south 
and west values denoted by negatives. While there may be some uncertainty in these values (see field 
``coordinateUncertaintyInMeters``), they are generally very accurate.

While these are very important and useful fields, very rarely will we encounter situations that require 
queries directly calling ``decimalLatitude`` and ``decimalLongitude``. Instead, the ALA and galah have a number 
of features that make spatial queries simpler.

Contextual and spatial layers
-----------------------------

Often we want to filter results down to some commonly defined spatial regions, such as states, LGAs or 
IBRA/IMCRA regions. The ALA contains a large range (>100) of contextual and spatial layers, in-built as 
searchable and queriable fields. They are denoted by names beginning with "cl", followed by an identifying 
number that may be up to 6 digits long. These fields are each based on shapefiles, and contain the names of 
the regions in these layers that each record lies in.

We strongly recommend using ``galah.search_all(fields="<your-search-term-here>")`` to check whether a contextual 
layer already exists in the ALA that matches what you require before proceeding with other methods of spatial 
filtering. These fields are all able to be used in the ``filters`` argument of ``atlas_counts``, ``atlas_occurrences``, 
``atlas_species`` or ``atlas_media``, so they are generally easier to use.

Suppose we are interested in querying records of the Red-Necked Avocet (*Recurvirostra novaehollandiae*) in a 
particular protected wetlands, the Coorong wetlands in South Australia. We can search the ALA fields for 
wetlands.

.. prompt:: python

    >>> import galah
    >>> galah.galah_config(email="your-email-here")
    >>> galah.search_all(fields="wetlands")

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas='Australia');print(galah.search_all(fields='wetlands'))"

Our search identifies that layer ``cl901`` seems to match what we are looking for. We can then either view all 
possible values in the field with ``galah.show_values()``, or use ``galah.search_values()`` again for our particular field.

.. prompt:: python

    >>> galah.search_values(field="cl901",value="coorong")

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.search_values(field=\"cl901\",value=\"coorong\"))"

We can filter all occurrences for exact matches with this value, "The Coorong, Lake Alexandrina & Lake Albert". Our galah query can be built 
as follows:

.. prompt:: python

    >>> avocets = galah.atlas_occurrences(
    ...   taxa = "Recurvirostra novaehollandiae",
    ...   filters = "cl901=The Coorong, Lake Alexandrina & Lake Albert"
    ... )
    >>> avocets.head(5)

.. program-output:: python3 -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");avocets = galah.atlas_occurrences(taxa = \"Recurvirostra novaehollandiae\",filters = \"cl901=The Coorong, Lake Alexandrina & Lake Albert\");print(avocets.head(5))"


Shapes and Regions
----------------------

While server-side spatial information is useful, there are likely to be cases where the shapefile or region 
you wish to query will not be pre-loaded as a contextual layer in the ALA. In this case, shapefiles can be 
introduced to the filtering process using the ``{shapely}`` package and the ``polygon`` or ``bbox`` arguments in 
``atlas_counts``, ``atlas_occurrences``, ``atlas_species`` or ``atlas_media``.  Shapefiles can be provided as a
``shapely`` object, the string denoting the polygon itself, or in the base of ``bbox``, a dictionary 
specifying ``xmin``, ``xmax``, ``ymin``, and ``ymax``.  For instance, we might interested in species occurrences in 
King George Square, Brisbane. We can take the ``MULTIPOLYGON`` object for the square (as sourced from the Brisbane City 
Council) and transform it into a ``{shapely}`` object.

.. prompt:: python

    >>> import shapely.wkt
    >>> king_george_square = shapely.wkt.loads("MULTIPOLYGON(((153.0243 -27.46886, 153.0242 -27.46896, 153.0236 -27.46837, 153.0239 -27.46814, 153.0239 -27.46813, 153.0242 -27.46789, 153.0244 -27.46805, 153.0245 -27.46821, 153.0246 -27.46828, 153.0247 -27.46835, 153.0248 -27.46848, 153.0246 -27.4686, 153.0246 -27.46862, 153.0245 -27.46871, 153.0243 -27.46886)))")

We can provide this ``MULTIPOLYGON`` as the argument ``polygon`` in ``atlas_occurrences`` to assess which species 
have been recorded in King George Square.

.. prompt:: python

    >>> species_king_george_square = galah.atlas_occurrences(
    ...   polygon=king_george_square,
    ...   fields=["decimalLatitude", "decimalLongitude", "eventDate", "scientificName", "vernacularName"]  
    ... )
    >>> species_king_george_square.head(10)

.. program-output:: python3 -c "import galah;import shapely.wkt;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);king_george_square = shapely.wkt.loads(\"MULTIPOLYGON(((153.0243 -27.46886, 153.0242 -27.46896, 153.0236 -27.46837, 153.0239 -27.46814, 153.0239 -27.46813, 153.0242 -27.46789, 153.0244 -27.46805, 153.0245 -27.46821, 153.0246 -27.46828, 153.0247 -27.46835, 153.0248 -27.46848, 153.0246 -27.4686, 153.0246 -27.46862, 153.0245 -27.46871, 153.0243 -27.46886)))\");species_king_george_square = galah.atlas_occurrences(polygon=king_george_square,fields=[\"decimalLatitude\", \"decimalLongitude\", \"eventDate\", \"scientificName\", \"vernacularName\"]);print(species_king_george_square)"

This argument can be provided as its string; however, we show you the above to give you an idea of what 
``galah-python`` does when you provide it a string.

There is a third argument of ``atlas_counts``, ``atlas_occurrences``, ``atlas_species`` or ``atlas_media`` 
called ``simplify_polygon``, which defaults to ``False``. By setting the ``simplify_polygon`` argument 
to ``True``, the provided ``POLYGON`` or ``MULTIPOLYGON`` will be converted into the smallest bounding box 
(rectangle) that contains the ``POLYGON``. In this case, records will be included that may not exactly lie 
inside the provided shape.

.. prompt:: python

    >>> species_king_george_square = galah.atlas_occurrences(
    ...   polygon=king_george_sq,
    ...   simplify_polygon=True,
    ...   fields=["decimalLatitude", "decimalLongitude", "eventDate", "scientificName", "vernacularName"]  
    ... )
    >>> species_king_george_square.head(10)

.. program-output:: python3 -c "import galah;import shapely.wkt;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);king_george_square = shapely.wkt.loads(\"MULTIPOLYGON(((153.0243 -27.46886, 153.0242 -27.46896, 153.0236 -27.46837, 153.0239 -27.46814, 153.0239 -27.46813, 153.0242 -27.46789, 153.0244 -27.46805, 153.0245 -27.46821, 153.0246 -27.46828, 153.0247 -27.46835, 153.0248 -27.46848, 153.0246 -27.4686, 153.0246 -27.46862, 153.0245 -27.46871, 153.0243 -27.46886)))\");species_king_george_square = galah.atlas_occurrences(polygon=king_george_square,simplify_polygon=True,fields=[\"decimalLatitude\", \"decimalLongitude\", \"eventDate\", \"scientificName\", \"vernacularName\"]);print(species_king_george_square.head(10))"

Large shapefiles
----------------

The ``simplify_polygon`` argument with option ``polygon`` is provided because objects with a large amount of 
vertices will take a long time to filter on the ALA's end. In the event you have a large shapefile, using 
``simplify_polygon=True`` will at least enable an initial reduction of the time it takes for the data to be 
downloaded, before finer filtering to the actual shapefile will obtain the desired set of occurrences. 

Alternatively, one can also perform the "bbox" reduction before passing the shape to ``atlas_counts``, 
``atlas_occurrences``, ``atlas_species`` or ``atlas_media`` by using ``{geopandas}`` and the ``unary_union`` 
function of the ``{shapely}`` package.

A common situation for this to occur is when a shapefile with multiple shapes is provided, where we are 
interested in grouping our results by each shape. Here is a mock workflow using a subset of `a shapefile of 
all 2,184 Brisbane parks <https://www.data.brisbane.qld.gov.au/data/dataset/park-locations>`_.

Let’s say we are interested in knowing which parks in the Brisbane postcode 4075 have the most occurrences 
of the Scaly-Breasted Lorikeet, Trichoglossus chlorolepidotus, since 2020. We can download the entire 
shapefile from the above link, and perform our filtering and summarising as follows:

.. prompt:: python

    >>> # first, get all parts within the Brisbane postcode 4075
    >>> import geopandas as gpd
    >>> parks = gpd.read_file("Park___Locations.shp") 
    >>> parks.columns
    >>> brisbane_parks = parks[parks["POST_CODE"] == '4075']
    >>> brisbane_parks.head(10)

.. program-output:: python galah_user_guide/lorikeet_Brisbane_script.py First

.. prompt:: python

    >>> # second, get a shape of all the Brisbane parks and draw a bounding box around it
    >>> import shapely
    >>> from shapely.ops import unary_union
    >>> brisbane_parks_all = gpd.GeoSeries(unary_union(brisbane_parks["geometry"]))
    >>> brisbane_parks_bbox = brisbane_parks_all.bounds

.. program-output:: python galah_user_guide/lorikeet_Brisbane_script.py Second

To visualise 

.. prompt:: python

    >>> plot_brisbane_parks_bbox = shapely.box(xmin=brisbane_parks_bbox["minx"][0],
    ...                                xmax=brisbane_parks_bbox["maxx"][0],
    ...                                ymin=brisbane_parks_bbox["miny"][0],
    ...                                ymax=brisbane_parks_bbox["maxy"][0]
    ...                                )
    >>> brisbane_parks_all.plot(edgecolor = "#5A5A5A", linewidth = 1, facecolor = "white", figsize = (7,10))
    >>> plt.plot(*plot_brisbane_parks_bbox.exterior.xy,color="red")
    >>> plt.ylabel("Latitude",size=16,x=.45,y=0.5)
    >>> plt.xlabel("Longitude",size=16)

.. image:: brisbane_parks_and_bbox.png
    :scale: 30%

.. prompt:: python

    >>> # third, find all occurrences of Trichoglossus chlorolepidotus in the bounding box in 2022
    >>> import galah
    >>> galah.galah_config(email="your-email-here")
    >>> lorikeet_brisbane = galah.atlas_occurrences(
    ...     taxa="Trichoglossus chlorolepidotus",
    ...     filters="year=2022",
    ...     bbox=brisbane_parks_bbox
    ... )
    >>> lorikeet_brisbane

.. program-output:: python galah_user_guide/lorikeet_Brisbane_script.py Third

.. prompt:: python

    >>> brisbane_parks_all.plot(edgecolor = "#5A5A5A", linewidth = 1, facecolor = "white", figsize = (7,10))
    >>> plt.plot(*plot_brisbane_parks_bbox.exterior.xy,color="red")
    >>> plt.ylabel("Latitude",size=16,x=.45,y=0.5)
    >>> plt.xlabel("Longitude",size=16)
    >>> plt.scatter(lorikeet_brisbane["decimalLongitude"],lorikeet_brisbane["decimalLatitude"],alpha=0.5,color="orange",label="Lorikeet occurrences")
    >>> plt.legend(loc=(0.5,0.96))

.. image:: lorikeets_on_map_shapefile.png
    :scale: 30%


.. prompt:: python

    >>> # Filter records down to only those in the shapefile polygons
    >>> brisbane_parks["count"] = pd.Series([0 for i in range(len(brisbane_parks))])
    >>> for i,park in brisbane_parks.iterrows():
    ...     points = [(x,y) for x,y in zip(lorikeet_brisbane["decimalLongitude"], lorikeet_brisbane["decimalLatitude"]) if shapely.contains_xy(park["geometry"],x,y)]
    ...     brisbane_parks.at[i,"count"] = len(points)
    >>> brisbane_parks_counts = brisbane_parks[["PARK_NAME","count"]].sort_values("count",ascending=False).reset_index(drop=True)
    >>> brisbane_parks_counts.head(10)

.. program-output:: python galah_user_guide/lorikeet_Brisbane_script.py Fourth

Some shapefiles cover large geographic areas with the caveat that even the bounding box doesn’t restrict the 
number of records to a value that can be downloaded easily. In this case, we recommend more nuances and detailed
methods that can be performed using looping techniques. One of our ALA Labs blog posts, Hex maps for species 
occurrence data, has been written detailing how to approach larger problems such as this.