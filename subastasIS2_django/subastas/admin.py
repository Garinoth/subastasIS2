from django.contrib import admin
from subastas.models import ExternalUser, Item, Auction, Offer, Bid

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# from my_user_profile_app.models import User

admin.site.register(ExternalUser)
admin.site.register(Item)
admin.site.register(Auction)
admin.site.register(Offer)
admin.site.register(Bid)
