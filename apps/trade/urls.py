from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('apps.trade.views',

    url(r'^categories/$', views.CategoryList.as_view()),
    url(r'^categories/tree/(?P<merchant_type>.+)/$', views.CategoryTree.as_view()),

    url(r'^merchant/(?P<pk>[0-9]+)/$', views.MerchantDetail.as_view()),

    url(r'^merchant/create/$', views.EditMerchant.as_view()),
    url(r'^merchant/edit/(?P<pk>\d+)/$', views.EditMerchant.as_view()),

    url(r'^merchant/validate/(?P<pk>\d+)/$', views.ValidateMerchant.as_view()),
)
