MIDDLEWARE_CLASSES = [
    'live_studio.auth.middleware.SetRemoteAddrFromForwardedFor',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'live_studio.auth.middleware.RequireLoginMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
]

try:
    import debug_toolbar

    MIDDLEWARE_CLASSES.append(
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
except ImportError:
    pass
