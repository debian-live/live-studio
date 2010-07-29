from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),

    (r'', include('live_studio.debug.urls', namespace='debug')),
    (r'', include('live_studio.build.urls', namespace='build')),
    (r'', include('live_studio.config.urls', namespace='config')),
    (r'', include('live_studio.static.urls', namespace='static')),
)
