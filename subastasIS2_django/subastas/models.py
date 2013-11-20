from django.db import models
from django.contrib.auth.models import User


class AuctionUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    birth_date = models.DateField()
    phone_number = models.DecimalField(max_digits=9, decimal_places=0, blank=True)
    points = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='/profile/', blank=True)

    is_internal = models.BooleanField(default=False)


class Item(models.Model):
    owner = models.ForeignKey(AuctionUser)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='/items/')
    category = models.CharField(max_length=100)
    first_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("can_create_item", "Can create items"),
            ("can_change_item", "Can modify items"),
        )


class Auction(models.Model):
    item = models.OneToOneField(Item, primary_key=True)
    base_price = models.PositiveIntegerField()
    current_price = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Offer(models.Model):
    item = models.OneToOneField(Item, primary_key=True)
    price = models.PositiveIntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()


class Bid(models.Model):
    user = models.ForeignKey(AuctionUser)
    auction = models.ForeignKey(Auction)
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.PositiveIntegerField()
