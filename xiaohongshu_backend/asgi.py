import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import xiaohongshu_backend.messaging.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xiaohongshu_backend.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            xiaohongshu_backend.messaging.routing.websocket_urlpatterns
        )
    ),
})
