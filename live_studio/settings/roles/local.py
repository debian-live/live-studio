from os.path import dirname, join, abspath

_BASE = dirname(dirname(dirname(dirname(abspath(__file__)))))

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = join(_BASE, 'htdocs', 'media')
BUILDS_ROOT = join(_BASE, 'builds')
TEMPLATE_DIRS = (join(_BASE, 'templates'),)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
