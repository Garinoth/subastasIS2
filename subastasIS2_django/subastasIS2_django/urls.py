from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'subastasIS2_django.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^subastas/', include('subastas.urls')),

)
