from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import hashlib
import random


User._meta.get_field('email')._unique = True
User.USERNAME_FIELD = 'email'
User.REQUIRED_FIELDS = ['username']


class AuctionUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    address = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=40, blank=True)
    birth_date = models.DateField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    auction_points = models.PositiveIntegerField(default=0)
    offer_points = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='/profile/', blank=True)

    activation_key = models.CharField(max_length=40, blank=True)

    def __unicode__(self):
        return u'%s' % (self.user.username)

    def set_activation_key(self):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        email = self.user.email
        if isinstance(email, unicode):
            email = email.encode('utf-8')
        self.activation_key = hashlib.sha1(salt + email).hexdigest()

    def send_activation_email(self):

        ctx_dict = {
            'username': self.user.username,
            'activation_key': self.activation_key,
        }

        subject = render_to_string('subastas/activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('subastas/activation_email.txt',
                                   ctx_dict)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


class Item(models.Model):
    owner = models.ForeignKey(AuctionUser)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='items/', blank=True)
    category = models.CharField(max_length=100, blank=True)
    first_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        permissions = (
            ("can_create_item", "Can create items"),
            ("can_change_item", "Can modify items"),
        )


class Auction(models.Model):
    item = models.OneToOneField(Item, primary_key=True)
    base_price = models.PositiveIntegerField(default=0)
    current_price = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __unicode__(self):
        return u'%s' % (self.item.name)


class Offer(models.Model):
    item = models.OneToOneField(Item, primary_key=True)
    price = models.PositiveIntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __unicode__(self):
        return u'%s' % (self.item.name)


class Bid(models.Model):
    user = models.ForeignKey(AuctionUser)
    auction = models.ForeignKey(Auction)
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()

    def __unicode__(self):
        return u'user: %s at auction: %s for %s' % (self.user.name, self.auction.item.name, self.points)
