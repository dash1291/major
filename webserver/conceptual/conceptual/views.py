from django.shortcuts import render

from py2neo import neo4j


def home(request):
    return render(request, 'new.html')


def browse(request):
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

    return render(request, 'browse.html', {'concepts': concepts})


def dashboard(request):
    return render(request, 'dashboard.html')
