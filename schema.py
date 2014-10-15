from py2neo import neo4j

graph = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (a:Airport) ASSERT a.id IS UNIQUE;").run()
neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (s:State) ASSERT s.name IS UNIQUE;").run()
neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (c:City) ASSERT c.name IS UNIQUE;").run()
neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (a:Aircraft) ASSERT a.tail_num IS UNIQUE;").run()
neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (c:Carrier) ASSERT c.id IS UNIQUE;").run()
neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (r:Reason) ASSERT r.name IS UNIQUE;").run()
neo4j.CypherQuery(graph, "CREATE INDEX ON :Flight(flight_num);").run()
neo4j.CypherQuery(graph, "CREATE INDEX ON :Airport(abbr);").run()
neo4j.CypherQuery(graph, "CREATE INDEX ON :Carrier(abbr);").run()