from django.conf.urls.defaults import *

urlpatterns = patterns('live_studio_www.config.views',
    url(r'configs$', 'configs', name='configs'),
    url(r'config/(?P<config_id>\d+)$', 'view', name='view'),
    url(r'config/(?P<config_id>\d+)/edit$', 'edit', name='edit'),
)
