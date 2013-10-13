# Django.core
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.shortcuts import redirect

def forum_hack(request, anystring):
    url = 'http://freicoin.freeforums.org/%s' % anystring

    if request.META['QUERY_STRING']:
        url += '?%s' % request.META['QUERY_STRING']
    return redirect(url)

urlpatterns = patterns('',

    # Angular App
    url(r'^$', TemplateView.as_view(template_name='ng-app.html'), name='home'),

    # Included apps and their root
    url(r'api/accounts/', include('apps.accounts.urls')),
    # url(r'^faucet/', include('apps.faucet.urls')),
    url(r'^api/donations/', include('apps.donations.urls')),
    url(r'^api/trade/', include('apps.trade.urls')),

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

    # url(r'^(?P<anystring>.+)/$', forum_hack),
)
