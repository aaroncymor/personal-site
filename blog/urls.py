from django.urls import path

from .views import PostListView, PostDetailView, PostFormView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('/<int:pk>', PostDetailView.as_view(), name='post-detail'),
]