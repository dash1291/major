from py2neo import neo4j

graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')

graph_db.clear()
