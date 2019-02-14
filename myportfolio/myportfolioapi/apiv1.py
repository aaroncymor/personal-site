from django.conf import settings
from django.urls import re_path, include

from rest_framework import routers

from .views import (
    UserViewSet,
    CategoryViewSet,
    PostViewSet,
    TagViewSet,
    ProjectViewSet
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, base_name='user')
router.register(r'categories', CategoryViewSet, base_name='category')
router.register(r'posts', PostViewSet, base_name='post')
router.register(r'tags', TagViewSet, base_name='tag')
router.register(r'projects', ProjectViewSet, base_name='project')

app_name = 'api'
urlpatterns = [
    re_path(r'^', include(router.urls), name='v1'),
]