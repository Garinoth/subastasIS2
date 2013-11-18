from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
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

def login_view(request):
    #TODO
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.


def logout_view(request):
    #TODO
    logout(request)
    # Redirect to succes page


@login_required
def auction_detail(request, auction_id):
    #TODO
    pass

@login_required
@permission_required('subastas.can_create_item', raise_exception=True)
def create_item_view(request):
    #TODO
    pass
