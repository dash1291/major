import json

from flask import Flask, render_template
from py2neo import neo4j


app = Flask(__name__)

@app.route('/graph')
def graph():
    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')
    relations = graph_db.get_index(neo4j.Relationship, 'relations')
    q = relations.query('relation_name:*')

    pairs = []

    for rel in q:
        pairs.append([rel.start_node['name'], rel.type, rel.end_node['name']])

    return json.dumps(pairs)


@app.route('/graph/<concept>')
def concept(concept):
    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')
    relations = graph_db.get_index(neo4j.Node, 'concepts')
    q = relations.query('concept_name:%s' % concept)

    pairs = []
    try:
        concept = q.next()
    except:
        return json.dumps(pairs)

    rels = concept.match()

    for rel in rels:
        pairs.append([rel.start_node['name'], rel.type, rel.end_node['name']])

    return json.dumps(pairs)


@app.route('/graphical/<concept>')
def graphical(concept):
    print concept
    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')
    relations = graph_db.get_index(neo4j.Node, 'concepts')
    q = relations.query('concept_name:"%s"' % str(concept))

    pairs = []
    try:
        concept = q.next()
    except:
        return json.dumps(pairs)

    rels = concept.match()

    nodes = {}
    edges = []
    for rel in rels:
        n1 = rel.start_node['name']
        n2 = rel.end_node['name']

        if n1 not in nodes:
            nodes[str(n1)] = {"radius":10.0, "weight":1.00, "centrality":0.00, "fill":"rgba(0,127,255,0.70)", "stroke":"rgba(0,0,0,0.80)"}

        if n2 not in nodes:
            nodes[str(n2)] = {"radius":10.0, "weight":1.00, "centrality":0.00, "fill":"rgba(0,127,255,0.70)", "stroke":"rgba(0,0,0,0.80)"}


        nodes[str(rel.type)] = {"radius":10.0, "weight":1.00, "centrality":0.00, "fill":"rgba(0,127,255,0.70)", "stroke":"rgba(0,0,0,0.80)"}
        edges.append([str(n1), str(rel.type), {"length":50.00, "stroke":"rgba(135,234,135,1.00)"}])
        edges.append([str(rel.type), str(n2), {"length":50.00, "stroke":"rgba(135,234,135,1.00)"}])

    return render_template('index.html', edges=edges, nodes=nodes)


app.debug = True
app.run()
