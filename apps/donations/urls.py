from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('apps.donations.views',

    url(r'^categories/$', views.CategoryList.as_view()),
    url(r'^categories/tree/(?P<organization_type>.+)/$', views.CategoryTree.as_view()),

    url(r'^organization/(?P<pk>[0-9]+)/$', views.OrganizationDetail.as_view()),

    url(r'^organization/create/$', views.EditOrganization.as_view()),
    url(r'^organization/edit/(?P<pk>\d+)/$', views.EditOrganization.as_view()),

    url(r'^organization/validate/(?P<pk>\d+)/$', views.ValidateOrganization.as_view()),
)
