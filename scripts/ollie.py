#!/usr/bin/env python
import sys

from py2neo import neo4j
import zmq


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:8080")


def parse_output(out):
    extractions = out.strip().split("\n")
    pairs = []

    for extraction in extractions:
        pairs.append(extraction[1:-1].split(";"))

    return pairs


def add_to_database(pairs):
    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')
    concepts = graph_db.get_or_create_index(neo4j.Node, 'concepts')
    relations = graph_db.get_or_create_index(neo4j.Relationship, 'relations')

    for p in pairs:
        n1 = concepts.get_or_create('concept_name', p[0], {'name': p[0]})
        n2 = concepts.get_or_create('concept_name', p[2], {'name': p[2]})

        rel_tup = (n1, p[1], n2)
        relations.get_or_create('relation_name', '%s %s %s' % rel_tup, rel_tup)


def send_extractor_request(text):
    socket.send(text)
    return socket.recv()


def pipeline(filename):
    print 'Resolving coreferences'
    res = send_extractor_request(open(filename).read())
    return parse_output(res)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'No file specified.'
    else:
        pipeline(sys.argv[1])
