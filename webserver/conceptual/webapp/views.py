import json
import StringIO

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from py2neo import neo4j

from conceptual.utils import ExtractorClient


def home(request):
    return render(request, 'landing.html')


def play(request):
    if request.method == 'POST':
        f = request.FILES['file']

        fp = StringIO.StringIO()

        for chunk in f.chunks():
            fp.write(chunk)
        fp.seek(0)

        extractions = ExtractorClient().extract(fp.read())
        return HttpResponse(json.dumps(extractions))

    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'new.html', c)


def visualize_page(request):
    page_url = request.GET.get('page')
    return render(request, 'visualize.html', {'page_url': page_url})


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


def signup(request):
    if request.method == 'POST':
        # TODO:: Do some typical checks and show errors if found
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(email, email, password)
        login(request, authenticate(username=email, password=password))
        return redirect('/dashboard')
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'signup.html', c)


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        uname = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=uname, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'signin.html', c)


@csrf_exempt
def signout(request):
    logout(request)
    return redirect('/signin')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
