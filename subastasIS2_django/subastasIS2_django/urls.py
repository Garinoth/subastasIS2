from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'subastasIS2_django.views.home', name='home'),
    url(r'^$', RedirectView.as_view(url='/subastas/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^subastas/', include('subastas.urls')),
)
