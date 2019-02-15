import django_filters as filters
from django_filters.rest_framework import FilterSet

from blog.models import (
    Category,
    Post,
    Tag
)

from projects.models import Project

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class CategoryFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    post_id = filters.NumberFilter(field_name='posts__id')
    post_title = filters.CharFilter(field_name='posts__title', lookup_expr='iexact')
    tag_id = filters.NumberFilter(field_name='posts__tags__id')
    tag = filters.CharFilter(field_name='posts__tags')
    
    class Meta:
        model = Category
        fields = ['id', 'post_id', 'post_title', 'tag_id', 'tag']

class PostFilter(FilterSet):
    category_id = filters.NumberFilter(field_name='category__id')
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    tag_id = filters.NumberFilter(field_name='tags__id')
    tag = filters.CharFilter(field_name='tags__tag', lookup_expr='iexact')
    
    tags = CharInFilter(field_name='tags__tag', lookup_expr='in')
    
    class Meta:
        model = Post
        fields = ['id', 'category_id', 'category_name', 'title', 'tag_id', 'tag']


class TagFilter(FilterSet):
    tag = filters.CharFilter(field_name='tag', lookup_expr='icontains')
    post_id = filters.NumberFilter(field_name='post__id')
    post_title = filters.NumberFilter(field_name='post__title', lookup_expr='iexact')
    category_id = filters.NumberFilter(field_name='post__category__id')
    category_name = filters.NumberFilter(field_name='post__category__name', lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ['id', 'tag', 'post_id', 'post_title', 'category_id', 'category_name']


class ProjectFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    class Meta:
        model = Project
        fields = ['id' ,'name', 'rank']