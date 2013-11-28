#!/usr/bin/env python
import subprocess
import sys

from py2neo import neo4j

from stanford import get_corefs


def parse_output(out, corefs):
    sents = out.split('\n\n')
    pairs = []

    sent_ind = 1
    for sent in sents:
        extractions = sent.split('\n')[1:]

        for extraction in extractions:
            if extraction == 'No extractions found.':
                break

            part = extraction.split(':')[1].strip()[1:-1].split(';')
            part = map(lambda x: x.strip().lower(), part)

            skip = False

            if part[0].lower() == 'it':
                skip = True
                for coref in corefs:

                    if coref[2] == sent_ind and coref[0] == part[0]:
                        part[0] = coref[1]
                        skip = False
            else:
                for coref in corefs:

                    if coref[2] == sent_ind:
                        if coref[0] == part[0]:
                            part[0] = coref[1]

                        elif coref[0] == part[2]:
                            part[2] = coref[1]

            if not skip:
                pairs.append(part)

        sent_ind += 1

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


def process_file(filename):
    print 'Extracting relations'
    cmd = 'java -Xmx512m -jar ollie-app-latest.jar --split %s -o out.txt' % (
        filename)
    subprocess.call(cmd.split(' '))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'No file specified.'
    else:
        filename = sys.argv[1]
        print 'Resolving coreferences'
        corefs = get_corefs(filename)

        process_file(filename)
        pairs = parse_output(open('out.txt').read(), corefs)
        add_to_database(pairs)
