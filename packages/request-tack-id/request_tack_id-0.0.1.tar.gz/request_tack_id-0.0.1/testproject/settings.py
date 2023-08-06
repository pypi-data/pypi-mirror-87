from django.conf import global_settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

DEBUG = True

SECRET_KEY = 'secret'

ROOT_URLCONF = "testproject.urls"

INSTALLED_APPS = ["request_tack_id"]

MIDDLEWARE_CLASSES = [
    'request_tack_id.middleware.RequestIDMiddleware',
    # ... other middleware goes here
] + list(getattr(global_settings, "MIDDLEWARE_CLASSES", []))

MIDDLEWARE = MIDDLEWARE_CLASSES

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_tack_id': {
            '()': 'request_tack_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s] [%(request_tack_id)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'mock': {
            'level': 'DEBUG',
            'class': 'testproject.handler.MockLoggingHandler',
            'filters': ['request_tack_id'],
            'formatter': 'standard',
        },
    },
    'loggers': {
        'testproject': {
            'handlers': ['mock'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'request_tack_id.middleware': {
            'handlers': ['mock'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
