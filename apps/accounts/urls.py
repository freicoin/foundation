from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register/$', 'apps.accounts.views.register', name='register'),
)

