# Django.core
from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Foundation
    url(r'^$', 'foundation.views.home', name='home'),
    url(r'^about/$', 'foundation.views.about', name='about'),
    url(r'^copyright/$', 'foundation.views.copyright', name='copyright'),

    # Included apps and their root
    url(r'', include('apps.accounts.urls')),
    url(r'^faucet/', include('apps.faucet.urls')),
    url(r'^nonprofits/', include('apps.donations.urls')),

    # Examples:
    # url(r'^$', 'foundation.views.home', name='home'),
    # url(r'^foundation/', include('foundation.foo.urls')),

    ###################
    # Admin Interface #
    ###################

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
