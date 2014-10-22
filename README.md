flight_graph
=============

A Neo4j graph database of flight data.

## Create the DB

Data is located [here](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time). Select the pre-zipped checkbox and download. Unzip the file. Make sure you're pointing to the correct file name at line 8 of `import.py`.

Also download the lookup tables for `UniqueCarrier` and `OriginAirportID`. Save these as `.csv`, not `.csv-`. They should be called `L_UNIQUE_CARRIERS.csv` and `L_AIRPORT_ID.csv`.

```
python schema.py
python import.py
python import_lookups.py
```

## Download the DB

Alternatively, download the zip file [here](https://www.dropbox.com/s/qq1ll7nwjmtt29j/flights.db.zip?dl=0).

## Query

Watch Intro to Cypher with this dataset [here](https://www.youtube.com/watch?v=VdivJqlPzCI). Queries are located in `queries`.
