from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',

    url(r'^current_user/$', views.CurrentUser.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^logout/$', views.Logout.as_view()),
    url(r'^register/$', views.Register.as_view()),
    url(r'^change_password/$', views.ChangePass.as_view()),
)

