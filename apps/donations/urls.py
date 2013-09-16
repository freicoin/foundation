from django.conf.urls import patterns, include, url

from .views import JsonApiView

urlpatterns = patterns('apps.donations.views',

    url(r'^$', 'ng_donations', name='nonprofits'),

    url(r'^json/$', JsonApiView.as_view(), {'action': 'get_categories'}, name='donations_json'),

    url(r'^json/(?P<org_id>[0-9]+)/$', JsonApiView.as_view(), {'action': 'get_organization'}),
    url(r'^json/(?P<org_type>.+)/$', JsonApiView.as_view(), {'action': 'get_categories'}),

    url(r'^join/$', 'org_edit', name='org_new'),
    url(r'^edit/$', 'org_edit', name='org_edit'),
    url(r'^edit/(?P<id>\d+)/$', 'org_edit', name='org_edit'),
    url(r'^validate/$', 'org_validate', name='org_validate'),
    url(r'^validate/(?P<id>\d+)/$', 'org_validate', name='org_validate'),
)
