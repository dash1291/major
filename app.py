import json

from flask import Flask
from py2neo import neo4j


app = Flask(__name__)

@app.route('/graphs')
def graph():
    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')
    relations = graph_db.get_index(neo4j.Relationship, 'relations')
    q = relations.query('relation_name:*')

    pairs = []
    for rel in q:
        pairs.append([rel.start_node['name'], rel.type, rel.end_node['name']])

    return json.dumps(pairs)

app.debug = True
app.run()
