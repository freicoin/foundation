from django.conf.urls import patterns, include, url

from apps.donations.views import OrgListView, OrgDetailView

urlpatterns = patterns('apps.donations.views',

    url(r'^$', 'ng_view', name='organization_list'),
    url(r'^json/$', OrgListView.as_view(), {'action': 'get_organizations'}, name='org_list_json'),
    url(r'^json/(?P<organization_id>[0-9]+)/$', OrgDetailView.as_view(), 
        {'action': 'get_organization'}, name='org_list_json'),

    url(r'^join/$', 'new_organization', name='organization_new'),
    url(r'^join/thanks/$', 'thanks', name='org_thanks'),
)
