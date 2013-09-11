from django.conf.urls import patterns, include, url

from .views import MerchantListView, MerchantDetailView

urlpatterns = patterns('apps.trade.views',

    url(r'^$', 'ng_trade', name='trade'),
    url(r'^json/$', MerchantListView.as_view(), {'action': 'get_merchants'}, name='mer_json'),
    url(r'^json/(?P<mer_id>[0-9]+)/$', MerchantDetailView.as_view(), 
        {'action': 'get_merchant'}, name='mer_json'),

    url(r'^join/$', 'mer_edit', name='mer_new'),
    url(r'^edit/$', 'mer_edit', name='mer_edit'),
    url(r'^edit/(?P<id>\d+)/$', 'mer_edit', name='mer_edit'),
    url(r'^validate/$', 'mer_validate', name='mer_validate'),
    url(r'^validate/(?P<id>\d+)/$', 'mer_validate', name='mer_validate'),
    url(r'^join/thanks/$', 'thanks', name='mer_thanks'),
)
