from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, status, viewsets, serializers
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response

from blog.models import (
    Category,
    Post,
    Tag,
    Decipher
)

from projects.models import Project

from .serializers import (
    UserSerializer,
    CategorySerializer,
    PostSerializer,
    TagSerializer,
    ProjectSerializer,
    DecipherSerializer,
)

from .filters import (
    CategoryFilter,
    PostFilter,
    TagFilter,
    DecipherFilter,
    ProjectFilter,
)

# Create your views here.

class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CategoryFilter


class PostViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)    
    filter_class = PostFilter


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend,)    
    filter_class = TagFilter


class DecipherViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Decipher.objects.all()
    serializer_class = DecipherSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = DecipherFilter


class ProjectViewSet(mixins.ListModelMixin, 
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (DjangoFilterBackend,)    
    filter_class = ProjectFilter