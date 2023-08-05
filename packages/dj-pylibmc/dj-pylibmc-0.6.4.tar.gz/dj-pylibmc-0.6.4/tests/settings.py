DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testing',
        'SUPPORTS_TRANSACTIONS': False,
    },
}

INSTALLED_APPS = ('tests',)

CACHES = {
    'default': {
        'BACKEND': 'dj_pylibmc.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'binary': {
        'BACKEND': 'dj_pylibmc.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'BINARY': True,
    },
    'with_options': {
        'BACKEND': 'dj_pylibmc.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'OPTIONS': {'tcp_nodelay': True, 'ketama': True},
    },
}

PYLIBMC_MIN_COMPRESS_LEN = 150 * 1024
PYLIBMC_COMPRESS_LEVEL = 1  # zlib.Z_BEST_SPEED

SECRET_KEY = 'secret'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {'django': {'handlers': ['console'], 'level': 'CRITICAL'}},
}
