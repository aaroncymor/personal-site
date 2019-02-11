from django.urls import path

from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectFormView,
    get_project_rankings,
    update_project_rankings
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('form', ProjectFormView.as_view(), name='project-form'),
    path('rank_list', get_project_rankings, name='project-rank-list'),
    path('rank_list_update', update_project_rankings, name='project-rank-list-update'),
]