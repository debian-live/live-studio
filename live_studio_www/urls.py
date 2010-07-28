from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'', include('live_studio_www.debug.urls', namespace='debug')),
    (r'', include('live_studio_www.config.urls', namespace='config')),
    (r'', include('live_studio_www.static.urls', namespace='static')),
)
