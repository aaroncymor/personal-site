from django.contrib.auth.models import User

from rest_framework import serializers

from blog.models import Category, Post, Tag, Decipher
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
    #posts = serializers.HyperlinkedRelatedField(
    #   many=True,
    #   view_name='api:post-detail',
    #   read_only=True
    #)
    class Meta:
        model = Category
        fields = ('_link', 'id', 'name', 'timestamp')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    _link = serializers.HyperlinkedIdentityField(
        view_name='api:post-detail'
    )

    category = CategorySerializer()

    tags = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='api:tag-detail',
        read_only=True
    )
    deciphers = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='api:decipher-detail',
        read_only=True
    )
    class Meta:
        model = Post
        fields = ('_link', 'id', 'category', 'title', 'content', 'published_date', 'timestamp', 'tags', 'deciphers')


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


class DecipherSerializer(serializers.HyperlinkedModelSerializer):
    _link = serializers.HyperlinkedIdentityField(
        view_name='api:decipher-detail'
    )
    post = PostSerializer()
    class Meta:
        model = Decipher
        fields = ('_link', 'id', 'post', 'hidden_text', 
                  'name', 'challenge', 'clue', 'code')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'rank')