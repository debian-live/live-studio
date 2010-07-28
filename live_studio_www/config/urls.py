from django.conf.urls.defaults import *

urlpatterns = patterns('live_studio_www.config.views',
    url(r'configs$', 'configs', name='configs'),
    url(r'config/(?P<config_id>\d+)$', 'config', name='config'),
)
