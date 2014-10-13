from csv_things import import_csv_to_dict
from py2neo import neo4j
from batch_upload import batch_upload

# Download lookup tables for carriers and airports.

graph = neo4j.GraphDatabaseService("http://localhost:1491/db/data/")
batch = neo4j.WriteBatch(graph)

data = import_csv_to_dict('L_UNIQUE_CARRIERS.csv', headers = True)

query = """
MATCH (c:Carrier {abbr:{Code}})
SET c.name = UPPER({Description})
"""

batch_upload(batch, data, query)

# Manual things done in Excel: split on colon and TRIM() to only get airport name in Description column.
data = import_csv_to_dict('L_AIRPORT.csv', headers = True)

query = """
MATCH (a:Airport {abbr:{Code}})
SET a.name = UPPER({Description})
"""

batch_upload(batch, data, query)