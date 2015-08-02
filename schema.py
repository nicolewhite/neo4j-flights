from py2neo import Graph

graph = Graph()

graph.cypher.execute("CREATE CONSTRAINT ON (a:Airport) ASSERT a.id IS UNIQUE;")
graph.cypher.execute("CREATE CONSTRAINT ON (s:State) ASSERT s.name IS UNIQUE;")
graph.cypher.execute("CREATE CONSTRAINT ON (s:State) ASSERT s.abbr IS UNIQUE;")
graph.cypher.execute("CREATE CONSTRAINT ON (c:City) ASSERT c.name IS UNIQUE;")
graph.cypher.execute("CREATE CONSTRAINT ON (a:Aircraft) ASSERT a.tail_num IS UNIQUE;")
graph.cypher.execute("CREATE CONSTRAINT ON (c:Carrier) ASSERT c.id IS UNIQUE;")
graph.cypher.execute("CREATE CONSTRAINT ON (r:Reason) ASSERT r.name IS UNIQUE;")
graph.cypher.execute("CREATE INDEX ON :Flight(flight_num);")
graph.cypher.execute("CREATE INDEX ON :Airport(abbr);")
graph.cypher.execute("CREATE INDEX ON :Carrier(abbr);")
