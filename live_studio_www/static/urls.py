from django.conf.urls.defaults import *

urlpatterns = patterns('live_studio_www.static.views',
    url(r'^$', 'welcome', name='welcome'),
)
