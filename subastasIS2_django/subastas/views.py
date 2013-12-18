from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.utils import timezone, simplejson as json

from subastas.forms import UserForm, AuctionUserForm, ItemForm, AuctionForm, OfferForm, BidForm, ActivationForm, SaleForm
from subastas.models import Auction, Offer, AuctionUser, Item, Bid

from django_simple_search.utils import generic_search


class ListUsersView(ListView):

    model = User
    template_name = 'subastas/user_list_dummy.html'


class ListAuctionsView(ListView):

    model = Auction
    queryset = Auction.objects.order_by('end_date')
    context_object_name = 'auction_list'
    template_name = 'subastas/auctions.html'


class ListOffersView(ListView):

    model = Offer
    queryset = Offer.objects.order_by('end_date')
    context_object_name = 'offer_list'
    template_name = 'subastas/offers.html'


def index(request):
    return render(request, 'subastas/index.html')


def help(request):
    return render(request, 'subastas/help.html')


def success(request):
    return render(request, 'subastas/sale_successful.html')


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
            valid = 'true'
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_active = False
            user.save()

            auction_user = auction_user_form.save(commit=False)
            auction_user.user = user
            auction_user.set_activation_key()
            auction_user.send_activation_email()
            auction_user.save()
        else:
            valid = 'false'

    else:
        user_form = UserForm(prefix='user')
        auction_user_form = AuctionUserForm(prefix='auction_user')
        valid = 'false'

    ctx = {
        'user_form': user_form,
        'auction_user_form': auction_user_form,
        'valid': valid,
    }

    return render(request, 'subastas/register.html', ctx)


def tos(request):
    return render(request, 'subastas/tos.html')


def activation(request, activation_key):
    if request.method == 'POST':
        form = ActivationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
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
@permission_required('subastas.can_create_item', raise_exception=True)
def create_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST, request.FILES, prefix='item')
        auction_form = AuctionForm(request.POST, prefix='auction')
        offer_form = OfferForm(request.POST, prefix='offer')
        item_type = request.POST['item_type']

        if item_type:
            if item_type == 'auction':
                if item_form.is_valid() and auction_form.is_valid():
                    item = item_form.save(commit=False)
                    item.owner = AuctionUser.objects.get(user=request.user)
                    item.save()

                    auction = auction_form.save(commit=False)
                    auction.item = item
                    auction.winner = item.owner
                    auction.save()

                    return HttpResponseRedirect(reverse('auctions'))

            if item_type == 'offer':
                if item_form.is_valid() and offer_form.is_valid():
                    item = item_form.save(commit=False)
                    item.owner = AuctionUser.objects.get(user=request.user)
                    item.save()

                    offer = offer_form.save(commit=False)
                    offer.item = item
                    # DELETE THIS WHEN MODELS ARE UPDATED TO ACCEPT NULL VALUE
                    offer.winner = item.owner
                    offer.save()

                    return HttpResponseRedirect(reverse('offers'))

    else:
        item_form = ItemForm(prefix='item')
        auction_form = AuctionForm(prefix='auction')
        offer_form = OfferForm(prefix='offer')
        item_type = None

    ctx = {
        'item_form': item_form,
        'auction_form': auction_form,
        'offer_form': offer_form,
        'item_type': item_type,
    }

    return render(request, 'subastas/item.html', ctx)


@login_required
def auction(request, pk):
    auction = Auction.objects.get(pk=pk)
    recharge = False
    error = ''

    if request.method == 'POST':
        bid_form = BidForm(request.POST, user=request.user, auction=auction)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.auction = auction
            bid.user = AuctionUser.objects.get(user=request.user)
            bid.user.auction_points -= 1
            bid.user.offer_points += 1
            bid.user.save()
            bid.auction.winner = bid.user
            bid.auction.end_date += timedelta(minutes=1)
            bid.auction.save()
            bid.save()

            return HttpResponseRedirect(reverse('auction_detail', kwargs={'pk': pk}))

        else:
            errors = bid_form.errors.as_text()
            if 'recharge' in errors:
                recharge = True

            else:
                error = errors.split(' * ')[1]

    else:
        bid_form = BidForm()

    ctx = {
        'auction': auction,
        'bid_form': bid_form,
        'recharge': recharge,
        'error': error,
        'now': timezone.now(),
    }

    return render(request, 'subastas/auction_detail.html', ctx)


@login_required
def offer(request, pk):
    offer = Offer.objects.get(pk=pk)
    valid = False
    error = ''

    if request.method == 'POST':
        sale_form = SaleForm(request.POST, user=request.user, offer=offer)
        if sale_form.is_valid():
            valid = True
            confirm = request.POST.get('confirm')
            if confirm == 'True':
                auction_user = AuctionUser.objects.get(user=request.user)
                auction_user.offer_points -= offer.price
                auction_user.save()

                offer.winner = auction_user
                offer.sold = True
                offer.save()

                return HttpResponseRedirect(reverse('success'))

        else:
            error = sale_form.errors.as_text().split(' * ')[1]

    else:
        sale_form = SaleForm()

    ctx = {
        'offer': offer,
        'sale_form': sale_form,
        'valid': valid,
        'error': error,
        'now': timezone.now(),
    }

    return render(request, 'subastas/offer_detail.html', ctx)


@login_required
def recharge(request):
    if request.method == 'POST':
        auction_user = AuctionUser.objects.get(user=request.user)
        points = request.POST.get('points')
        auction_user.auction_points += int(points)
        auction_user.save()

        return HttpResponseRedirect(reverse('success'))

    return render(request, 'subastas/recharge.html')


@login_required
def search(request):
    QUERY = "searchField"
    MODEL_MAP = {Item: ["name"]}

    objects = []

    for model, fields in MODEL_MAP.iteritems():
        objects += generic_search(request, model, fields, QUERY)

    return render_to_response("subastas/search_results.html",
                              {"objects": objects,
                               "search_string": request.GET.get(QUERY, ""),
                               })

@login_required
def poll_auction(request):
    auction = Auction.objects.get(pk=request.GET["pk"])
    bids = len(Bid.objects.filter(auction=auction))

    end_date = {
        "year": auction.end_date.year,
        "month": auction.end_date.month,
        "day": auction.end_date.day,
        "hour": auction.end_date.hour,
        "minute": auction.end_date.minute,
        "second": auction.end_date.second,
    }

    n = timezone.now()
    now = {
        "year": n.year,
        "month": n.month,
        "day": n.day,
        "hour": n.hour,
        "minute": n.minute,
        "second": n.second,
    }

    res = { "winner": auction.winner.user.username,
            "winner_id": auction.winner.user.pk,
            "bids": bids,
            "end_date": end_date,
            "now": now,
    }

    return HttpResponse(json.dumps(res))


@login_required
def poll_offer(request):
    offer = Offer.objects.get(pk=request.GET["pk"])

    sold = 'false'
    if offer.sold:
        sold = 'true'

    res = { "winner": offer.winner.user.username,
            "winner_id": offer.winner.user.pk,
            "sold": sold,
    }

    return HttpResponse(json.dumps(res))