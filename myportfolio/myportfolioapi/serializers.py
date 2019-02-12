from django.contrib.auth.models import User

from rest_framework import serializers

from blog.models import Category, Post, Tag
from projects.models import Project


class UserSerializer(serializers.HyperlinkedModelSerializer):
    _link = serializers.HyperlinkedIdentityField(
        view_name='api:user-detail'
    )
    class Meta:
        model = User
        fields = ('_link', 'username', 'first_name', 'last_name', 
                  'email', 'groups', 'user_permissions', 'is_staff',
                  'is_superuser', 'last_login', 'date_joined'
                )


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    _link = serializers.HyperlinkedIdentityField(
        view_name='api:category-detail'
    )
    posts = serializers.HyperlinkedRelatedField(
       many=True,
       view_name='api:post-detail',
       read_only=True
    )
    class Meta:
        model = Category
        fields = ('_link', 'id', 'name', 'timestamp', 'posts')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    _link = serializers.HyperlinkedIdentityField(
        view_name='api:post-detail'
    )
    category = serializers.HyperlinkedIdentityField(
        view_name='api:category-detail'
    )
    tags = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='api:tag-detail',
        read_only=True
    )
    class Meta:
        model = Post
        fields = ('_link', 'id', 'category',  'title', 'content', 'published_date', 'timestamp', 'tags')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    _link = serializers.HyperlinkedIdentityField(
        view_name='api:tag-detail'
    )
    post = serializers.HyperlinkedIdentityField(
        view_name='api:post-detail'
    )
    
    class Meta:
        model = Tag
        fields = ('_link', 'id', 'tag', 'post', 'timestamp')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'description', 'rank')