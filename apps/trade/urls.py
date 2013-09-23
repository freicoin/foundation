from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('apps.trade.views',

    url(r'^categories/$', views.CategoryList.as_view(), name='trade_categories'),
    url(r'^categories/tree/$', views.CategoryTree.as_view(), name='trade_category_tree'),
    url(r'^categories/tree/(?P<merchant_type>.+)/$', views.CategoryTree.as_view()),

    url(r'^merchant/$', views.MerchantDetail.as_view(), name='trade_merchant_detail'),
    url(r'^merchant/(?P<pk>[0-9]+)/$', views.MerchantDetail.as_view()),

    url(r'^merchant/edit/$', views.EditMerchant.as_view(), name='trade_merchant_edit'),
    url(r'^merchant/edit/(?P<pk>\d+)/$', views.EditMerchant.as_view()),

    url(r'^validate/$', views.ValidateMerchant.as_view(), name='trade_merchant_validate'),
    url(r'^validate/(?P<pk>\d+)/$', views.ValidateMerchant.as_view()),
)
