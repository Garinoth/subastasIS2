from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'subastas/index.html')


@login_required
def test(request):
    context = {}
    return HttpResponse('ALGOOOOOOOOO')
    # return render(request, 'subastas/index.html', context)


def register(request):
    # TODO Send emails
    user = User.objects.create_user(
        'john', 'lennon@thebeatles.com', 'johnpassword')
    user.last_name = 'Lennon'
    user.save()


@login_required
def item_detail(request, auction_id):
    # TODO
    pass


@login_required
@permission_required('subastas.can_create_item', raise_exception=True)
def item_create(request):
    # TODO
    pass
