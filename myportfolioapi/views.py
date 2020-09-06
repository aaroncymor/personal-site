import logging

from django.contrib.auth.models import User
from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from blog.models import (
    Category,
    Post,
    Tag,
    Decipher
)

from .serializers import (
    UserSerializer,
    CategorySerializer,
    PostSerializer,
    TagSerializer,
    DecipherSerializer,
)

from .filters import (
    CategoryFilter,
    PostFilter,
    TagFilter,
    DecipherFilter,
)

from .pagination import CustomPagination
from .mixins import CustomListModelMixin
from .authentication import CsrfExemptSessionAuthentication

logger = logging.getLogger(__name__)

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


class PostViewSet(CustomListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)    
    filter_class = PostFilter
    pagination_class = CustomPagination


class TagViewSet(CustomListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend,)    
    filter_class = TagFilter
    pagination_class = CustomPagination


class DecipherViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Decipher.objects.all()
    serializer_class = DecipherSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = DecipherFilter

    @action(detail=True, methods=['POST'], url_name='check-code',
            authentication_classes=(CsrfExemptSessionAuthentication,
            BasicAuthentication))
    def check_code(self, request, pk=None, *args, **kwargs):
        """
        TODO: Using below reference, we need to implement a custom
        SesionAuthentication and override enforce csrf so that this
        method gets passed csrf check. 
        
        ref:
        https://www.cnblogs.com/AmilyWilly/p/6438448.html
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
        """

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
        headers = {'content-type': 'application/json'}
        response.update({'hidden_text':instance.hidden_text})
        return Response(response, status=status.HTTP_200_OK, headers=headers)

