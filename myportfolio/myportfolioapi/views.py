from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, status, viewsets, serializers
from rest_framework.decorators import action
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

    @action(detail=True, methods=['POST'])
    def check_code(self, request, pk=None, *args, **kwargs):
        response = {}
        if 'code' not in request.POST:
            response['error'] = 'The code is required.'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        code = request.POST['code']
        instance = self.get_object()
        
        if instance.code:
            if code != instance.code:
                response['error'] = 'The code is not matching with decipher code.'
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance)
        response['data'] = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class ProjectViewSet(mixins.ListModelMixin, 
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (DjangoFilterBackend,)    
    filter_class = ProjectFilter