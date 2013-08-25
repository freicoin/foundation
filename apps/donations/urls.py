from django.conf.urls import patterns, include, url

from apps.donations.views import OrgListView, OrgDetailView

urlpatterns = patterns('apps.donations.views',

    url(r'^$', 'ng_view', name='nonprofits'),
    url(r'^json/$', OrgListView.as_view(), {'action': 'get_organizations'}, name='org_list_json'),
    url(r'^json/(?P<organization_id>[0-9]+)/$', OrgDetailView.as_view(), 
        {'action': 'get_organization'}, name='org_list_json'),

    url(r'^join/$', 'org_edit', name='organization_new'),
    url(r'^edit/(?P<id>\d+)/$', 'org_edit', name='organization_edit'),
    url(r'^join/thanks/$', 'thanks', name='org_thanks'),

    url(r'^partials/list.html$', 'organization_list', name='organization_list'),
)
