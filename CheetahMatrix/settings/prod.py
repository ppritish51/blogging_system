from .base import *
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
dotenv_path = '/var/produser/cheetah-matrix/config/prod.env'
print(dotenv_path)
load_dotenv(dotenv_path)

# Now you can access the environment variables using os.getenv
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False  # Convert string to bool
ALLOWED_HOSTS = ['198.71.55.91',
                 'cheetahmatrix.slowestcheetah.com',
                 'slowestcheetah.com',
                 'educationcounsellingcenter.com']

CORS_ALLOW_ALL_ORIGINS = False  # Do not allow all origins

# Construct CORS_ALLOWED_ORIGINS from ALLOWED_HOSTS
CORS_ALLOWED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]  # Add https variants too

# Add the frontend URL to the list of allowed origins
CORS_ALLOWED_ORIGINS += [
    'http://localhost:7534',
    'https://slowestcheetah.com',
    'https://www.slowestcheetah.com',
    'https://cheetahmatrix.slowestcheetah.com']

CORS_ALLOW_CREDENTIALS = True

WSGI_APPLICATION = 'CheetahMatrix.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cheetah_matrix_dev',
        'USER': 'superuser',
        'PASSWORD': 'Temp@Pri30two',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 5,  # add this line
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
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
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
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
        'burst': '2/second',
        'sustained': '50/hour',

        'anon': '500/hour',
        'user': '1000/hour',
        'password_reset_via_email': '5/day',
        'search': '60/min',
        'copy_clipboard': '8/min',
        'education': '10/min',  # The custom throttle rate for "education"
        'blog': '120/min'
    }
}

STATIC_URL = 'static/'
STATIC_ROOT = '/var/produser/cheetah-matrix/static/'

SENDINBLUE_API_KEY = ""
RESET_PASSWORD_BASE_URL = "http://www.slowestcheetah.com/reset-password"

OPEN_AI_KEY = ""
OPEN_AI_ORG_ID = ""

LOGGING_VALUE = 'ERROR'
if DEBUG:
    LOGGING_VALUE = 'DEBUG'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": LOGGING_VALUE,
            "class": "logging.FileHandler",
            "filename": "/var/www/dev/debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": LOGGING_VALUE,
            "propagate": True,
        },
    },
}

ML_END_SERVICE_URL = 'http://198.71.55.91:7777/internal-chat/'
