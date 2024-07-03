# myproject/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from ChatGptHelper.ChatGptHiringAssistant.consumers import InterviewSessionConsumer
from .routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CheetahMatrix.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
