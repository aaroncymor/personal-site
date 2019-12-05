from django.urls import path

from .views import (
    HomeView, LoginView,
    DashboardView, logout_view,
    PrivacyPolicyView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('privacypolicy/', PrivacyPolicyView.as_view(), name='privacypolicy'),
]