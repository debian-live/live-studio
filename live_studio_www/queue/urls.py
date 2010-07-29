from django.conf.urls.defaults import *

urlpatterns = patterns('live_studio_www.queue.views',
    url('config/(?P<config_id>\d+)/enqueue', 'enqueue',
        name='enqueue'),
)
