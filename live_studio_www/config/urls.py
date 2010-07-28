from django.conf.urls.defaults import *

urlpatterns = patterns('live_studio_www.config.views',
    url(r'configs$', 'configs', name='configs'),
)
