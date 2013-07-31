# Django.core
from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Foundation
    (r'^$', 'foundation.views.home'),
    (r'^about/$', 'foundation.views.about'),

    # Donations
    (r'^join_nonprofits/$', 'donations.views.new_organization'),
    (r'^join_nonprofits/thanks/$', 'donations.views.thanks'),
    (r'^nonprofits/$', 'donations.views.organization_list'),
    (r'^nonprofit/(?P<organization_id>[0-9]+)/$', 'donations.views.organization_detail'),

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
