from django.conf.urls.defaults import *

urlpatterns = patterns('live_studio.config.views',
    url(r'config/add$', 'add', name='add'),
    url(r'configs$', 'configs', name='configs'),
    url(r'config/(?P<config_id>\d+)$', 'view', name='view'),
    url(r'config/(?P<config_id>\d+)/edit$', 'edit', name='edit'),
)
