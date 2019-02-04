from django.urls import path

from .views import ProjectListView, ProjectDetailView, ProjectFormView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('form', ProjectFormView.as_view(), name='project-form'),
]