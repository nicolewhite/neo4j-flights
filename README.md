flight_graph
=============

A Neo4j graph database of flight data.

## Create the DB

Data is located [here](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time). Select the pre-zipped checkbox and download. Unzip the file. Make sure you're pointing to the correct file name at line 8 of `import.py`.

Also download the lookup tables for `UniqueCarrier` and `OriginAirportID`. Save these as `.csv`, not `.csv-`.

```
python schema.py
python import.py
python import_lookups.py
```

## Download the DB

Alternatively, download the zip file [here]()https://dl.dropboxusercontent.com/u/94782892/graph.db.zip.

## Model

<a href="https://dl.dropboxusercontent.com/u/94782892/flight_diagram.svg" target="_blank"><img src="https://dl.dropboxusercontent.com/u/94782892/flight_diagram.svg" width="100%" height="100%"></a>