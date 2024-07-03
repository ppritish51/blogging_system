from .base import *

DEBUG = True
SECRET_KEY = 'django-insecure-+u$=1&=cdvo0g+373!&$o1ia--9+m)hk_0w8)&jtybkb5x(-h7'

ALLOWED_HOSTS = []

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

WSGI_APPLICATION = 'CheetahMatrix.wsgi.application'
# ASGI_APPLICATION = 'CheetahMatrix.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
        'burst': '2/second',
        'sustained': '10/min',

        'anon': '10000/hour',
        'user': '10000/hour',
        'password_reset_via_email': '4/day',
        'search': '6000/hour',
        'copy_clipboard': '6/min',
        'education': '10/min',  # The custom throttle rate for "education"
        'blog': '120/min'
    }
}

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

SENDINBLUE_API_KEY = "aces-sg435-asfgd"
RESET_PASSWORD_BASE_URL = "http://localhost:8000"

OPEN_AI_KEY = ""
OPEN_AI_ORG_ID = ""

ML_END_SERVICE_URL = 'http://127.0.0.1:7777/internal-chat/'
