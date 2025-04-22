# Mecanicien_prestataire/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import message.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mecanicien_prestataire.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            message.routing.websocket_urlpatterns
        )
    ),
})
