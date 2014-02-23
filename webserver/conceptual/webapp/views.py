from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from py2neo import neo4j


def home(request):
    return render(request, 'landing.html')


def play(request):
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


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # TODO:: Do some typical checks and show errors if found
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(email, email, password)
        login(request, authenticate(username=email, password=password))
        return redirect('/dashboard')
    else:
        return render(request, 'signup.html')


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
        return render(request, 'signin.html')


@csrf_exempt
def signout(request):
    logout(request)
    return redirect('/signin')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
