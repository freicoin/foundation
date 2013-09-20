from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('apps.trade.views',

    url(r'^$', 'ng_trade', name='trade'),

    url(r'^json/$', views.CategoryList.as_view(), name='trade_json'),

    url(r'^json/(?P<pk>[0-9]+)/$', views.MerchantDetail.as_view()),
    url(r'^json/(?P<merchant_type>.+)/$', views.CategoryList.as_view()),

    url(r'^join/$', 'mer_edit', name='mer_new'),
    url(r'^edit/$', 'mer_edit', name='mer_edit'),
    url(r'^edit/(?P<id>\d+)/$', 'mer_edit', name='mer_edit'),
    url(r'^validate/$', views.ValidateMerchant.as_view(), name='mer_validate'),
    url(r'^validate/(?P<pk>\d+)/$', views.ValidateMerchant.as_view()),
)
