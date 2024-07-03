import jwt
from django.conf import settings
from datetime import datetime, timedelta

def generate_forgot_password_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=2)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
