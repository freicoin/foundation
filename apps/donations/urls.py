from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('apps.donations.views',

    url(r'^$', 'ng_donations', name='nonprofits'),

    # url(r'^categories/$', views.CategoryList.as_view(), name='donations_categories'),
    url(r'^categories/$', views.JsonApiView.as_view(), {'action': 'get_categories'}, name='donations_categories'),
    # url(r'^categories/tree/$', views.CategoryTree.as_view(), name='donations_category_tree'),
    url(r'^categories/tree/$', views.JsonApiView.as_view(), {'action': 'get_categories'}, name='donations_category_tree'),
    # url(r'^categories/tree/(?P<organization_type>.+)/$', views.CategoryTree.as_view()),
    url(r'^categories/tree/(?P<org_type>.+)/$', views.JsonApiView.as_view(), {'action': 'get_categories'}),

    url(r'^organization/$', views.OrganizationDetail.as_view(), name='donations_organization_detail'),
    url(r'^organization/(?P<pk>[0-9]+)/$', views.OrganizationDetail.as_view()),

    # url(r'^organization/edit/$', views.EditOrganization.as_view(), name='donations_organization_edit'),
    url(r'^organization/edit/$', 'org_edit', name='donations_organization_edit'),
    # url(r'^organization/edit/(?P<pk>\d+)/$', views.EditOrganization.as_view()),
    url(r'^organization/edit/(?P<id>\d+)/$', 'org_edit'),

    # url(r'^validate/$', views.ValidateOrganization.as_view(), name='donations_organization_validate'),
    url(r'^validate/$', 'org_validate', name='donations_organization_validate'),
    # url(r'^validate/(?P<pk>\d+)/$', views.ValidateOrganization.as_view()),
    url(r'^validate/(?P<id>\d+)/$', 'org_validate'),


)
