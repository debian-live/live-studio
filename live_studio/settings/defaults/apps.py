INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',

    'registration',

    'live_studio.auth',
    'live_studio.build',
    'live_studio.utils',
    'live_studio.debug',
    'live_studio.config',
    'live_studio.static',
    'live_studio.templatetags',
]

for module in ('django_extensions', 'debug_toolbar'):
    try:
        __import__(module)
        INSTALLED_APPS.append(module)
    except ImportError:
        pass

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
