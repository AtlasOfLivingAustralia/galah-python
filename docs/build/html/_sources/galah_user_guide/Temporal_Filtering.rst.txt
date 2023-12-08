.. _Temporal Filtering:

Temporal filtering
==================

Adapted from `the Temporal Filtering galah-R article <galah.ala.org.au/R/articles/temporal_filtering.html>`_.

*Callum Waite, Shandiya Balasubramaniam, Amanda Buyan*

Queries to the ALA will almost always require some form of temporal filtering. It is important 
to know how these types of data are stored in the ALA and how we can query them to obtain desired 
filters.

The ALA database possesses numerous date and time fields that relate to each observation. Here we 
provide descriptions of each of these fields and how they are best used to obtain specific queries. 
Ultimately, there are two ways users can filter temporal queries:

- filter using pre-existing/defined parameters, such as specific years or months
- filter within a bespoke date and/or time range

All temporal filtering is conducted using the ``filters`` argument in ``atlas_counts()``, 
``atlas_media()``, ``atlas_occurrences()`` and ``atlas_species()``. All temporal fields described 
below can be queried for exact matches (``==``), greater/less than (``>``, ``<``) or greater/less than or 
equal to (``<=``, ``>=``). Queries for multiple fields or multiple queries of the same field can be 
combined in the one ``filters`` call in order to obtain filters on time windows.

Year, Month and Day
--------------------

The ALA contains in-built year, month and day fields for every record. These are queried as 
numeric fields (i.e. July = 7) and can be used for quick data exploration and filtering. When 
the date limits of a desired query can be easily defined by year, month and/or day deliminations, 
these fields are most useful.

We can, for instance, use the year and month fields to group the 2022 amphibian records in the 
ALA by month (noting that months are labelled by a number).

.. prompt:: python

    >>> import galah
    >>> galah.atlas_counts(
    ...     taxa="Amphibia",
    ...     filters="year=2021",
    ...     group_by="month",
    ...     expand=False
    ... )

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts(taxa='Amphibia',filters='year=2021',group_by='month',expand=False))"

It is also important to observe that the outputted month column is of type character even though 
the values are numeric. This is the case for each of the year, month and day fields. However, 
they can be queried as either numeric or character values within ``filters``.

The other important fact about these fields when queried in ``filters`` is their independence; 
they cannot be used to query complex windows between two dates because the day and month filters 
are applied universally.

For instance, consider the native perennial Australian wildflower Chamaescilla corymbosa, whose 
known growth and flowering times are from August–October. We might be interested in the number 
of records for this species in the first week of spring (i.e. September) in each of the last 10 
years. The following query does not provide all results between 1/9/2013 and 7/9/2023. Rather, 
it will only return results that fall within all 3 windows at once.

.. prompt:: python

    >>> galah.atlas_counts(
    ...     taxa="Chamaescilla corymbosa",
    ...     filters=[
    ...         "year>=2013",
    ...         "year<=2023",
    ...         "month=9",
    ...         "day>=1",
    ...         "day<=7"
    ...     ],
    ...     group_by="year",
    ...     expand=False
    ... )

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts(taxa='Chamaescilla corymbosa',filters=['year>=2013','year<=2023','month=9','day>=1','day<=7'],group_by='year',expand=False))"

Occurrence dates
--------------------

For a more bespoke way to query exact dates of records, users can use the eventDate field. This 
field contains the exact date and time information of records and enables specific time windows 
to be queried easily. The only caveat is that the time/date must be provided in a specific format 
to ``filters`` for the ALA query to work.

The required format of dates in eventDate is the ISO 8601 International Date Standard format. 
This requires dates and times to be of the form “YYYY-MM-DDTHH:MM:SSZ”. Note that the T in the 
middle should be the actual letter “T” to delimit the date and time components, while the “Z” 
officially denotes that the time should be queried as UTC (Greenwich Meridian) time. Timezones 
can be confusing at the best of times, however it is easiest to remember that all ALA records 
are recorded at the local time of their location, and all times are then treated as effectively 
being UTC times.

The upshot of this specific formatting is that, for instance, the time I am writing this paragraph, 
4:26pm on the 2nd of August 2023, would be represented as "2023-08-02T16:26:44Z" in the ALA, 
even though officially my timezone is "+0930".

Because ``eventDate`` specifies the time to seconds, it is recommended that greater or less than 
queries are used rather than exact matches. When used with ``filters``, we can easily identify 
how many records of the humpback whale (*Megaptera novaeangliae*) have occurred since the species 
was removed from the Australian threatened species list on 26/02/2022.

.. prompt:: python

    >>> galah.atlas_counts(
    ...     taxa="Megaptera novaeangliae",
    ...     filters="eventDate>=2022-02-26T00:00:00Z"
    ... )

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts(taxa='Megaptera novaeangliae',filters=['eventDate>=2022-02-26T00:00:00Z']))"

It can be unintuitive to provide dates in this format. Luckily, it is straightforward to convert 
dates into the ISO 8601 International Date Standard format using the ``{datetime`` module:

.. prompt:: python

    >>> # convert the date September 22nd 2005 at 8:45pm to ISO 8601
    >>> # note the order is year,month,day,hours,minutes,seconds,milliseconds
    >>> import datetime
    >>> datetime.datetime(2005,9,22,20,45).isoformat()

.. program-output:: python -c "import datetime;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);print(datetime.datetime(2005,9,22,20,45).isoformat())"

After sending a query, any outputted eventDate values returned by a galah query will be of date 
class "POSIXct".

Upload dates
-----------------
The other important date field present in the ALA pertains to the date that the record was 
provided to the ALA. This field is called ``firstLoadedDate`` and is formatted in exactly the same 
manner as ``eventDate``.

Different data providers provide batches of records to the ALA at different intervals. 
iNaturalist Australia provide weekly uploads of data, while eBird provides yearly uploads. 
``firstLoadedDate`` can be especially useful for finding new records to the ALA that have been 
provided since you last checked. For instance, we can use it to see how many observations of 
Sulphur-Crested Cockatoos recorded in the first week of 2023 were actually loaded into the 
ALA by the following week:

.. prompt:: python

    >>> # Total records of Cactua galerita in Jan1-7
    >>> galah.atlas_counts(
    ...     taxa="Cacatua galerita",
    ...     filters=[
    ...         "eventDate>=2023-01-07T00:00:00Z",
    ...         "eventDate<2023-01-08T00:00:00Z"
    ...     ]
    ... )

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts(taxa='Cacatua galerita',filters=['eventDate>=2023-01-07T00:00:00Z','eventDate<2023-01-08T00:00:00Z']))"

.. prompt:: python

    >>> # Records of Cactua galerita uploaded in Jan 1-14
    >>> galah.atlas_counts(
    ...     taxa="Cacatua galerita",
    ...     filters=[
    ...         "eventDate>=2023-01-07T00:00:00Z",
    ...         "eventDate<2023-01-08T00:00:00Z",
    ...         "firstLoadedDate<2023-01-15T00:00:00Z"
    ...     ]
    ... )

.. program-output:: python -c "import galah;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);galah.galah_config(atlas=\"Australia\");print(galah.atlas_counts(taxa='Cacatua galerita',filters=['eventDate>=2023-01-07T00:00:00Z','eventDate<2023-01-08T00:00:00Z','firstLoadedDate<2023-01-15T00:00:00Z']))"

Note that no lower bound is required for ``firstLoadedDate`` because ``eventDate`` imposes that by proxy 
(records can’t be uploaded before they’ve occurred).