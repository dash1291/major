import json
import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from flask import Flask, render_template, request
from py2neo import neo4j

from ollie import pipeline

app = Flask(__name__)


"""@app.route('/render', method=['POST'])
def render():
    pairs = json.loads(request.form['data'])
    edges = []
    for pair in pairs:
        n1 = pair[0]
        n2 = pair[2]
        rel = pair[1]

        edges.append({'source': str(n1), 'target': str(n2), 'type': str(rel)})

    return render_template('index4.html', links=edges)
"""

@app.route('/graph', methods=['POST', 'GET'])
def graph():
    if request.method == 'POST':
        f = request.files['file']
        f.save('/tmp/doc.txt')
        pairs = pipeline('/tmp/doc.txt')

        edges = []
        for pair in pairs:
            n1 = pair[0]
            n2 = pair[2]
            rel = pair[1]

            edges.append({'source': str(n1), 'target': str(n2), 'type': str(rel)})

        #return render_template('graph.html', links=edges)
        return json.dumps(edges)

    else:
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


@app.route('/search/<query>')
def search(query):
    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')
    concepts = graph_db.get_index(neo4j.Node, 'concepts')
    query = '*' + '*'.join(query.strip().split(' ')) + '*'
    print query
    q = concepts.query('concept_name:%s' % str(query))

    pairs = []
    try:
        concept = q.next()
    except:
        return json.dumps(pairs)

    rels = concept.match()

    for rel in rels:
        pairs.append([rel.start_node['name'], rel.type, rel.end_node['name']])

    return json.dumps(pairs)


@app.route('/graphical/<concepts>')
def graphical(concepts):
    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')
    relations = graph_db.get_index(neo4j.Node, 'concepts')
    query =  '"' + '" OR "'.join(concepts.split(',')) + '"'
    q = relations.query('concept_name:(%s)' % str(query))

    pairs = []
    rels = []

    concept = None
    while True:
        try:
            concept = q.next()
        except:
            break

        rels += concept.match()

    if not concept:
        return json.loads(pairs)

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
        #edges.append([str(n1), str(rel.type), {"length":50.00, "stroke":"rgba(135,234,135,1.00)"}])
        #edges.append([str(rel.type), str(n2), {"length":50.00, "stroke":"rgba(135,234,135,1.00)"}])
        edges.append({'source': str(n1), 'target': str(n2), 'type': str(rel.type)})

    return render_template('graph.html', links=edges, nodes=nodes)


@app.route('/')
def home():
    return render_template('new.html')


@app.route('/browse')
def browse():
    concepts = []
    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')
    relations = graph_db.get_index(neo4j.Node, 'concepts')
    q = relations.query('concept_name:*')

    while True:
        try:
            concept = q.next()
            concepts.append(str(concept['name']))
        except:
            break

    return render_template('browse.html', concepts=concepts)


app.debug = True
app.run()
