from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from subastas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.ListUsersView.as_view(), name='test'),
    url(r'^help/$', views.help, name='help'),
    url(r'^search/$', views.search, name='search'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'subastas/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'index'}, name='logout'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^tos/$', views.tos, name='tos'),
    url(r'^activation/$', views.activation, name='activation'),
    url(r'^activation/(?P<activation_key>\w+)/$', views.activation, name='activation'),
    url(r'^item/$', views.create_item, name='item'),
    url(r'^auctions/$', login_required(views.ListAuctionsView.as_view()), name='auctions'),
    url(r'^auctions/(?P<pk>\d+)/$', views.auction, name='auction_detail'),
    url(r'^offers/$', login_required(views.ListOffersView.as_view()), name='offers'),
    url(r'^offers/(?P<pk>\d+)/$', views.offer, name='offer_detail'),
    url(r'^recharge/$', views.recharge, name='recharge'),
    url(r'^success/$', views.success, name='success'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
