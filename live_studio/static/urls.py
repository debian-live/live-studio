from django.conf.urls.defaults import *

urlpatterns = patterns('live_studio.static.views',
    url(r'^$', 'welcome', name='welcome'),
)
