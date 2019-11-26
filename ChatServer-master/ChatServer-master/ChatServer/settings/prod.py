from .base import *

DEBUG=False

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS = {
    'host': os.environ.get('REDIS_HOST', ''),
    'port': int(os.environ.get('REDIS_PORT', '')),
    'db': int(os.environ.get('REDIS_DB', '0')),
    'password': os.environ.get('REDIS_PASSWORD', 'session'),
    'prefix': os.environ.get('REDIS_PREFIX', ''),
    'socket_timeout': int(os.environ.get('REDIS_TIMEOUT', '1')),
    'retry_on_timeout': False
    }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASS', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get('REDIS_HOST', ''), int(os.environ.get('REDIS_PORT', '')))],
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp-relay.gmail.com'
EMAIL_HOST_USER = 'noreply@domain.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_AUTO_CREATE_BUCKET = True
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_IS_GZIPPED = True
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read'

STATICFILES_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATICFILES_STORAGE = 'ChatServer.storage.StaticStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'ChatServer.storage.MediaStorage'

CONFIGFILES_LOCATION = 'config'
CONFIG_STORAGE_CLASS = 'ChatServer.storage.ConfigStorage'