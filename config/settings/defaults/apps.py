INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',

    'live_studio_www.auth',
]

try:
    import django_extensions

    INSTALLED_APPS.append('django_extensions')
except ImportError:
    pass
