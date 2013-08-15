from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.donations.views',

    url(r'^$', 'organization_list', name='organization_list'),
    url(r'^detail/(?P<organization_id>[0-9]+)/$', 'organization_detail', name='organization_detail'),
    url(r'^join/$', 'new_organization', name='organization_new'),
    url(r'^join/thanks/$', 'thanks', name='thanks'),
)
