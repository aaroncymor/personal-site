from django.conf import settings
from django.urls import re_path, include

from rest_framework import routers

from .views import FacebookChatbotViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'fb', FacebookChatbotViewSet, base_name='fb-chatbot')

app_name = 'chatbot-api'
urlpatterns = [
    re_path(r'^', include(router.urls), name='v1'),
]