from django.urls import path

from .views import (
    PostListView,
    PostDetailView,
    PostFormView,
    delete_post,
    submit_post_search,
    get_random_tags
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/delete', delete_post, name='post-delete'),
    path('form', PostFormView.as_view(), name='post-form'),
    path('search', submit_post_search, name='post-search'),
    path('random_tags', get_random_tags, name='post-random-tags' )
]