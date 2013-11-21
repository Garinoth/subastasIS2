from django.db import models
from django.contrib.auth.models import User


class AuctionUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    address = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=40, blank=True)
    birth_date = models.DateField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    points = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='/profile/', blank=True)


class Item(models.Model):
    owner = models.ForeignKey(AuctionUser)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='/items/', blank=True)
    category = models.CharField(max_length=100, blank=True)
    first_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("can_create_item", "Can create items"),
            ("can_change_item", "Can modify items"),
        )


class Auction(models.Model):
    item = models.OneToOneField(Item, primary_key=True)
    base_price = models.PositiveIntegerField(default=0)
    current_price = models.PositiveIntegerField(default=base_price)
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
