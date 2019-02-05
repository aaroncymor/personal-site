"""myportfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from filebrowser.sites import site

from .core import views as core_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # django-filebrowser url requires to be before admin url
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('tinymce/', include('tinymce.urls')),

    path('admin/', admin.site.urls),
    path('', core_views.HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='myportfolio/login.html'), name='login'),
    path('dashboard/', core_views.DashboardView.as_view(), name='dashboard'),
    path('blog/', include('blog.urls')),
    path('projects/', include('projects.urls')),
]
