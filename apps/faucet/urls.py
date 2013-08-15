from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.faucet.views',

    url(r'^$', 'faucet', name='faucet'),
    url(r'^recent/$', 'recent_sends', name='recent_sends'),
)
