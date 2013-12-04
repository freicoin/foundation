from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.faucet.views',

    url(r'^faucet.html$', 'faucet', name='faucet'),
    url(r'^recent.html$', 'recent_sends'),
)
