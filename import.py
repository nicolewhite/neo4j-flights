from csv_things import import_csv_to_dict
from py2neo import neo4j
from batch_upload import batch_upload

graph = neo4j.GraphDatabaseService("http://localhost:1491/db/data/")
batch = neo4j.WriteBatch(graph)

# Only need to run once.
# neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (a:Airport) ASSERT a.id IS UNIQUE;").run()
# neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (s:State) ASSERT s.name IS UNIQUE;").run()
# neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (c:City) ASSERT c.name IS UNIQUE;").run()
# neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (a:Aircraft) ASSERT a.tail_num IS UNIQUE;").run()
# neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (c:Carrier) ASSERT c.id IS UNIQUE;").run()
# neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (r:Reason) ASSERT r.name IS UNIQUE;").run()


data = import_csv_to_dict('january.csv', headers = True)

query = """
MERGE (oAirport:Airport {id: TOINT({OriginAirportID}) })
SET oAirport.abbr = UPPER({Origin})

MERGE (oCity:City {name: UPPER({OriginCityName}) })
MERGE (oState:State {abbr: UPPER({OriginState}), name: UPPER({OriginStateName}) })

MERGE (oCity)-[:IN_STATE]->(oState)
MERGE (oAirport)-[:IN_CITY]->(oCity)

MERGE (dAirport:Airport {id: TOINT({DestAirportID}) })
SET dAirport.abbr = UPPER({Dest})

MERGE (dCity:City {name: UPPER({DestCityName}) })
MERGE (dState:State {abbr: UPPER({DestState}), name: UPPER({DestStateName}) })

MERGE (dCity)-[:IN_STATE]->(dState)
MERGE (dAirport)-[:IN_CITY]->(dCity)

MERGE (a:Aircraft {tail_num: {TailNum} })
MERGE (c:Carrier {id: {AirlineID}, abbr: UPPER({UniqueCarrier}) })

CREATE (f:Flight {flight_num: TOINT({FlightNum}) }),
       (f)-[:ORIGIN {taxi_time: TOINT({TaxiOut}), dep_delay: TOINT({DepDelay}) }]->(oAirport),
	   (f)-[:DESTINATION {taxi_time: TOINT({TaxiIn}), arr_delay: TOINT({ArrDelay}) }]->(dAirport),
	   (f)-[:CARRIER]->(c),
	   (f)-[:AIRCRAFT]->(a)

SET f.year = TOINT({Year}),
    f.month = TOINT({Month}),
    f.day = TOINT({DayofMonth}),
    f.weekday = TOINT({DayOfWeek})

FOREACH (delay IN (CASE {CarrierDelay} WHEN "" THEN []
                                       WHEN "0.00" THEN []
						               ELSE [TOINT({CarrierDelay})]
						               END) |
	MERGE (r:Reason {name:'CARRIER'})
	MERGE (f)-[:DELAYED_BY {time: delay }]->(r)
)

FOREACH (delay IN (CASE {WeatherDelay} WHEN "" THEN []
                                       WHEN "0.00" THEN []
                                       ELSE [TOINT({WeatherDelay})]
                                       END) |
	MERGE (r:Reason {name:'WEATHER'})
	MERGE (f)-[:DELAYED_BY {time: delay }]->(r)
)

FOREACH (delay IN (CASE {NASDelay} WHEN "" THEN []
                                   WHEN "0.00" THEN []
                                   ELSE [TOINT({NASDelay})]
                                   END) |
	MERGE (r:Reason {name:'NATIONAL AIR SYSTEM'})
	MERGE (f)-[:DELAYED_BY {time: delay }]->(r)
)

FOREACH (delay IN (CASE {SecurityDelay} WHEN "" THEN []
                                        WHEN "0.00" THEN []
                                        ELSE [TOINT({SecurityDelay})]
                                        END) |
	MERGE (r:Reason {name:'SECURITY'})
	MERGE (f)-[:DELAYED_BY {time: delay }]->(r)
)

FOREACH (delay IN (CASE {LateAircraftDelay} WHEN "" THEN []
                                            WHEN "0.00" THEN []
						ELSE [TOINT({LateAircraftDelay})]
						END) |
	MERGE (r:Reason {name:'LATE AIRCRAFT'})
	MERGE (f)-[:DELAYED_BY {time: delay }]->(r)
)

FOREACH (cancellation IN (CASE {CancellationCode} WHEN "A" THEN ["CARRIER"]
                                                  WHEN "B" THEN ["WEATHER"]
                                                  WHEN "C" THEN ["NATIONAL AIR SYSTEM"]
                                                  WHEN "D" THEN ["SECURITY"]
                                                  ELSE []
                                                  END) |
    MERGE (r:Reason {name:cancellation})
    MERGE (f)-[:CANCELLED_BY]->(r)
)

FOREACH (div IN (CASE {Div1AirportID} WHEN "" THEN [] ELSE [TOINT({Div1AirportID})] END) |
    MERGE (a:Airport {id:div})
    MERGE (f)-[:DIVERTED_TO]->(a)
)

FOREACH (div IN (CASE {Div2AirportID} WHEN "" THEN [] ELSE [TOINT({Div2AirportID})] END) |
    MERGE (a:Airport {id:div})
    MERGE (f)-[:DIVERTED_TO]->(a)
)

FOREACH (div IN (CASE {Div3AirportID} WHEN "" THEN [] ELSE [TOINT({Div3AirportID})] END) |
    MERGE (a:Airport {id:div})
    MERGE (f)-[:DIVERTED_TO]->(a)
)

FOREACH (div IN (CASE {Div4AirportID} WHEN "" THEN [] ELSE [TOINT({Div4AirportID})] END) |
    MERGE (a:Airport {id:div})
    MERGE (f)-[:DIVERTED_TO]->(a)
)

FOREACH (div IN (CASE {Div5AirportID} WHEN "" THEN [] ELSE [TOINT({Div5AirportID})] END) |
    MERGE (a:Airport {id:div})
    MERGE (f)-[:DIVERTED_TO]->(a)
);
"""

batch_upload(batch, data, query)

