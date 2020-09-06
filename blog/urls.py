from django.urls import path

from .views import (
    PostListView,
    PostDetailView,
    PostFormView,
    PostDecipherFormView,
    delete_post,
    submit_post_search,
    get_random_tags,
    get_deciphers_by_post,
    get_post_list,
    get_post_detail,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/delete', delete_post, name='post-delete'),
    path('posts/<int:pk>/deciphers', get_deciphers_by_post, name='post-decipher-list'),
    path('posts/<int:post_id>/deciphers/<int:decipher_id>/form', PostDecipherFormView.as_view(), name='post-decipher-form'),
    path('form', PostFormView.as_view(), name='post-form'),
    path('search', submit_post_search, name='post-search'),
    path('random_tags', get_random_tags, name='post-random-tags' ),

    path('post-list', get_post_list, name='post-list-2' ),
    path('post-detail', get_post_detail, name='post-detail-2'),
]