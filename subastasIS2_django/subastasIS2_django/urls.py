from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'subastasIS2_django.views.home', name='home'),
    url(r'^subastas/', include('subastas.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
