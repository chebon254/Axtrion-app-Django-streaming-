"""
ASGI config for axtrion project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
# axtrion/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from main.consumers import *
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axtrion.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # Add your WebSocket consumers here
            path('ws/live_stream/', LiveStreamConsumer.as_asgi()),
        )
    ),
})

