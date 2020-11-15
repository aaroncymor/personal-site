from django.conf import settings
from django.urls import re_path, include

from rest_framework import routers

from personal_site_api.views import (
    UserViewSet,
    CategoryViewSet,
    PostViewSet,
    TagViewSet,
    DecipherViewSet,
    autocomplete_search
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, base_name='user')
router.register(r'categories', CategoryViewSet, base_name='category')
router.register(r'posts', PostViewSet, base_name='post')
router.register(r'tags', TagViewSet, base_name='tag')
router.register(r'deciphers', DecipherViewSet, base_name='decipher')

app_name = 'api'
urlpatterns = [
    re_path(r'^', include(router.urls), name='v1'),
    re_path(r'autocomplete', autocomplete_search, name='autocomplete-search'),
]