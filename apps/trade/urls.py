from django.conf.urls import patterns, include, url

from .views import JsonApiView, MerchantDetail, MerchantValidate

urlpatterns = patterns('apps.trade.views',

    url(r'^$', 'ng_trade', name='trade'),

    url(r'^json/$', JsonApiView.as_view(), {'action': 'get_categories'}, name='trade_json'),

    url(r'^json/(?P<pk>[0-9]+)/$', MerchantDetail.as_view()),
    url(r'^json/(?P<merchant_type>.+)/$', JsonApiView.as_view(), {'action': 'get_categories'}),

    url(r'^join/$', 'mer_edit', name='mer_new'),
    url(r'^edit/$', 'mer_edit', name='mer_edit'),
    url(r'^edit/(?P<id>\d+)/$', 'mer_edit', name='mer_edit'),
    url(r'^validate/$', MerchantValidate.as_view(), name='mer_validate'),
    url(r'^validate/(?P<pk>\d+)/$', MerchantValidate.as_view()),
)
