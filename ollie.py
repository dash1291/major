#!/usr/bin/env python
import subprocess
import sys

from py2neo import neo4j


def parse_output(out):
    sents = out.split('\n\n')
    pairs = []

    for sent in sents:
        extractions = sent.split('\n')[1:]

        for extraction in extractions:
            part = extraction.split(':')[1].strip()[1:-1].split(';')
            part = map(lambda x: x.strip(), part)
            pairs.append(part)

    return pairs


def process_file(filename):
    cmd = 'java -Xmx512m -jar ollie-app-latest.jar --split %s -o out.txt' % (
        filename)
    subprocess.call(cmd.split(' '))
    pairs = parse_output(open('out.txt').read())

    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data/')
    concepts = graph_db.get_or_create_index(neo4j.Node, 'concepts')

    for p in pairs:
        n1 = concepts.get_or_create('concept_name', p[0], {'name': p[0]})
        n2 = concepts.get_or_create('concept_name', p[2], {'name': p[2]})
        graph_db.create((n1, p[1], n2))


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print 'No file specified.'
    else:
        filename = sys.argv[1]
        process_file(filename)
