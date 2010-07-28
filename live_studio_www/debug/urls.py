from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('live_studio_www.debug.views',
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^(?P<path>favicon.ico|robots\.txt)$', 'serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
