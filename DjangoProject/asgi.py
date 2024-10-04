import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # Add this for handling sessions/auth
from django.urls import path
from charging.consumer import OCPPConsumer
import django
from django.urls import re_path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject.settings")

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        re_path(r"^IonBee/ocpp/(?P<company_id>[^/]+)/(?P<charge_point_id>[^/]+)/$", OCPPConsumer.as_asgi()),
    ]),
})