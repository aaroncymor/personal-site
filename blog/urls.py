from django.urls import path

from .views import (
    PostListView,
    PostDetailView,
    PostFormView,
    DecipherFormView,
    delete_post,
    submit_post_search,
    get_random_tags,
    get_deciphers_by_post
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/delete', delete_post, name='post-delete'),
    path('posts/<int:pk>/deciphers', get_deciphers_by_post, name='post-decipher-list'),
    #path('form', PostFormView.as_view(), name='post-form'),
    path('search', submit_post_search, name='post-search'),
    path('random_tags', get_random_tags, name='post-random-tags' )
]