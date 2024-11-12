"""
Файл с WebSocket путями
"""

from .consumers import Notifications
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"ws/notifications/$", Notifications.as_asgi()),
]
