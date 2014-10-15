from csv_things import import_csv_to_dict
from py2neo import neo4j
from batch_upload import batch_upload

graph = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
batch = neo4j.WriteBatch(graph)

data = import_csv_to_dict('L_UNIQUE_CARRIERS.csv', headers = True)

query = """
MATCH (c:Carrier {abbr:UPPER({Code})})
SET c.name = UPPER({Description})
"""

batch_upload(batch, data, query)

data = import_csv_to_dict('L_AIRPORT_ID.csv', headers = True)

# Split on colon to get only the airport name.
for d in data:
    text = d['Description']
    text = text.split(":")

    if(len(text) == 2):
        city, airport = text
    else:
        airport = text[0]

    airport = airport.strip()
    d['Description'] = airport

query = """
MATCH (a:Airport {id:TOINT{Code})})
SET a.name = UPPER({Description})
"""

batch_upload(batch, data, query)