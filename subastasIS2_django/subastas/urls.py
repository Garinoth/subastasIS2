from django.conf.urls import patterns, url

from subastas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'subastas/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'subastas/logout.html', 'next_page': 'test'}, name='logout'),
    )
