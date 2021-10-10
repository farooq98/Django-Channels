from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/issue/$', consumers.ChatConsumer),
    re_path(r'ws/issue/(?P<issue_id>\w+)/$', consumers.ChatConsumer),
]
