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

    # Donations
    url(r'^join_nonprofits/$', 'apps.donations.views.new_organization', name='organization_new'),
    url(r'^join_nonprofits/thanks/$', 'apps.donations.views.thanks', name='thanks'),
    url(r'^nonprofits/$', 'apps.donations.views.organization_list', name='organization_list'),
    url(r'^nonprofit/(?P<organization_id>[0-9]+)/$', 'apps.donations.views.organization_detail', name='organization_detail'),

    # Faucet
    (r'^faucet/$', 'apps.faucet.views.faucet'),
    (r'^faucet/recent/$', 'apps.faucet.views.recent_sends'),

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
