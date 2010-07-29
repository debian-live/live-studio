from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('live_studio.debug.views',
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^builds/(?P<path>.*)$', 'serve',
            {'document_root': settings.BUILDS_DIR}),
        (r'^(?P<path>favicon.ico|robots\.txt)$', 'serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
