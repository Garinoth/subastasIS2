from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from subastas.forms import UserForm, AuctionUserForm, ItemForm, AuctionForm, OfferForm, BidForm


def index(request):
    return render(request, 'subastas/index.html')


class ListUsersView(ListView):

    model = User
    template_name = 'subastas/user_list_dummy.html'


@login_required
def test(request):
    context = {}
    return HttpResponse('ALGOOOOOOOOO')
    # return render(request, 'subastas/index.html', context)


def register_user(request):
    # TODO Send emails
    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='user')
        auction_user_form = AuctionUserForm(request.POST, prefix='auction_user')

        if user_form.is_valid() and auction_user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            auction_user = auction_user_form.save(commit=False)
            auction_user.user = user
            auction_user.save()

            return HttpResponseRedirect(reverse('index'))

    else:
        user_form = UserForm(prefix='user')
        auction_user_form = AuctionUserForm(prefix='auction_user')

    return render(request, 'subastas/register.html', {
        'user_form': user_form,
        'auction_user_form': auction_user_form})


@login_required
def item_detail(request, auction_id):
    # TODO
    pass


@login_required
@permission_required('subastas.can_create_item', raise_exception=True)
def item_create(request):
    # TODO
    pass
