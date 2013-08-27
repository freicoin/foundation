from django.conf.urls import patterns, include, url

from .views import OrgListView, OrgDetailView

urlpatterns = patterns('apps.donations.views',

    url(r'^$', 'ng_donations', name='nonprofits'),
    url(r'^json/$', OrgListView.as_view(), {'action': 'get_organizations'}, name='org_json'),
    url(r'^json/(?P<org_id>[0-9]+)/$', OrgDetailView.as_view(), 
        {'action': 'get_organization'}, name='org_json'),

    url(r'^join/$', 'org_edit', name='org_new'),
    url(r'^edit/$', 'org_edit', name='org_edit'),
    url(r'^edit/(?P<id>\d+)/$', 'org_edit', name='org_edit'),
    url(r'^join/thanks/$', 'thanks', name='org_thanks'),
)
