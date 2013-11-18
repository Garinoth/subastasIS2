from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    pass


def test(request):
    context = {}
    return render(request, 'subastas/index.html', context)


def create_user(request):
    #TODO
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.last_name = 'Lennon'
    user.save()

def login(request):
    #TODO
