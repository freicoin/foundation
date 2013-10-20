from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import views

urlpatterns = patterns('',

    url(r'^registration_confirm/(?P<uidb36>.+)/(?P<token>.+)/$', 
        'apps.accounts.views.registration_confirm',
        name='registration_confirm'),

    url(r'^password_reset_confirm/(?P<uidb36>.+)/(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'template_name': 'password_reset_confirm.html'},
        name='password_reset_confirm'),

    url(r'^password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete', 
        {'template_name': 'password_reset_complete.html'}),
)
