from csv_things import import_csv_to_dict
from py2neo import authenticate, Graph
from batch_upload import batch_upload

authenticate("localhost:7474", "neo4j", "neo4j")
graph = Graph()

data = import_csv_to_dict('L_UNIQUE_CARRIERS.csv', headers = True)

query = """
MATCH (c:Carrier {abbr:UPPER({Code})})
SET c.name = UPPER({Description})
"""

batch_upload(graph, data, query)

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
MATCH (a:Airport {id:TOINT({Code})})
SET a.name = UPPER({Description})
"""

batch_upload(graph, data, query)
