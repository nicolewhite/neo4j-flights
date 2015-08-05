from csv_things import import_csv_to_dict
from py2neo import authenticate, Graph
from batch_upload import batch_upload

authenticate("localhost:7474", "neo4j", "neo4j")
graph = Graph()

data = import_csv_to_dict('On_Time_On_Time_Performance_2014_1.csv', headers = True)

query = """
MERGE (oAirport:Airport {id: TOINT({OriginAirportID}) })
SET oAirport.abbr = UPPER({Origin})

MERGE (oCity:City {name: UPPER({OriginCityName}) })
MERGE (oState:State {abbr: UPPER({OriginState}), name: UPPER({OriginStateName}) })

MERGE (oCity)-[:IN_STATE]->(oState)
MERGE (oAirport)-[:IN_CITY]->(oCity)
MERGE (oAirport)-[:IN_STATE]->(oState)

MERGE (dAirport:Airport {id: TOINT({DestAirportID}) })
SET dAirport.abbr = UPPER({Dest})

MERGE (dCity:City {name: UPPER({DestCityName}) })
MERGE (dState:State {abbr: UPPER({DestState}), name: UPPER({DestStateName}) })

MERGE (dCity)-[:IN_STATE]->(dState)
MERGE (dAirport)-[:IN_CITY]->(dCity)
MERGE (dAirport)-[:IN_STATE]->(dState)

CREATE (f:Flight {flight_num: TOINT({FlightNum}) }),
       (f)-[:ORIGIN {taxi_time: TOINT({TaxiOut}), dep_delay: TOINT({DepDelay}) }]->(oAirport),
	   (f)-[:DESTINATION {taxi_time: TOINT({TaxiIn}), arr_delay: TOINT({ArrDelay}) }]->(dAirport)

SET f.year = TOINT({Year}),
    f.month = TOINT({Month}),
    f.day = TOINT({DayofMonth}),
    f.weekday = TOINT({DayOfWeek})

FOREACH (a IN (CASE {TailNum} WHEN "" THEN [] ELSE [{TailNum}] END) |
    MERGE (craft:Aircraft {tail_num:a})
    MERGE (f)-[:AIRCRAFT]->(craft)
)

FOREACH (c IN (CASE {AirlineID} WHEN "" THEN [] ELSE [TOINT({AirlineID})] END) |
    MERGE (car:Carrier {id:c, abbr: UPPER({UniqueCarrier}) })
    MERGE (f)-[:CARRIER]->(car)
)

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
    MERGE (f)-[d:DIVERTED_TO]->(a)
    SET d.step = 1
)

FOREACH (div IN (CASE {Div2AirportID} WHEN "" THEN [] ELSE [TOINT({Div2AirportID})] END) |
    MERGE (a:Airport {id:div})
    MERGE (f)-[d:DIVERTED_TO]->(a)
    SET d.step = 2
)

FOREACH (div IN (CASE {Div3AirportID} WHEN "" THEN [] ELSE [TOINT({Div3AirportID})] END) |
    MERGE (a:Airport {id:div})
    MERGE (f)-[d:DIVERTED_TO]->(a)
    SET d.step = 3
)

FOREACH (div IN (CASE {Div4AirportID} WHEN "" THEN [] ELSE [TOINT({Div4AirportID})] END) |
    MERGE (a:Airport {id:div})
    MERGE (f)-[d:DIVERTED_TO]->(a)
    SET d.step = 4
)

FOREACH (div IN (CASE {Div5AirportID} WHEN "" THEN [] ELSE [TOINT({Div5AirportID})] END) |
    MERGE (a:Airport {id:div})
    MERGE (f)-[d:DIVERTED_TO]->(a)
    SET d.step = 5
);
"""

batch_upload(graph, data, query)
