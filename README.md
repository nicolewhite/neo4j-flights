flight_graph
=============

A Neo4j graph database of flight data.

## Create the DB

Data is located [here](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time). Select the pre-zipped checkbox and download. Unzip the file. Make sure you're pointing to the correct file name at line 8 of `import.py`.

Also download the lookup tables for `UniqueCarrier` and `OriginAirportID`. Save these as `.csv`, not `.csv-`. They should be called `L_UNIQUE_CARRIERS.csv` and `L_AIRPORT_ID.csv`.

```
 python import_all.py --neo4j_username=neo4j --neo4j_password=<password-here>
```

## Setup

To run the scripts above, you will need to install the following python packages if you don't have them installed already.

### Option 1: virtualenv

```
$ virtualenv --system-site-packages env-test
$ source env-test/bin/activate
(env-test) $ pip install -r requirements.txt
```

### Option 2: pip install

```
pip install py2neo
pip install unicodecsv
```

## Query

Watch Intro to Cypher with this dataset [here](https://www.youtube.com/watch?v=VdivJqlPzCI). Queries are located in `queries`.
