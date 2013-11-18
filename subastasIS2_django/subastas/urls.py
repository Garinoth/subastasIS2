from django.conf.urls import patterns, url

from subastas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^test/$', views.test, name='test'),

    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'subastas/login.html'}),
)
