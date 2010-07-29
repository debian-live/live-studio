MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'live_studio_www.auth.middleware.RequireLoginMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)
