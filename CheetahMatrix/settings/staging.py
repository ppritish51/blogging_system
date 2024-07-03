from .base import *
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'staging', 'config', 'staging.env'))
print(dotenv_path)
load_dotenv(dotenv_path)

# Now you can access the environment variables using os.getenv
SECRET_KEY = os.getenv("SECRET_KEY", 'staging-secret-key')
DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", 'localhost,127.0.0.1,198.71.55.91').split(',')  # Convert string to list

CORS_ALLOWED_ORIGINS = [
    "chrome-extension://your-chrome-extension-id",
]
CORS_ALLOW_CREDENTIALS = True

WSGI_APPLICATION = 'CheetahMatrix.wsgi.application'
# ASGI_APPLICATION = 'CheetahMatrix.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'staging_db',
        'USER': 'staging_user',
        'PASSWORD': 'staging_password',
        'HOST': 'staging_db_host',
        'PORT': '5432',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=360),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '400/hour',
        'password_reset_via_email': '8/day',
    }
}

SENDINBLUE_API_KEY = os.getenv("SENDINBLUE_API_KEY")
RESET_PASSWORD_BASE_URL = "http://staging.cheetahmatrix.com"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/root/staging/logs/error.log',
        },
        'file_request': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/root/staging/logs/request.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_error', 'file_request'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}