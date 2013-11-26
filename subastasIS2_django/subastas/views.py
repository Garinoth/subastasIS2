from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from subastas.forms import UserForm, AuctionUserForm, ItemForm, AuctionForm, OfferForm, BidForm, ActivationForm, ValidationError


class ListUsersView(ListView):

    model = User
    template_name = 'subastas/user_list_dummy.html'


def index(request):
    return render(request, 'subastas/index.html')


@login_required
def test(request):
    context = {}
    return HttpResponse('ALGOOOOOOOOO')
    # return render(request, 'subastas/index.html', context)


def register_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='user')
        auction_user_form = AuctionUserForm(
            request.POST, prefix='auction_user')

        if user_form.is_valid() and auction_user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_active = False
            user.save()

            auction_user = auction_user_form.save(commit=False)
            auction_user.user = user
            auction_user.set_activation_key()
            auction_user.save()
            auction_user.send_activation_email()

    else:
        user_form = UserForm(prefix='user')
        auction_user_form = AuctionUserForm(prefix='auction_user')

    return render(request, 'subastas/register.html', {
        'user_form': user_form,
        'auction_user_form': auction_user_form
        })


def tos(request):
    return render(request, 'subastas/tos.html')


def activation(request, activation_key):
    if request.method == 'POST':
        form = ActivationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user is not None:
                user.is_active = True
                user.save()
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))

    else:
        if activation_key:
            form = ActivationForm(initial={'activation_key': activation_key})

    return render(request, 'subastas/activation.html', {
        'form': form,
        })


@login_required
def item_detail(request, auction_id):
    # TODO
    pass


@login_required
@permission_required('subastas.can_create_item', raise_exception=True)
def item_create(request):
    # TODO
    pass
