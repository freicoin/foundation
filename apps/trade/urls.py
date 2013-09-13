from django.conf.urls import patterns, include, url

from .views import JsonApiView

urlpatterns = patterns('apps.trade.views',

    url(r'^$', 'ng_trade', name='trade'),

    url(r'^json/$', JsonApiView.as_view(), {'action': 'get_merchants'}, name='mer_json'),

    url(r'^json/$', JsonApiView.as_view(), {'action': 'get_categories'}, name='generic_json'),
    url(r'^json/(?P<mer_id>[0-9]+)/$', JsonApiView.as_view(), {'action': 'get_merchant'}),
    url(r'^json/(?P<merchant_type>.+)/$', JsonApiView.as_view(), {'action': 'get_categories'}),

    url(r'^join/$', 'mer_edit', name='mer_new'),
    url(r'^edit/$', 'mer_edit', name='mer_edit'),
    url(r'^edit/(?P<id>\d+)/$', 'mer_edit', name='mer_edit'),
    url(r'^validate/$', 'mer_validate', name='mer_validate'),
    url(r'^validate/(?P<id>\d+)/$', 'mer_validate', name='mer_validate'),
)
