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

try:
    import django_extensions

    INSTALLED_APPS.append('django_extensions')
except ImportError:
    pass
