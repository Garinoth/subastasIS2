from django.contrib import admin
from subastas.models import Auction, Bid, ExternalUser, InternalUser, Item

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# from my_user_profile_app.models import User

admin.site.register(Auction)
admin.site.register(ExternalUser)
admin.site.register(InternalUser)
admin.site.register(Item)
