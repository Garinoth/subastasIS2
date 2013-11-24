from django.conf.urls import patterns, url

from subastas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.ListUsersView.as_view(), name='test'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'subastas/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'index'}, name='logout'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^tos/$', views.tos, name='tos'),
    )
