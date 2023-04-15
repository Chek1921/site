"""
ASGI config for mySite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from main import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mySite.settings')

django_asgi_app = get_asgi_application()

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter([
           path('ws/notify/', consumers.NotificationConsumer.as_asgi()),
        ])),
    ),
    # Just HTTP for now. (We can add other protocols later.)
})
