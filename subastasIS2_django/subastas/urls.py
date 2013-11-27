from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from subastas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.ListUsersView.as_view(), name='test'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'subastas/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'index'}, name='logout'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^tos/$', views.tos, name='tos'),
    url(r'^activation/$', views.activation, name='activation'),
    url(r'^activation/(?P<activation_key>\w+)/$', views.activation, name='activation'),
    url(r'^auctions/$', login_required(views.ListAuctionsView.as_view()), name='auctions'),
    url(r'^auctions/(?P<pk>\d+)$', login_required(views.DetailAuctionView.as_view()), name='auction_detail'),
    url(r'^item/$', views.create_item, name='item'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
