from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from subastas.forms import UserForm, AuctionUserForm, ItemForm, AuctionForm, OfferForm, BidForm, ActivationForm, SaleForm
from subastas.models import Auction, Offer, AuctionUser


class ListUsersView(ListView):

    model = User
    template_name = 'subastas/user_list_dummy.html'


class ListAuctionsView(ListView):

    model = Auction
    queryset = Auction.objects.order_by('end_date')
    context_object_name = 'auction_list'
    template_name = 'subastas/auctions.html'


class DetailAuctionView(DetailView):

    model = Auction
    context_object_name = 'auction'


class ListOffersView(ListView):

    model = Offer
    queryset = Offer.objects.order_by('end_date')
    context_object_name = 'offer_list'
    template_name = 'subastas/offers.html'


class DetailOfferView(DetailView):

    model = Offer
    context_object_name = 'offer'


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
            bid.auction.save()
            bid.save()

            return HttpResponseRedirect(reverse('auction_detail', args=pk))

        else:
            if 'recharge' in bid_form.errors:
                recharge = True


    else:
        bid_form = BidForm()

    ctx = {
        'auction': auction,
        'bid_form': bid_form,
        'recharge': recharge
    }

    return render(request, 'subastas/auction_detail.html', ctx)


@login_required
def offer(request, pk):
    offer = Offer.objects.get(pk=pk)

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

                return HttpResponseRedirect(reverse('offers'))

    else:
        sale_form = SaleForm()
        valid = False

    ctx = {
        'offer': offer,
        'sale_form': sale_form,
        'valid': valid,

    }

    return render(request, 'subastas/offer_detail.html', ctx)
