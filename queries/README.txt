Queries were ran within the DBPedia SPARQL endpoint found here: https://dbpedia.org/sparql

Due a pre-set limit on the number of rows that can be returned in a single SPARQL query (10000), it was necessary to add the OFFSET parameter for each query, and then run the query at intervals of 10000 offsets in order to get the full set of data for each platform.

In addition to this 10000 limit on the number of rows to be returned, there was a maximum limit on the number of rows that could be searched through, which was 40000. In order to get around this, for platforms that have more than 40000 facts associated with them, we incorporate a filter that will filter in and out games that tend to have a large number of rows associated with them. This typically includes games with episodic content where each of the episodes and its data gets associated with the same base game. This results in two queries that finds games and properties for a small set of games, as well as this set's complement.

If there are still too much data for us to query, then a date range was used to query for games within specific date ranges (or with no dates at all). This was the case for the PC games.

These schemes allows us to side-step the 40000 row limit on this SPARQL endpoint.